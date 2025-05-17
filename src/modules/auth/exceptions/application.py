from src.core.exceptions import ApplicationBaseException


class ProofVerificationException(ApplicationBaseException):
    message: str
