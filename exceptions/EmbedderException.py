from .ServerException import ServerException

class EmbedderException(ServerException):
    def __init__(self, message, status_code = 500, code = "EMBEDDER ERROR"):
        super().__init__(message, status_code, code)