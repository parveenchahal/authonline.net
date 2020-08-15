from dataclasses import dataclass
from http_responses.models.response_model import ResponseModel as _ResponseModel
from http import HTTPStatus

@dataclass
class MessageResponseModel(_ResponseModel):
    message: str

