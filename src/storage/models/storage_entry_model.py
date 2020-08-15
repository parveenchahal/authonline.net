from common.abstract_model import Model
from dataclasses import dataclass

@dataclass
class StorageEntryModel(Model):
    key: str
    data: Model
    etag: str = "*"