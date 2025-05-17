from fastapi import status

from src.core.api.exceptions.details import ExceptionDetail
from src.core.api.exceptions.http.base import BaseHTTPException


class InternalServerErrorHTTPException(BaseHTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = ExceptionDetail.server_error


class AuthenticationHTTPException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail: str = ExceptionDetail.missing_authorization_credentials


class PermissionDenied(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = ExceptionDetail.permission_denied


class NotFound(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = ExceptionDetail.not_found
