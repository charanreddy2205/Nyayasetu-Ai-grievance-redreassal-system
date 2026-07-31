import threading
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


def _preload_nltk_resources() -> None:
    """
    Downloads and caches NLTK resources in a background thread to
    avoid blocking the first request after server boot.
    """
    try:
        import nltk
        resources = [
            ('tokenizers/punkt_tab', 'punkt_tab'),
            ('sentiment/vader_lexicon', 'vader_lexicon'),
        ]
        for find_path, package_name in resources:
            try:
                nltk.data.find(find_path)
            except LookupError:
                nltk.download(package_name, quiet=True)
                logger.info(f"[AppConfig] NLTK resource downloaded: {package_name}")
        logger.info("[AppConfig] All NLTK resources verified and ready.")
    except Exception as e:
        logger.warning(f"[AppConfig] NLTK preload failed (non-critical): {e}")


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self) -> None:
        """
        Triggered once Django finishes loading all apps.
        Preloads NLP lexicons in the background.
        """
        import os
        # Prevent running on management command subprocesses (migrations etc.)
        if os.environ.get('RUN_MAIN') or os.environ.get('DYNO'):
            thread = threading.Thread(target=_preload_nltk_resources, daemon=True)
            thread.start()
