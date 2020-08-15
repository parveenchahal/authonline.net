from dataclasses import dataclass
from http_responses.models.response_model import ResponseModel as _ResponseModel

@dataclass
class Oath2TokenResponse(_ResponseModel):
    access_token: str
