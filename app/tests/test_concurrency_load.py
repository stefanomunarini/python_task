import asyncio

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_concurrent_requests():
    async def make_request():
        async with AsyncClient(app=app, base_url="http://test") as client:
            res = await client.get(
                "/api/v1/tao_dividends",
                params={"netuid": 18, "hotkey": "test"},
                headers={"Authorization": "Bearer supersecrettoken"}
            )
            assert res.status_code == 200

    # Fire 50 requests in parallel
    await asyncio.gather(*(make_request() for _ in range(50)))