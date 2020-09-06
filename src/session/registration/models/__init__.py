from dataclasses import dataclass
from common import Model
from typing import List

@dataclass
class SessionRegistrationDetailsModel(Model):
    object_id: str
    client_id: str
    redirect_uri: str
    resources: List[str]
    