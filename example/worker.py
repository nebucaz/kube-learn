import os
from celery import Celery

celery_app = Celery('fetch-worker',
                    broker=os.getenv('CELERY_BROKER_URL'),
                    backend=os.getenv('CELERY_RESULT_BACKEND'))

@celery_app.task(bind=True, track_started=True)
def fetch_task(self, url):
    return f'done fetching url {url}'
