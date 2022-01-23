from common.databases.nosql import DatabaseOperations
from common.utils import dict_to_obj
from .models import UserModel
import uuid
from datetime import datetime
from common.databases.nosql.models import DatabaseEntryModel


class UserHandler(object):

    _dp_op: DatabaseOperations

    def __init__(self, dp_op: DatabaseOperations):
        self._dp_op = dp_op

    def _create(self, username: str, auth_method: str):
        object_id = str(uuid.uuid5(uuid.NAMESPACE_OID, f'{username}-{datetime.utcnow()}'))
        user = UserModel(**{
            'username': username,
            'object_id': object_id,
            'auth_method': auth_method,
        })
        db_entry = DatabaseEntryModel(**{
            'id': username,
            'partition_key': 0,
            'data': user.to_dict(),
            'etag': "*"
        })
        self._dp_op.insert_or_update(db_entry)

    def get_or_create(self, username: str, auth_method: str) -> UserModel:
        user = None
        user = self._dp_op.get(username, 0)
        if user is not None:
            return dict_to_obj(UserModel, user.data)
        self._create(username, auth_method)
        user = self._dp_op.get(username, 0)
        if user is None:
            # TODO: raise exception
            pass
        data = user.data
        user = dict_to_obj(UserModel, data)
        return user
        