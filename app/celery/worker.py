import time

from celery import Celery

from app.core.config import settings

celery = Celery(__name__)
celery.conf.broker_url = settings.get_celery_broker_uri
celery.conf.result_backend = settings.get_backend_uri

@celery.task(name='create_task')
def create_task(task_type):
    time.sleep(10 * task_type)
    return True
