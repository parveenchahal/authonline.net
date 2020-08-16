from storage import Storage
from .models import UserInfoModel
from requests import request as http_request 
from common.utils import parse_json
from storage.models import StorageEntryModel
from logging import Logger

class UserInfoHandler(object):

    _logger: Logger
    _storage: Storage
    _google_userinfo_endpoint: str = "https://openidconnect.googleapis.com/v1/userinfo"

    def __init__(self, logger: Logger, storage: Storage):
        self._logger = logger
        self._storage = storage

    @staticmethod
    def _generate_key(username: str, session_id: str):
        return f'{username}-{session_id}'

    def get(self, username: str, session_id: str) -> UserInfoModel:
        key = UserInfoHandler._generate_key(username, session_id)
        storage_entry = self._storage.get(key, UserInfoModel)
        return storage_entry.data

    def fetch_and_store_from_google(self, username: str, session_id: str, access_token: str):
        res = http_request('GET', self._google_userinfo_endpoint, headers={"Authorization": f'Bearer {access_token}'})
        info_dict = parse_json(res.text)
        user_info = UserInfoModel()
        
        user_info.username = info_dict.get("email", None)
        user_info.name = info_dict.get("name", None)
        user_info.first_name = info_dict.get("given_name", None)
        user_info.last_name = info_dict.get("family_name", None)
        user_info.email = info_dict.get("email", None)
        user_info.email_verified = info_dict.get("email_verified", None)
        user_info.photo_url = info_dict.get("picture", None)

        storage_entry = StorageEntryModel(**{
            'key': UserInfoHandler._generate_key(username, session_id),
            'data': user_info,
            'etag': '*'
        })

        self._storage.add_or_update(storage_entry)
        