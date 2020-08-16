from dataclasses import dataclass
from common.abstract_model import Model as _Model

@dataclass
class Oath2TokenResponse(_Model):
    access_token: str