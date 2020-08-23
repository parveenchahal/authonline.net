'''from cachetools import TTLCache, Cache
from storage import Storage
from common.abstract_model import Model
from .models import StorageEntryModel
from threading import RLock


class InMemoryDictStorage(Storage):

    _dict: dict
    _lock: RLock

    def __init__(self):
        self._lock = RLock()
        self._dict = {}

    def get(self, key: str, model_for_data: Model) -> StorageEntryModel:
        return self._dict.get(key, None)

    def add_or_update(self, storage_entry: StorageEntryModel):
        with self._lock:
            self._dict[storage_entry.key] = storage_entry
    
    def delete(self, key: str):
        self._dict.pop(key, None)

    '''