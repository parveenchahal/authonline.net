from dataclasses import dataclass
from common import Model
from typing import List

@dataclass
class SessionRegistrationDetailsModel(Model):
    client_id: str
    resource: str
    owners: List[str]
    redirect_uris: List[str]
