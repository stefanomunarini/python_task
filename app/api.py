import logging
import logging
import os
from typing import Annotated

from bittensor_wallet import Wallet
from celery import chain
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException

from app.auth import validate_token
from app.redis import get_cached_result, set_cached_result
from app.services.bittensor import fish
from app.tasks.datura import get_datura_tweets_task

load_dotenv()
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/ping")
async def ping():
    return {"ping": "pong"}


@router.get("/tao_dividends")
async def tao_dividends(
        netuid: Annotated[int, "Subnet ID"] = None,
        hotkey: Annotated[str, "Account"] = None,
        _: dict = Depends(validate_token),
        trade: bool = False
):
    cached = False
    staked = False

    if results := await get_cached_result(f"{netuid}_{hotkey}"):
        cached = True
    else:
        wallet = Wallet(hotkey=os.getenv('WALLET_HOTKEY')).create_if_non_existent()
        try:
            results, block_hash = await fish(netuid, wallet.hotkey.public_key)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"fish() failed: {e}")

        await set_cached_result(f"{netuid}_{hotkey}", results, ttl=60*2) # TODO results is empty

    if trade:
        chain(
            get_datura_tweets_task.s(f"Bittensor netuid {netuid}"),
            # process_sentiment_task.s(),
            # submit_stake_adjustment_task.s()
        ).delay()

    return {
        "netuid": netuid,
        "hotkey": hotkey,
        "dividend": 123456789, # TODO mangle results
        "cached": cached,
        "stake_tx_triggered": staked
    }
