from threading import RLock
from jwt.jwk import AbstractJWKBase, RSAJWK, load_pem_public_key, default_backend
from crypto.certificate_handler import CertificateHandler
from crypto.jwt.key_handler import KeyHandler
from crypto.models import Certificate
from typing import List
from cryptography.hazmat.backends.openssl.backend import backend

class RSAPublicKeyHandler(KeyHandler):

    __lock: RLock
    __certificate_handler: CertificateHandler
    __key_list: List[AbstractJWKBase]

    def __init__(self, certificate_handler: CertificateHandler):
        self.__certificate_handler = certificate_handler
        self.__lock = RLock()

    def __get_key_obj(self, key: bytes) -> RSAJWK:
        print(key)
        key = load_pem_public_key(key, backend=default_backend())
        return RSAJWK(key)


    def get(self) -> List[AbstractJWKBase]:
        _, is_changed = self.__certificate_handler.get()
        if is_changed or self.__key_list is None:
            with self.__lock:
                cert_list, is_changed = self.__certificate_handler.get()
                if is_changed or self.__key_list is None:
                    self.__key_list = [self.__get_key_obj(cert.certificate) for cert in cert_list]
        return self.__key_list