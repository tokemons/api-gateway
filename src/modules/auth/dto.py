from datetime import UTC, datetime, timedelta
from typing import Annotated

from pydantic import Field
from typing_extensions import Doc

from src.config import settings
from src.core.types.dto import BaseDTO


class PayloadDTO(BaseDTO):
    payload: str


class Domain(BaseDTO):
    length_bytes: int = Field(alias="lengthBytes")
    value: str


class ProofDTO(BaseDTO):
    timestamp: int
    domain: Domain
    payload: str
    signature: str
    state_init: str


class ProofVerificationDTO(BaseDTO):
    address: str
    network: int
    proof: ProofDTO


def default_expire() -> int:
    default_expires_delta = timedelta(minutes=settings.jwt.access_token_expire_minutes)
    expire = datetime.now(tz=UTC) + default_expires_delta
    return int(expire.timestamp())


class JWTPayload(BaseDTO):
    address: Annotated[str, Doc("User address")]
    exp: Annotated[int, Doc("Unix timestamp in seconds")] = Field(default_factory=default_expire)


class JWTResponse(BaseDTO):
    token: str
