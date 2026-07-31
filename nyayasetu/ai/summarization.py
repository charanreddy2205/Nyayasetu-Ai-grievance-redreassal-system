import logging
import re
import nltk
from ai.config import SUMMARIZER_STRATEGY

logger = logging.getLogger(__name__)

def ensure_punkt_downloaded() -> None:
    try:
        nltk.data.find('tokenizers/punkt_tab.zip')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)


class BaseSummarizer:
    """
    Contract for pluggable text summarization routines.
    """
    def summarize(self, text: str) -> str:
        raise NotImplementedError("Subclasses must implement summarize")


class SentenceTokenizeSummarizer(BaseSummarizer):
    """
    Extractive summarization using NLTK sentence tokenization (taking first 2 sentences).
    """
    def summarize(self, text: str) -> str:
        if not text:
            return ""
            
        try:
            ensure_punkt_downloaded()
            from nltk.tokenize import sent_tokenize
            sentences = sent_tokenize(text)
        except Exception as e:
            logger.warning(f"NLTK sentence tokenize failed, using regex fallback: {e}")
            sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
            
        if not sentences:
            return text
            
        summary_sentences = sentences[:2]
        summary = " ".join(summary_sentences)
        if len(summary) > 200:
            summary = summary[:197] + "..."
        return summary


class TextRankSummarizer(BaseSummarizer):
    """
    Stub for Graph-based extractive summarization (TextRank).
    """
    def summarize(self, text: str) -> str:
        logger.info("TextRank Summarizer stub executed.")
        # Fallback directly
        return SentenceTokenizeSummarizer().summarize(text)


class SummarizerFactory:
    """
    Factory creating instances of Summarizers based on active settings.
    """
    @staticmethod
    def get_summarizer() -> BaseSummarizer:
        if SUMMARIZER_STRATEGY == 'textrank':
            return TextRankSummarizer()
        return SentenceTokenizeSummarizer()
