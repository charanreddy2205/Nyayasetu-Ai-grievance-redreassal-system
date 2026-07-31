import nltk
import logging
from nltk.sentiment.vader import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)

def ensure_nltk_resources():
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon')

def analyze_complaint(text):
    """
    Analyzes the complaint text and returns an urgency level.
    """
    try:
        ensure_nltk_resources()
        
        sid = SentimentIntensityAnalyzer()
        scores = sid.polarity_scores(text)
        compound_score = scores['compound']
        
        # Dangerous keywords list
        dangerous_keywords = [
            "violence", "suicide", "bomb", "threat", "kill", "attack", 
            "emergency", "urgent", "death", "blood", "fire", "weapon"
        ]
        
        text_lower = text.lower()
        has_danger = any(keyword in text_lower for keyword in dangerous_keywords)
        
        if has_danger or compound_score < -0.6:
            return 'critical'
        elif compound_score < -0.3:
            return 'high'
        elif compound_score < 0.1:
            return 'medium'
        else:
            return 'low'
    except Exception as e:
        logger.error(f"AI Engine Error: {e}", exc_info=True)
        return 'low' # Default to low urgency on failure


def classify_department(text):
    """
    Classifies the complaint text into one of the known departments:
    'electricity', 'Drainage', or 'Road & Safety'.
    """
    if not text:
        return 'Road & Safety'
        
    text_lower = text.lower()
    
    # Keyword sets
    electricity_keywords = ["power", "electricity", "electric", "pole", "light", "outage", "transformer", "wire", "shock", "blackout", "bulb", "short circuit", "spark", "cable", "current"]
    drainage_keywords = ["drain", "drainage", "sewage", "sewer", "water leak", "overflow", "leakage", "stink", "dirty water", "clog", "pipe", "gutter", "blockage", "manhole"]
    road_keywords = ["road", "pothole", "traffic", "safety", "street", "path", "accident", "cracks", "construction", "asphalt", "sidewalk", "divider", "pavement"]
    
    # Calculate matches
    electricity_hits = sum(keyword in text_lower for keyword in electricity_keywords)
    drainage_hits = sum(keyword in text_lower for keyword in drainage_keywords)
    road_hits = sum(keyword in text_lower for keyword in road_keywords)
    
    # Return the one with highest hits, default to 'Road & Safety' if all 0
    max_hits = max(electricity_hits, drainage_hits, road_hits)
    if max_hits == 0:
        return 'Road & Safety'  # Fallback department
        
    if max_hits == electricity_hits:
        return 'electricity'
    elif max_hits == drainage_hits:
        return 'Drainage'
    else:
        return 'Road & Safety'


def generate_summary(text):
    """
    Generates a concise summary of the complaint description.
    """
    if not text:
        return ""
    
    # Try using nltk to sentence-tokenize
    try:
        import nltk
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            try:
                nltk.download('punkt_tab')
            except Exception:
                pass
        
        from nltk.tokenize import sent_tokenize
        sentences = sent_tokenize(text)
    except Exception:
        # Fallback simple sentence tokenizer by splitting on common sentence boundaries
        import re
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
    if not sentences:
        return text
        
    # Take first two sentences and cap length
    summary_sentences = sentences[:2]
    summary = " ".join(summary_sentences)
    if len(summary) > 200:
        summary = summary[:197] + "..."
    return summary
