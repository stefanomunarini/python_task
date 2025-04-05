import os
import re

import httpx
from dotenv import load_dotenv

load_dotenv()

CHUTES_API_KEY = os.getenv("CHUTES_API_KEY")
CHUTES_URL = "https://llm.chutes.ai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {CHUTES_API_KEY}",
    "Content-Type": "application/json"
}

MODEL = "unsloth/Llama-3.2-3B-Instruct"

async def get_sentiment_score(tweets: list[str]) -> int:
    prompt = (
            "Given the following tweets about Bittensor, analyze the overall sentiment.\n"
            "Respond with only a number between -100 and 100. No explanation. No breakdown. No citations. Only the sentiment score value. *Format your response exactly like this*:\n"
            "`sentiment_score: <number>`\n\n"
            "Tweets:\n\n" + "\n".join(tweets)
    )

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 64,
        "temperature": 0.3,
        "stream": False
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            CHUTES_URL,
            headers=HEADERS,
            json=payload
        )
        response.raise_for_status()
        result = response.json()

    try:
        match = re.search(
            r"(?i)sentiment\s*score\s*[:\-]?\s*(-?\d+)",
            result["choices"][0]["message"]["content"]
        )
        if not match:
            raise ValueError(
                "Unable to read sentiment score from LLM response."
                "Possibly malformed response")
        score = int(match.group(1))
        return max(-100, min(100, score))
    except Exception as e:
        raise ValueError(f'Failed to parse sentiment score. Reason: {e}')
