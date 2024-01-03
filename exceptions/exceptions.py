class ErrorException(Exception):
    def __init__(self, message: str = "", error_code=500, *args, **kwargs):
        self.message = message
        self.error_code = error_code


class ServiceException(ErrorException):
    def __init__(self, message: str = "", error_code=500, *args, **kwargs):
        super().__init__(message, error_code, *args, **kwargs)
