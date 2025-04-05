import logging
from typing import Annotated

from celery import chain
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException

from app.auth import validate_token
from app.redis import get_cached_result, set_cached_result
from app.services.bittensor import fish
from app.tasks.chutes import process_sentiment_task, \
    submit_stake_adjustment_task
from app.tasks.datura import get_datura_tweets_task

load_dotenv()
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/tao_dividends")
async def tao_dividends(
        netuid: Annotated[int, "Subnet ID"] = None,
        hotkey: Annotated[str, "Account"] = None,
        _: dict = Depends(validate_token),
        trade: bool = False
):
    cached = False
    staked = False
    cahce_key = f"{netuid}_{hotkey}"

    if balance := await get_cached_result(cahce_key):
        cached = True
    else:
        try:
            results, block_hash = await fish(netuid, hotkey)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"fish() failed: {e}")

        balance = results[0] if len(results) > 0 else 0
        await set_cached_result(cahce_key, balance, ttl=60*2)

    if trade:
        chain(
            get_datura_tweets_task.s(f"Bittensor netuid {netuid}"),
            process_sentiment_task.s(netuid=netuid, hotkey=hotkey),
            submit_stake_adjustment_task.s()
        ).delay()
    return {
        "netuid": netuid,
        "hotkey": hotkey,
        "dividend": balance,
        "cached": cached,
        "stake_tx_triggered": staked
    }
