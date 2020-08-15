from crypto.certificate_handler import CertificateHandler
from requests import get as http_get, request
from datetime import datetime, timedelta
from typing import List
import copy
from threading import RLock
from crypto.models.certificate import Certificate
from common.utils import parse_json, to_json_string


class CertificateFromKeyvault(CertificateHandler):

    __secret_uri: str
    __cached_secret: List[Certificate]
    __next_read: datetime
    __auth_uri: str
    __cache_timeout: timedelta
    __lock: RLock

    def __init__(self, secret_uri: str, cache_timeout: timedelta, auth_uri: str):
        self.__secret_uri = secret_uri
        self.__cached_secret = None
        self.__cache_timeout = cache_timeout
        self.__next_read = None
        self.__auth_uri = auth_uri
        self.__lock = RLock()

    def __update_required(self, now):
        return self.__cached_secret is None or self.__next_read is None or now >= self.__next_read

    def get(self) -> List[Certificate]:
        now = datetime.utcnow()
        if self.__update_required(now):
            with self.__lock:
                if self.__update_required(now):
                    res = http_get(self.__auth_uri)
                    access_token = parse_json(res.text)["access_token"]
                    res = request("GET", self.__secret_uri, headers={"Authorization": f'Bearer {access_token}'})
                    value = parse_json(res.text)['value']
                    cert_list = parse_json(value)
                    cert_list = [Certificate.from_json_string(Certificate, to_json_string(x)) for x in cert_list]
                    self.__cached_secret = cert_list
                    self.__next_read = now + self.__cache_timeout
        return copy.deepcopy(self.__cached_secret)