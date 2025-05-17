class ApplicationBaseException(BaseException):
    message: str = "Application exception"

    def __init__(self, message: str | None = None) -> None:
        message = message or self.message
        super().__init__(message)
