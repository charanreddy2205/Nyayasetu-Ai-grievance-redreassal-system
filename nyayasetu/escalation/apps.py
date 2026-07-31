from django.apps import AppConfig


class EscalationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'escalation'

    def ready(self):
        import os
        import sys
        
        # Prevent scheduler from running multiple times in development (reloader)
        # or during migrations
        if os.environ.get('RUN_MAIN', None) != 'true' and 'runserver' in sys.argv:
            return
        if 'migrate' in sys.argv or 'makemigrations' in sys.argv:
            return
            
        from .scheduler import start
        start()
