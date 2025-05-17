from typing import Annotated

from fastapi import Depends, Query, WebSocketException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    PyJWTError,
)
from loguru import logger
from starlette import status

from src.core.api.exceptions.details import ExceptionDetail
from src.core.api.exceptions.http.common import AuthenticationHTTPException
from src.modules.auth.dto import JWTPayload
from src.modules.auth.services.jwt import JWT

users_security = HTTPBearer(auto_error=False)

__all__ = ("JWTPayloadDep", "WebSocketJWTPayloadDep")


async def get_jwt_payload(creds: Annotated[HTTPAuthorizationCredentials | None, Depends(users_security)]) -> JWTPayload:
    if not creds:
        raise AuthenticationHTTPException(detail=ExceptionDetail.missing_authorization_credentials)

    try:
        return JWT.decode(token=creds.credentials)
    except ExpiredSignatureError as exc:
        raise AuthenticationHTTPException(detail=ExceptionDetail.expired_jwt) from exc
    except (ValueError, DecodeError, InvalidSignatureError, PyJWTError) as exc:
        raise AuthenticationHTTPException(detail=ExceptionDetail.invalid_jwt) from exc


JWTPayloadDep = Annotated[JWTPayload, Depends(get_jwt_payload)]


async def get_jwt_payload_for_ws(token: Annotated[str | None, Query()] = None) -> JWTPayload:
    if not token:
        logger.info("forbiddenn!!!!!")
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason=ExceptionDetail.missing_authorization_credentials,
        )

    try:
        return JWT.decode(token=token)
    except ExpiredSignatureError as exc:
        logger.info("forbiddenn!!!!!")
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason=ExceptionDetail.expired_jwt) from exc
    except (ValueError, DecodeError, InvalidSignatureError, PyJWTError) as exc:
        logger.info("forbiddenn!!!!!")
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason=ExceptionDetail.invalid_jwt) from exc


WebSocketJWTPayloadDep = Annotated[JWTPayload, Depends(get_jwt_payload_for_ws)]
