from common.databases.nosql import DatabaseOperations
from .models import UserInfoModel
from requests import request as http_request 
from common.utils import dict_to_obj, parse_json
from common.databases.nosql.models import DatabaseEntryModel
from logging import Logger

class UserInfoHandler(object):

    _logger: Logger
    _db_op: DatabaseOperations
    _google_userinfo_endpoint: str = "https://openidconnect.googleapis.com/v1/userinfo"

    def __init__(self, logger: Logger, db_op: DatabaseOperations):
        self._logger = logger
        self._db_op = db_op

    def get(self, object_id: str, session_id: str) -> UserInfoModel:
        db_entry = self._db_op.get(object_id, 0)
        return dict_to_obj(UserInfoModel, db_entry.data)

    def fetch_and_store_from_google(self, object_id: str, access_token: str):
        res = http_request(
            'GET',
            self._google_userinfo_endpoint,
            headers={"Authorization": f'Bearer {access_token}'})
        info_dict: dict = parse_json(res.text)

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

        db_entry = DatabaseEntryModel(**{
            'id': object_id,
            'partition_key': 0,
            'data': user_info.to_dict(),
            'etag': '*'
        })

        self._db_op.insert_or_update(db_entry)
        