import os

import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)


async def get_cached_result(key):
    return await redis_client.get(key)

async def set_cached_result(key, value, ttl=60*2):
    await redis_client.set(key, value, ex=ttl)
