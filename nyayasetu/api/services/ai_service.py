import logging
from ai.classification import DepartmentClassifier
from ai.sentiment import SentimentAnalyzerFactory
from ai.summarization import SummarizerFactory
from ai.urgency import UrgencyEvaluator
from ai.config import DEFAULT_URGENCY_LEVEL, DEFAULT_DEPARTMENT_NAME

logger = logging.getLogger(__name__)


class AIService:
    """
    Thin service layer delegating NLP tasks to the modular ai/ package.
    Preserves backward compatibility with all existing callers.
    """

    @staticmethod
    def analyze_complaint(text: str) -> str:
        """
        Analyzes complaint text and returns urgency classification.

        Args:
            text: Complaint description.

        Returns:
            Urgency level string (low, medium, high, critical).
        """
        try:
            analyzer = SentimentAnalyzerFactory.get_analyzer()
            score = analyzer.analyze_sentiment(text)
            return UrgencyEvaluator.evaluate(text, score)
        except Exception as e:
            logger.error(f"AIService.analyze_complaint failed: {e}", exc_info=True)
            return DEFAULT_URGENCY_LEVEL

    @staticmethod
    def generate_summary(text: str) -> str:
        """
        Generates a concise extractive summary.

        Args:
            text: Complaint description.

        Returns:
            Summarized text string.
        """
        try:
            summarizer = SummarizerFactory.get_summarizer()
            return summarizer.summarize(text)
        except Exception as e:
            logger.error(f"AIService.generate_summary failed: {e}", exc_info=True)
            return text[:200] if text else ""

    @staticmethod
    def predict_department(text: str) -> str:
        """
        Predicts best matching department name using database keyword routing.

        Args:
            text: Complaint description.

        Returns:
            Department name string.
        """
        try:
            return DepartmentClassifier.classify(text)
        except Exception as e:
            logger.error(f"AIService.predict_department failed: {e}", exc_info=True)
            return DEFAULT_DEPARTMENT_NAME
