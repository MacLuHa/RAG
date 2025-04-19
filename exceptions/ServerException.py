
class ServerException(Exception):
    def __init__(self, message: str, status_code: int = 500, code: str = "SERVER ERROR"):
        self.message = message
        self.status_code = status_code
        self.code = code

    def to_dict(self):
        return {
            'error': self.message,
            'code': self.code
        }
    