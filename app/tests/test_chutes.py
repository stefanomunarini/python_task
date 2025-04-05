import pytest

from app.services.chutes import get_sentiment_score


@pytest.mark.asyncio
async def test_sentiment_score():
    tweets = [
        "Bittensor is the future of decentralized AI.",
        "Super innovative and super promising subnet."
    ]
    score = await get_sentiment_score(tweets)
    assert isinstance(score, int)
    assert -100 <= score <= 100
