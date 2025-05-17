from pydantic import RootModel

from src.core.types.dto import BaseDTO


class ProofInvalidLengthHTTPExceptionDTO(BaseDTO):
    detail: str


class ProofVerificationFailedHTTPExceptionDTO(BaseDTO):
    detail: str


class ProofInvalidFormatHTTPExceptionDTO(BaseDTO):
    detail: str


class ProofExpiredHTTPExceptionDTO(BaseDTO):
    detail: str


ProofHTTPExceptions = (
    ProofInvalidLengthHTTPExceptionDTO
    | ProofVerificationFailedHTTPExceptionDTO
    | ProofInvalidFormatHTTPExceptionDTO
    | ProofExpiredHTTPExceptionDTO
)


class ProofHTTPExceptionDTO(RootModel[ProofHTTPExceptions]): ...
