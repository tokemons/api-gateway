from typing import cast

from fastapi import HTTPException
from pytoniq import Address, AddressError
from starlette.status import HTTP_400_BAD_REQUEST


async def validated_address(address: str) -> str:
    try:
        return cast("str", Address(address).to_str())
    except AddressError as exc:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid address",
        ) from exc
