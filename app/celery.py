import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

celery = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)
celery.autodiscover_tasks(["app.tasks.datura"])
