import logging
import re
import time
from dataclasses import dataclass, field
from typing import Optional
from ai.classification import DepartmentClassifier
from ai.sentiment import SentimentAnalyzerFactory
from ai.summarization import SummarizerFactory
from ai.urgency import UrgencyEvaluator
from ai.config import DEFAULT_URGENCY_LEVEL, DEFAULT_DEPARTMENT_NAME

logger = logging.getLogger(__name__)


@dataclass
class AIPipelineResult:
    """
    Carries the full AI analysis results for a grievance text.
    """
    department_name: str = DEFAULT_DEPARTMENT_NAME
    urgency_level: str = DEFAULT_URGENCY_LEVEL
    sentiment_score: float = 0.0
    summary: str = ""
    processing_ms: float = 0.0
    fallback_used: bool = False
    errors: list = field(default_factory=list)


def clean_text(text: str) -> str:
    """
    Normalises and sanitizes raw complaint text for downstream NLP processing.
    Removes excessive whitespace and special characters.
    """
    if not text:
        return ""
    # Collapse multiple whitespace, strip leading/trailing spaces
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove null bytes and control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return text


class AIProcessingPipeline:
    """
    Orchestrates the sequential AI stages for processing grievance descriptions.

    Stages:
        1. Text Cleaning
        2. Department Classification
        3. Sentiment Analysis
        4. Urgency Evaluation
        5. Summary Generation

    Designed to be safely reusable and extensible.
    """

    def __init__(self) -> None:
        self._sentiment_analyzer = SentimentAnalyzerFactory.get_analyzer()
        self._summarizer = SummarizerFactory.get_summarizer()

    def process(self, complaint_id: int, text: str) -> AIPipelineResult:
        """
        Runs all AI pipeline stages on a complaint description.

        Args:
            complaint_id: Database PK used for logging correlation.
            text: Raw complaint description text.

        Returns:
            AIPipelineResult containing all classification outputs.
        """
        start = time.monotonic()
        result = AIPipelineResult()

        # Minimum length validation
        if not text or len(text.strip()) < 5:
            logger.warning(f"[Pipeline][Complaint #{complaint_id}] Text too short, returning defaults.")
            result.fallback_used = True
            return result

        # Stage 1: Text Cleaning
        cleaned = clean_text(text)

        # Stage 2: Department Classification
        try:
            result.department_name = DepartmentClassifier.classify(cleaned)
        except Exception as e:
            logger.error(f"[Pipeline][Complaint #{complaint_id}] Classification failed: {e}")
            result.department_name = DEFAULT_DEPARTMENT_NAME
            result.fallback_used = True
            result.errors.append(f"classification_error: {e}")

        # Stage 3: Sentiment Analysis
        try:
            result.sentiment_score = self._sentiment_analyzer.analyze_sentiment(cleaned)
        except Exception as e:
            logger.error(f"[Pipeline][Complaint #{complaint_id}] Sentiment analysis failed: {e}")
            result.sentiment_score = 0.0
            result.fallback_used = True
            result.errors.append(f"sentiment_error: {e}")

        # Stage 4: Urgency Evaluation
        try:
            result.urgency_level = UrgencyEvaluator.evaluate(cleaned, result.sentiment_score)
        except Exception as e:
            logger.error(f"[Pipeline][Complaint #{complaint_id}] Urgency evaluation failed: {e}")
            result.urgency_level = DEFAULT_URGENCY_LEVEL
            result.fallback_used = True
            result.errors.append(f"urgency_error: {e}")

        # Stage 5: Summary Generation
        try:
            result.summary = self._summarizer.summarize(cleaned)
        except Exception as e:
            logger.error(f"[Pipeline][Complaint #{complaint_id}] Summarization failed: {e}")
            result.summary = cleaned[:200] + "..." if len(cleaned) > 200 else cleaned
            result.fallback_used = True
            result.errors.append(f"summarization_error: {e}")

        result.processing_ms = (time.monotonic() - start) * 1000
        logger.info(
            f"[Pipeline][Complaint #{complaint_id}] "
            f"Completed in {result.processing_ms:.1f}ms | "
            f"dept={result.department_name} | urgency={result.urgency_level} | "
            f"sentiment={result.sentiment_score:.3f} | fallback={result.fallback_used}"
        )
        return result
