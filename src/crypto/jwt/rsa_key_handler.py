from threading import RLock
from jwt.jwk import AbstractJWKBase, RSAJWK, load_pem_private_key, default_backend
from crypto.certificate_handler import CertificateHandler
from crypto.jwt.signing_key_handler import SigningKeyHandler
from crypto.models import Certificate

class RSAKeyHandler(SigningKeyHandler):

    __lock: RLock
    __certificate_handler: CertificateHandler
    __key: AbstractJWKBase

    def __init__(self, certificate_handler: CertificateHandler):
        self.__certificate_handler = certificate_handler
        self.__lock = RLock()

    def get(self) -> AbstractJWKBase:
        _, is_changed = self.__certificate_handler.get()
        if is_changed or self.__key is None:
            with self.__lock:
                cert_list, is_changed = self.__certificate_handler.get()
                if is_changed or self.__key is None:
                    cert: Certificate = cert_list[0]
                    key = load_pem_private_key(cert.private_key, password=None, backend=default_backend())
                    self.__key = RSAJWK(key)
        return self.__key