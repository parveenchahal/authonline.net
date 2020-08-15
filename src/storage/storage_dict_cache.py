from cachetools import TTLCache, Cache
from storage.storage import Storage
from common.abstract_model import Model
from storage.models import StorageEntryModel
from threading import RLock


class StorageDictCache(Storage):

    __dict: dict
    __lock: RLock

    def __init__(self):
        self.__lock = RLock()
        self.__dict = {}

    def get(self, key: str, model_for_data: Model) -> StorageEntryModel:
        return self.__dict.get(key, None)

    def add_or_update(self, storage_entry: StorageEntryModel):
        with self.__lock:
            self.__dict[storage_entry.key] = storage_entry
    
    def delete(self, key: str):
        self.__dict.pop(key, None)

    