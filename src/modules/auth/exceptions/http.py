from fastapi import status

from src.core.api.exceptions.http.base import BaseHTTPException
from src.modules.auth.constants import PROOF_LENGTH
from src.modules.auth.exceptions.details import ProofVerificationExceptionDetail


class BaseProofHTTPException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail: str = "Proof verification failed"


class ProofInvalidLengthHTTPException(BaseProofHTTPException):
    detail: str = ProofVerificationExceptionDetail.invalid_length_exception.format(length=PROOF_LENGTH)


class ProofVerificationFailedHTTPException(BaseProofHTTPException):
    detail: str = ProofVerificationExceptionDetail.verification_failed_exception


class ProofInvalidFormatHTTPException(BaseProofHTTPException):
    detail: str = ProofVerificationExceptionDetail.invalid_proof_format_exception


class ProofExpiredHTTPException(BaseProofHTTPException):
    detail: str = ProofVerificationExceptionDetail.proof_expired_exception
