from datetime import datetime, timedelta
from threading import RLock
from jwt.jwk import AbstractJWKBase, RSAJWK, load_pem_private_key, default_backend
from .._certificate_handler import CertificateHandler
from ._key_handler import KeyHandler
from typing import List
from cachetools import TTLCache, cachedmethod, cached

class Caching(object):
    def __init__(self):
        pass

class RSAPrivateKeyHandler(KeyHandler):

    _certificate_handler: CertificateHandler
    _cache_timeout: timedelta
    _ttl_cache: TTLCache
    _lock: RLock

    def __init__(self, certificate_handler: CertificateHandler, cache_timeout: timedelta = timedelta(seconds=10)):
        self._certificate_handler = certificate_handler
        self._cache_timeout = cache_timeout
        self._ttl_cache = TTLCache(1, cache_timeout.total_seconds)
        self._lock = RLock()

    def _get_key_obj(self, key: bytes) -> RSAJWK:
        key = load_pem_private_key(key, password=None, backend=default_backend())
        return RSAJWK(key)

    def get(self) -> List[AbstractJWKBase]:
        try:
            return self._ttl_cache['get']
        except KeyError:
            with self._lock:
                try:
                    return self._ttl_cache['get']
                except KeyError:
                    cert_list = self._certificate_handler.get()
                    key_list = [self._get_key_obj(cert.private_key) for cert in cert_list]
                    try:
                        pass
                        #self._ttl_cache['get'] = key_list
                    except ValueError:
                        pass
                    return key_list
