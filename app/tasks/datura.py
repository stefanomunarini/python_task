import asyncio

from app.celery import celery
from app.services.datura import get_datura_tweets


@celery.task
def get_datura_tweets_task(query: str):
    return asyncio.run(get_datura_tweets(query))
