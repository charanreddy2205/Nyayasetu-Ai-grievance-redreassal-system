import logging
from ai.config import (
    DANGER_KEYWORDS, URGENCY_THRESHOLD_CRITICAL, URGENCY_THRESHOLD_HIGH,
    URGENCY_THRESHOLD_MEDIUM, DEFAULT_URGENCY_LEVEL
)

logger = logging.getLogger(__name__)

class UrgencyEvaluator:
    """
    Evaluates grievance urgency classification.
    Merges sentiment compound polarity scores with danger threat keyword overrides.
    """
    
    @staticmethod
    def evaluate(text: str, sentiment_score: float) -> str:
        """
        Computes urgency category classification.

        Args:
            text: Grievance description.
            sentiment_score: Sentiment polarity compound score (-1.0 to 1.0).

        Returns:
            Urgency classification category (low, medium, high, critical).
        """
        if not text:
            return DEFAULT_URGENCY_LEVEL

        text_lower = text.lower()
        
        # Check for danger keyword threats
        has_danger = any(kw in text_lower for kw in DANGER_KEYWORDS)
        
        # Combine compound sentiment logic with threat overlays
        if has_danger or sentiment_score <= URGENCY_THRESHOLD_CRITICAL:
            return 'critical'
        elif sentiment_score <= URGENCY_THRESHOLD_HIGH:
            return 'high'
        elif sentiment_score <= URGENCY_THRESHOLD_MEDIUM:
            return 'medium'
        else:
            return DEFAULT_URGENCY_LEVEL
