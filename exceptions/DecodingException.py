from .ServerException import ServerException

class DecodingException(ServerException):
    def __init__(self, message, status_code = 500, code = "DECODING ERROR"):
        super().__init__(message, status_code, code)