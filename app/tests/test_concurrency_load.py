import asyncio
import os
import time

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient

load_dotenv()


@pytest.mark.asyncio
async def test_concurrent_requests():
    async def make_request():
        async with AsyncClient() as client:
            res = await client.get(
                "http://0.0.0.0:8000/api/v1/tao_dividends",
                params={"netuid": 18, "hotkey": os.getenv('WALLET_HOTKEY')},
                headers={"Authorization": f"Bearer {os.getenv('API_TOKEN')}"},
            )
            assert res.status_code == 200

    await asyncio.gather(*(make_request() for _ in range(1000)))
