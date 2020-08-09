from dataclasses import dataclass
from dataclasses_json import dataclass_json
import copy
from datetime import datetime
from common.abstract_model import Model
from dataclasses import dataclass


@dataclass
class Session(Model):
    sid: str
    amr: list
    username: str
    resource: str
    expiry: int
    next_validation: int
    seq_num: int
    etag: str = "*"
    
    def to_dict(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        d.pop("etag", None)
        return d

    @property
    def is_valid(self) -> bool:
        now = int(datetime.timestamp(datetime.utcnow()))
        return now < self.expiry
