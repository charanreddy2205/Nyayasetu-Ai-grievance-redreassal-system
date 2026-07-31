import logging
from django.apps import apps
from ai.config import DEFAULT_DEPARTMENT_NAME, FALLBACK_DEPARTMENT_KEYWORDS

logger = logging.getLogger(__name__)

class DepartmentClassifier:
    """
    Classifies a grievance text into the best matching Department.
    Supports weighted database-backed keyword matching with hardcoded fallback routines.
    """
    
    @staticmethod
    def classify(text: str) -> str:
        """
        Classifies grievance text by scoring keyword frequency occurrences.
        """
        if not text:
            return DEFAULT_DEPARTMENT_NAME
            
        text_lower = text.lower()
        scores = {}
        
        try:
            # Dynamically resolve Department and DepartmentKeyword models
            # This prevents circular import errors on application boot
            DepartmentKeyword = apps.get_model('departments', 'DepartmentKeyword')
            
            # Fetch all keywords from the database
            db_keywords = DepartmentKeyword.objects.select_related('department').all()
            
            if db_keywords.exists():
                for kw in db_keywords:
                    dept_name = kw.department.name
                    scores[dept_name] = scores.get(dept_name, 0)
                    if kw.word.lower() in text_lower:
                        scores[dept_name] += kw.weight
            else:
                # Use fallback dictionary if no database keyword records exist
                for dept_name, keywords in FALLBACK_DEPARTMENT_KEYWORDS.items():
                    scores[dept_name] = 0
                    for word in keywords:
                        if word in text_lower:
                            scores[dept_name] += 1
        except Exception as e:
            logger.error(f"Error querying database keywords, using config fallbacks: {e}")
            for dept_name, keywords in FALLBACK_DEPARTMENT_KEYWORDS.items():
                scores[dept_name] = 0
                for word in keywords:
                    if word in text_lower:
                        scores[dept_name] += 1

        if not scores or max(scores.values()) == 0:
            return DEFAULT_DEPARTMENT_NAME

        # Resolve exact name match or pick max score department
        return max(scores, key=scores.get)
