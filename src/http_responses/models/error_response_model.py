from dataclasses import dataclass
from common.abstract_model import Model as _Model
from http import HTTPStatus

@dataclass
class ErrorResponseModel(_Model):
    http_status_code: HTTPStatus
    error_message: str
