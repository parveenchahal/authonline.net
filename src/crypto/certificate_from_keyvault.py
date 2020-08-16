from .certificate_handler import CertificateHandler
from requests import get as http_get, request
from datetime import datetime, timedelta
from typing import List
import copy
from threading import RLock
from .models.certificate import Certificate
from common.utils import parse_json, to_json_string


class CertificateFromKeyvault(CertificateHandler):

    _secret_uri: str
    _cached_secret: List[Certificate]
    _next_read: datetime
    _auth_uri: str
    _cache_timeout: timedelta
    _lock: RLock

    def __init__(self, secret_uri: str, cache_timeout: timedelta, auth_uri: str):
        self._secret_uri = secret_uri
        self._cached_secret = None
        self._cache_timeout = cache_timeout
        self._next_read = None
        self._auth_uri = auth_uri
        self._lock = RLock()

    def _update_required(self, now):
        return self._cached_secret is None or self._next_read is None or now >= self._next_read

    def get(self) -> List[Certificate]:
        now = datetime.utcnow()
        if self._update_required(now):
            with self._lock:
                if self._update_required(now):
                    res = http_get(self._auth_uri)
                    access_token = parse_json(res.text)["access_token"]
                    res = request("GET", self._secret_uri, headers={"Authorization": f'Bearer {access_token}'})
                    value = parse_json(res.text)['value']
                    cert_list = parse_json(value)
                    cert_list = [Certificate.from_json_string(Certificate, to_json_string(x)) for x in cert_list]
                    self._cached_secret = cert_list
                    self._next_read = now + self._cache_timeout
        return copy.deepcopy(self._cached_secret)