from flask_restful import ResponseBase
import json

class ErrorResponse(ResponseBase):
    def __init__(self, msg: str, status: int, content_type: str = "application/json"):
        m = {
            "message": msg
        }
        super().__init__(json.dumps(m), status, content_type=content_type)

class BadRequest(ErrorResponse):
    __status_code = 400
    def __init__(self, msg: str = "BadRequest"):
        super().__init__(msg, self.__status_code)


class NotFound(ErrorResponse):
    __status_code = 404
    def __init__(self, msg: str = "NotFound"):
        super().__init__(msg, self.__status_code)

class Unauthorized(ErrorResponse):
    __status_code = 401
    def __init__(self, msg: str = "Unauthorized"):
        super().__init__(msg, self.__status_code)

class InternalServerError(ErrorResponse):
    __status_code = 500
    def __init__(self, msg: str = "InternalServerError"):
        super().__init__(msg, self.__status_code)

