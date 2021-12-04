from common.storage import Storage
from .models import UserInfoModel
from requests import request as http_request 
from common.utils import dict_to_obj, parse_json
from common.storage.models import StorageEntryModel
from logging import Logger

class UserInfoHandler(object):

    _logger: Logger
    _storage: Storage
    _google_userinfo_endpoint: str = "https://openidconnect.googleapis.com/v1/userinfo"

    def __init__(self, logger: Logger, storage: Storage):
        self._logger = logger
        self._storage = storage

    def get(self, object_id: str, session_id: str) -> UserInfoModel:
        storage_entry = self._storage.get(object_id, 0)
        return dict_to_obj(UserInfoModel, storage_entry.data)

    def fetch_and_store_from_google(self, object_id: str, access_token: str):
        res = http_request(
            'GET',
            self._google_userinfo_endpoint,
            headers={"Authorization": f'Bearer {access_token}'})
        info_dict = parse_json(res.text)

        user_info = UserInfoModel(**{
            'object_id': object_id,
            'username': info_dict.get("email", None),
            'name': info_dict.get("name", None),
            'first_name': info_dict.get("given_name", None),
            'last_name': info_dict.get("family_name", None),
            'email': info_dict.get("email", None),
            'email_verified': info_dict.get("email_verified", None),
            'photo_url': info_dict.get("picture", None)
        })

        storage_entry = StorageEntryModel(**{
            'id': object_id,
            'partition_key': 0,
            'data': user_info.to_dict(),
            'etag': '*'
        })

        self._storage.add_or_update(storage_entry)
        