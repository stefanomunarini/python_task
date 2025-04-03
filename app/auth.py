import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=True)

VALID_TOKENS = {
    os.getenv("API_TOKEN"): {
        "username": "api_user",
        "scopes": ["tao:read", "tao:write"]
    }
}


async def validate_token(token: str = Depends(oauth2_scheme)):
    if token not in VALID_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    return VALID_TOKENS[token]

async def get_user_data(
        user_data: dict = Depends(validate_token)
):
    return user_data
