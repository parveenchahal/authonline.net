from jwt import JWT
from crypto.jwt.signing_key_handler import SigningKeyHandler
from jwt.utils import b64decode as _b64decode
from common.utils import bytes_to_string

class JWTTokenHandler(object):
    _jwt: JWT
    _signing_key_handler: SigningKeyHandler
    _alg: str

    def __init__(self, signing_key_handler: SigningKeyHandler, alg: str = "RS256"):
        self._signing_key_handler = signing_key_handler
        self._alg = alg
        self._jwt = JWT()

    def sign(self, payload: dict) -> str:
        key = self._signing_key_handler.get()
        access_token = self._jwt.encode(payload, key, alg=self._alg)
        return access_token

    @staticmethod
    def decode_payload(encoded_payload: str) -> str:
        b = _b64decode(encoded_payload)
        return bytes_to_string(b)