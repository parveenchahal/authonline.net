from common.storage import Storage
from common.utils import dict_to_obj
from .models import SessionRegistrationDetailsModel

class SessionRegistrationHandler(object):

    _storage: Storage

    def __init__(self, storage: Storage):
        self._storage = storage

    def get(self, client_id: str) -> SessionRegistrationDetailsModel:
        storage_entry = self._storage.get(client_id, 0)
        if storage_entry is not None:
            return dict_to_obj(SessionRegistrationDetailsModel, storage_entry.data)
        return None