from dataclasses import dataclass
from common.abstract_model import Model
from typing import List

@dataclass
class SessionRegistrationDetailsModel(Model):
    object_id: str
    client_id: str
    redirect_url: str
    resources: List[str]
    