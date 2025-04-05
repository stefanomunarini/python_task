import asyncio
import logging
from typing import Dict, Any

from app.celery import celery
from app.services.bittensor import submit_stake_adjustment
from app.services.chutes import get_sentiment_score

logger = logging.getLogger(__name__)


@celery.task
def process_sentiment_task(
        tweets_response: dict,
        netuid: int = 18,
        hotkey: str = "5FFApaS75bv5pJHfAp2FVLBj9ZaXuFDjEypsaBNc1wCfe52v"
) -> Dict[str, Any]:
    tweets = [
        tweet["text"]
        for tweet in tweets_response
    ]
    sentiment = asyncio.run(get_sentiment_score(tweets))
    logger.info({"sentiment": sentiment, "netuid": netuid, "hotkey": hotkey})
    return {"sentiment": sentiment, "netuid": netuid, "hotkey": hotkey}


@celery.task
def submit_stake_adjustment_task(result: dict) -> Dict[str, Any]:
    sentiment = result["sentiment"]
    netuid = result["netuid"]
    hotkey = result["hotkey"]

    amount = abs(sentiment) * 0.01

    if sentiment > 0:
        tx = asyncio.run(submit_stake_adjustment("stake", netuid, hotkey, amount))
    elif sentiment < 0:
        tx = asyncio.run(submit_stake_adjustment("unstake", netuid, hotkey, amount))
    else:
        tx = "neutral sentiment — no extrinsic sent"

    return {"sentiment": sentiment, "extrinsic": tx}
