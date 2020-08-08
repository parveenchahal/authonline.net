from flask_restful import ResponseBase

class ErrorResponse(ResponseBase):
    def __init__(self, msg: str, status: int, content_type: str):
        super().__init__(msg, status, content_type=content_type)

class BadRequest(ErrorResponse):
    __status_code = 400
    __content_type = "text/plain"
    def __init__(self, msg: str = "BadRequest"):
        super().__init__(msg, self.__status_code, content_type=self.__content_type)


class NotFound(ErrorResponse):
    __status_code = 404
    __content_type = "text/plain"
    def __init__(self, msg: str = "NotFound"):
        super().__init__(msg, self.__status_code, content_type=self.__content_type)

class Unauthorized(ErrorResponse):
    __status_code = 401
    __content_type = "text/plain"
    def __init__(self, msg: str = "Unauthorized"):
        super().__init__(msg, self.__status_code, content_type=self.__content_type)

class InternalServerError(ErrorResponse):
    __status_code = 500
    __content_type = "text/plain"
    def __init__(self, msg: str = "InternalServerError"):
        super().__init__(msg, self.__status_code, content_type=self.__content_type)

