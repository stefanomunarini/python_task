from celery import Celery

from app.config import get_settings

REDIS_URL = get_settings().redis_url

celery = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)
