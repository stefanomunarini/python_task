from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth import validate_token

router = APIRouter()


@router.get("/tao_dividends")
async def tao_dividends(
        netuid: Annotated[str, "Subnet ID"],
        hotkey: Annotated[str, "Account"],

        _: dict = Depends(validate_token)
):

    return {"status": "ok"}
