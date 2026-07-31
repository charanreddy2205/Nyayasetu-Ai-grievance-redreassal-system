import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nyayasetu.settings')

app = Celery('nyayasetu')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover task modules (tasks.py) in all registered Django apps
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self) -> None:
    """
    Simple verification task logging request info.
    """
    print(f'Request: {self.request!r}')
