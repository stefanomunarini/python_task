import os

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient

load_dotenv()


@pytest.mark.asyncio
async def test_tao_dividends():
    async with AsyncClient() as client:
        response = await client.get(
            "http://0.0.0.0:8000/api/v1/tao_dividends",
            params={"netuid": 18, "hotkey": os.getenv('WALLET_HOTKEY')},
            headers={"Authorization": f"Bearer {os.getenv('API_TOKEN')}"},
        )
    assert response.status_code == 200
    assert "dividend" in response.json()
