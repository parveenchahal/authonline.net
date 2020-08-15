from dataclasses import dataclass
from http_responses.models.response_model import ResponseModel as _ResponseModel
from http import HTTPStatus

@dataclass
class ErrorResponseModel(_ResponseModel):
    http_status_code: HTTPStatus
    error_message: str
