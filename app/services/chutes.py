import os
import httpx
from dotenv import load_dotenv

load_dotenv()

CHUTES_API_KEY = os.getenv("CHUTES_API_KEY")
CHUTES_URL = "https://chutes.ai/api/v1/infer/chute/20acffc0-0c5f-58e3-97af-21fc0b261ec4"

HEADERS = {
    "Authorization": f"Bearer {CHUTES_API_KEY}",
    "Content-Type": "application/json"
}


async def get_sentiment_score(tweets: list[str]) -> int:
    prompt = "Given these tweets, analyze the overall sentiment for Bittensor and return a number between -100 and 100:\n\n"
    prompt += "\n\n".join(tweets)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            CHUTES_URL,
            headers=HEADERS,
            json={"input": {"prompt": prompt}}
        )
        response.raise_for_status()
        result = response.json()

    try:
        score = int(result["output"])
        return max(-100, min(100, score))
    except Exception as e:
        raise ValueError(f"Invalid sentiment score returned: {result}")
