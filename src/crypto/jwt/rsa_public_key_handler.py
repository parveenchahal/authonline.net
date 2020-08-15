from datetime import datetime, timedelta
from threading import RLock
from jwt.jwk import AbstractJWKBase, RSAJWK, load_pem_public_key, default_backend
from crypto.certificate_handler import CertificateHandler
from crypto.jwt.key_handler import KeyHandler
from typing import List
from cryptography.hazmat.backends.openssl.backend import backend

class RSAPublicKeyHandler(KeyHandler):

    __lock: RLock
    __certificate_handler: CertificateHandler
    __key_list: List[AbstractJWKBase]
    __cache_timeout: timedelta
    __next_read: datetime

    def __init__(self, certificate_handler: CertificateHandler, cache_timeout: timedelta = timedelta(hours=1)):
        self.__certificate_handler = certificate_handler
        self.__cache_timeout = cache_timeout
        self.__lock = RLock()
        self.__key_list = None
        self.__next_read = None

    def __update_required(self, now):
        return self.__key_list is None or self.__next_read is None or now >= self.__next_read

    def __get_key_obj(self, key: bytes) -> RSAJWK:
        key = load_pem_public_key(key, backend=default_backend())
        return RSAJWK(key)


    def get(self) -> List[AbstractJWKBase]:
        now = datetime.utcnow()
        if self.__update_required(now):
            with self.__lock:
                if self.__update_required(now):
                    cert_list = self.__certificate_handler.get()
                    self.__key_list = [self.__get_key_obj(cert.certificate) for cert in cert_list]
                    self.__next_read = now + self.__cache_timeout
        return self.__key_list