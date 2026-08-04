import logging
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from ai.config import SENTIMENT_MODEL_TYPE

logger = logging.getLogger(__name__)

def ensure_vader_downloaded() -> None:
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon', quiet=True)


class BaseSentimentAnalyzer:
    """
    Base contract for pluggable sentiment model integrations.
    """
    def analyze_sentiment(self, text: str) -> float:
        raise NotImplementedError("Subclasses must implement analyze_sentiment")


class VaderSentimentAnalyzer(BaseSentimentAnalyzer):
    """
    Sentiment polarity analyzer leveraging NLTK VADER.
    """
    def __init__(self) -> None:
        ensure_vader_downloaded()
        self.sid = SentimentIntensityAnalyzer()
        
        # Add custom grievance-specific words to lexicon
        custom_words = {
            'unsafe': -2.5,
            'danger': -3.0,
            'dark': -1.0,
            'broken': -2.0,
            'failure': -2.0,
            'urgent': -1.5,
            'hazard': -2.5,
            'leak': -1.5,
            'pothole': -1.5,
            'stink': -2.0
        }
        self.sid.lexicon.update(custom_words)

    def analyze_sentiment(self, text: str) -> float:
        if not text:
            return 0.0
        try:
            scores = self.sid.polarity_scores(text)
            return float(scores.get('compound', 0.0))
        except Exception as e:
            logger.error(f"VADER polarity calculation error: {e}", exc_info=True)
            return 0.0


class HuggingFaceSentimentAnalyzer(BaseSentimentAnalyzer):
    """
    Placeholder/stub for advanced HuggingFace transformers (e.g. DistilBERT).
    """
    def analyze_sentiment(self, text: str) -> float:
        logger.info("HuggingFace Sentiment Analyzer stub executed.")
        # Under production upgrades:
        # from transformers import pipeline
        # classifier = pipeline("sentiment-analysis")
        # result = classifier(text)[0]
        # return -1.0 if result['label'] == 'NEGATIVE' else 1.0
        return 0.0


class SentimentAnalyzerFactory:
    """
    Factory creating instances of SentimentAnalyzer based on active configurations.
    """
    @staticmethod
    def get_analyzer() -> BaseSentimentAnalyzer:
        if SENTIMENT_MODEL_TYPE == 'huggingface':
            return HuggingFaceSentimentAnalyzer()
        return VaderSentimentAnalyzer()
