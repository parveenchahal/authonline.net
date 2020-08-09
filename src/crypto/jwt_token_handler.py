import uuid
from jwt import JWT
from datetime import datetime, timedelta
from crypto import CertificateHandler
from crypto.models import Certificate
from common.utils import bytes_to_string

class JWTTokenHandler(object):

    __jwt: JWT
    __certificate_handler: CertificateHandler
    __alg: str = "RS256"
    __default_payload: dict = {
        "iss": "authonline.net",
    }

    def __init__(self, certificate_handler: CertificateHandler):
        self.__certificate_handler = certificate_handler
        self.__jwt = JWT()

    def get(self, payload: dict, expiry: timedelta = timedelta(hours=1)) -> str:
        payload = dict(payload, **self.__default_payload)
        now_utc = datetime.utcnow()
        exp = int(datetime.timestamp(now_utc + expiry))

        payload['iat'] = int(now_utc.timestamp())
        payload['nbf'] = int(now_utc.timestamp())
        payload['exp'] = exp
        payload['jti'] = str(uuid.uuid5(uuid.NAMESPACE_OID, f"{payload['sub']} + {str(exp)}"))
        cert: Certificate = self.__certificate_handler.get()[0]
        key = cert.private_key
        return bytes_to_string(__jwt.encode(payload, key, algorithm=self.__alg))