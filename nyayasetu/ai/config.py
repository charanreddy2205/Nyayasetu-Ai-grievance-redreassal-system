import os

# Default Fallbacks
DEFAULT_URGENCY_LEVEL = 'low'
DEFAULT_DEPARTMENT_NAME = 'Road & Safety'

# Pluggable Model Switcher
# Allowed: 'vader', 'distilbert', 'huggingface_api'
SENTIMENT_MODEL_TYPE = os.environ.get('AI_SENTIMENT_MODEL_TYPE', 'vader')

# Summarizer Strategy Switcher
# Allowed: 'first_sentences', 'textrank', 'bart'
SUMMARIZER_STRATEGY = os.environ.get('AI_SUMMARIZER_STRATEGY', 'first_sentences')

# Keyword Classification Switcher
# Allowed: 'database_keywords', 'hardcoded', 'bert_classifier'
CLASSIFICATION_MODEL = os.environ.get('AI_CLASSIFICATION_MODEL', 'database_keywords')

# Urgency Rules Config
URGENCY_THRESHOLD_CRITICAL = -0.6
URGENCY_THRESHOLD_HIGH = -0.3
URGENCY_THRESHOLD_MEDIUM = 0.1

# Danger Threat Keywords for Urgency Overrides
DANGER_KEYWORDS = [
    'fire', 'explos', 'short circuit', 'spark', 'flood', 
    'collapse', 'poison', 'leakage', 'hazard', 'accident',
    'violence', 'suicide', 'bomb', 'threat', 'kill', 'attack', 
    'emergency', 'urgent', 'death', 'blood', 'weapon'
]

# Static Fallback Keywords for Classification (in case database keywords are empty)
FALLBACK_DEPARTMENT_KEYWORDS = {
    'Electricity & Power': [
        'power', 'electricity', 'electric', 'pole', 'light', 'outage', 
        'transformer', 'wire', 'shock', 'blackout', 'bulb', 'short circuit', 
        'spark', 'cable', 'current', 'streetlight', 'streetlights', 'lamp',
        'grid', 'voltage', 'electrocution', 'meter', 'switch', 'generator', 'phase'
    ],
    'Water & Sewage': [
        'drain', 'drainage', 'sewage', 'sewer', 'water leak', 'overflow', 
        'leakage', 'stink', 'dirty water', 'clog', 'pipe', 'gutter', 
        'blockage', 'manhole', 'pipeline', 'drinking water', 'tap', 'plumbing',
        'flooding', 'sanitation', 'mud', 'contaminated', 'tank'
    ],
    'Road & Safety': [
        'road', 'pothole', 'traffic', 'safety', 'street', 'path', 'accident', 
        'cracks', 'construction', 'asphalt', 'sidewalk', 'divider', 'pavement',
        'speed bump', 'signboard', 'crossing', 'highway', 'lane', 'intersection',
        'bridge', 'traffic light', 'block'
    ],
    'Sanitation & Waste': [
        'garbage', 'trash', 'waste', 'dump', 'smell', 'dustbin', 'sweeper',
        'clean', 'sanitation', 'debris', 'rubbish', 'litter', 'recycling', 
        'compost', 'landfill', 'pollution', 'odor', 'stagnant'
    ]
}
