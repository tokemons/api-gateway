from src.core.api.exceptions.details import ExceptionDetail
from src.core.types.dto import BaseDTO


class InternalServerErrorHTTPExceptionDTO(BaseDTO):
    detail: str = ExceptionDetail.server_error
