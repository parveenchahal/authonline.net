from storage import Storage
from .models import UserModel
import uuid
from datetime import datetime
from storage.models import StorageEntryModel


class UserHandler(object):

    _storage: Storage

    def __init__(self, storage: Storage):
        self._storage = storage

    def _create(self, username: str, auth_method: str):
        object_id = str(uuid.uuid5(uuid.NAMESPACE_OID, f'{username}-{datetime.utcnow()}'))
        user = UserModel(**{
            'username': username,
            'object_id': object_id,
            'auth_method': auth_method,
        })
        storage_entry: StorageEntryModel = StorageEntryModel(**{
            'id': username,
            'partition_key': 0,
            'data': user,
            'etag': "*"
        })
        self._storage.add_or_update(storage_entry)

    def get_or_create(self, username: str, auth_method: str) -> UserModel:
        user = None
        user: StorageEntryModel = self._storage.get(username, 0, UserModel)
        if user is not None:
            return user.data
        self._create(username, auth_method)
        user = self._storage.get(username, 0, UserModel).data
        return user
        