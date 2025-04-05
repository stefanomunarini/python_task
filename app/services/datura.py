import logging
import os

import httpx
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

URL = "https://apis.datura.ai/twitter"

HEADERS = {
    "Authorization": os.getenv('DATURA_API_KEY'),
    "Content-Type": "application/json"
}

PAYLOAD = {
    "query": "",
    "blue_verified": False,
    "end_date": "2025-02-17",
    "is_image": False,
    "is_quote": False,
    "is_video": False,
    "lang": "en",
    "min_likes": 0,
    "min_replies": 0,
    "min_retweets": 0,
    "sort": "Top",
    "start_date": "2025-02-16",
    "count": 20
}


async def get_datura_tweets(query: str):
    PAYLOAD["query"] = query
    response = httpx.post(URL, json=PAYLOAD, headers=HEADERS)
    logger.info(response.json())
    return response.json()
