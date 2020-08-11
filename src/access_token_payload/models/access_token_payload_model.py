from common.abstract_model import Model
from dataclasses import dataclass

@dataclass
class AccessTokenPayloadModel(Model):
    aud: str = None
    iss: str = None
    iat: str = None
    nbf: str = None
    exp: str = None
    jti: str = None
    sub: str = None
    scp: str = None
    username: str = None
    amr: list = None
    remote_addr: str = None

    def to_dict(self):
        return super().to_dict(omit_none=True)