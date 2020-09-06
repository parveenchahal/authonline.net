from common.storage import Storage
from .models import SessionRegistrationDetailsModel

class SessionRegistrationHandler(object):

    _storage: Storage

    def __init__(self, storage: Storage):
        self._storage = storage

    def get(self, client_id: str) -> SessionRegistrationDetailsModel:
        storage_entry = self._storage.get(client_id, 0, SessionRegistrationDetailsModel)
        if storage_entry is not None:
            return storage_entry.data
        return None