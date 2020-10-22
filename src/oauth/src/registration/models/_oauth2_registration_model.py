from dataclasses import dataclass
from common import Model
from typing import Dict, List

@dataclass
class Oauth2RegistrationModel(Model):
    roles: Dict[str, List]
    resources: List[str]
