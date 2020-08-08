from crypto.certificate import Certificate
from requests import get as http_get, request
from datetime import datetime, timedelta
from typing import List
import json
import copy
from threading import RLock


class CertificateFromKeyvault(Certificate):

    __secret_uri: str
    __cached_secret: List[dict]
    __last_read: datetime
    __auth_uri: str
    __expires_in: timedelta
    __lock: RLock

    def __init__(self, secret_uri: str, cache_timeout: timedelta, auth_uri: str):
        self.__secret_uri = secret_uri
        self.__cached_secret = None
        self.__last_read = None
        self.__auth_uri = auth_uri
        self.__lock = RLock()

    def __update_required(self, now):
        return self.__cached_secret is None or self.__last_read is None or now >= self.__last_read

    def get(self) -> List[dict]:
        now = datetime.utcnow()
        if self.__update_required(now):
            with self.__lock:
                if self.__update_required(now):
                    res = http_get(self.__auth_uri)
                    access_token = json.loads(res.text)["access_token"]
                    res = request("GET", self.__secret_uri, headers={"Authorization": f'Bearer {access_token}'})
                    self.__cached_secret = json.loads(json.loads(res.text)['value'])
                    self.__last_read = now
        return copy.deepcopy(self.__cached_secret)