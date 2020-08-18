from dataclasses import dataclass
from common.abstract_model import Model as _Model
from http import HTTPStatus

@dataclass
class MessageResponseModel(_Model):
    message: str

