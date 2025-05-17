from dataclasses import dataclass


@dataclass(frozen=True)
class ExceptionDetail:
    # NOTE: Basic
    permission_denied: str = "Permission denied"
    not_found: str = "Not found"

    # NOTE: Authentication
    authentication_failed: str = "Authentication failed"
    missing_authorization_credentials: str = "Missing Authorization Credentials"
    expired_jwt: str = "Expired JWT Credentials"
    invalid_jwt: str = "Invalid token"

    # NOTE: Server
    server_error: str = "Server internal error."
