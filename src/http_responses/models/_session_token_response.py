from dataclasses import dataclass
from common.abstract_model import Model as _Model

@dataclass
class SessionTokenResponse(_Model):
    session: str
