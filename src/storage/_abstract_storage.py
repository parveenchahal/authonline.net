from abc import abstractmethod
from .models import StorageEntryModel
from common.abstract_model import Model
from typing import List

class Storage():
    @abstractmethod
    def get(self, id: str, partition_key: str, model_for_data: Model) -> StorageEntryModel:
        raise NotImplementedError()
    
    @abstractmethod
    def add(self, storage_entry: StorageEntryModel):
        raise NotImplementedError()

    @abstractmethod
    def update(self, storage_entry: StorageEntryModel):
        raise NotImplementedError()

    @abstractmethod
    def query(self, query_dict: dict) -> List[StorageEntryModel]:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: str, partition_key: str) -> bool:
        raise NotImplementedError()
