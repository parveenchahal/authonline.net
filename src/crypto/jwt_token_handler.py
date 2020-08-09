import uuid
from jwt import JWT
from jwt.jwk import RSAJWK, RSAPrivateKey, load_pem_private_key, default_backend
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

    def get(self, payload: dict, expiry: timedelta = timedelta(hours=1)) -> dict:
        payload = dict(payload, **self.__default_payload)
        now_utc = datetime.utcnow()
        exp = int(datetime.timestamp(now_utc + expiry))

        payload['iat'] = int(now_utc.timestamp())
        payload['nbf'] = int(now_utc.timestamp())
        payload['exp'] = exp
        payload['jti'] = str(uuid.uuid5(uuid.NAMESPACE_OID, f"{payload['sub']} + {str(exp)}"))
        cert: Certificate = self.__certificate_handler.get()[0]
        key = load_pem_private_key(cert.private_key, password=None, backend=default_backend())
        access_token = self.__jwt.encode(payload, RSAJWK(key), alg=self.__alg)
        return {
            'access_token': access_token
        }
