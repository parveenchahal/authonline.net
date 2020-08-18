from abc import abstractmethod
from .models import StorageEntryModel
from common.abstract_model import Model

class Storage():
    @abstractmethod
    def get(self, key: str, model_for_data: Model) -> StorageEntryModel:
        raise NotImplementedError()
    
    @abstractmethod
    def add_or_update(self, storage_entry: StorageEntryModel):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, key: str) -> bool:
        raise NotImplementedError()
