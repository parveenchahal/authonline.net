from common import Model
from dataclasses import dataclass

@dataclass
class AccessTokenPayloadModel(Model):
    aud: str = None
    iss: str = None
    iat: int = None
    nbf: int = None
    exp: int = None
    jti: str = None
    sid: str = None
    sub: str = None
    scp: str = None
    usr: str = None
    object_id: str = None
    amr: list = None
    ip_addr: str = None

    def to_dict(self):
        return super().to_dict(omit_none=True)