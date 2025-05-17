from datetime import timedelta

import jwt

from src.config import settings
from src.modules.auth.dto import JWTPayload, JWTResponse


class JWT:
    _default_expires_delta = timedelta(minutes=settings.jwt.access_token_expire_minutes)
    _secret_key = settings.jwt.secret_key

    @classmethod
    def decode(cls, token: str) -> JWTPayload:
        payload = jwt.decode(
            jwt=token,
            key=cls._secret_key.get_secret_value(),
            algorithms=["HS256"],
        )
        return JWTPayload.model_validate(payload)

    @classmethod
    def encode(cls, data: JWTPayload) -> JWTResponse:
        token = jwt.encode(
            payload=data.model_dump(mode="json"),
            key=cls._secret_key.get_secret_value(),
            algorithm="HS256",
        )
        return JWTResponse(token=token)
