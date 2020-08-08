from dataclasses import dataclass
from dataclasses_json import dataclass_json
import copy
import json
from datetime import datetime

class Session:
    sid: str
    username: str
    expiry: int
    next_validation:datetime
    seq_num: int
    etag: str = "*"

    def __init__(self, sid: str, username: str, expiry: int, next_validation: datetime, seq_num: int, etag: str = "*"):
        self.sid = sid
        self.username = username
        self.expiry = expiry
        self.next_validation = next_validation
        self.seq_num = seq_num
        self.etag = etag
    
    def to_dict(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        d.pop("etag", None)
        return d

    def to_json_string(self) -> str:
        d = self.to_dict()
        return json.dumps(d)

    @staticmethod
    def from_json_string(json_data: str):
        d = dict(json.loads(json_data))
        s = Session(**d)
        return s

    @property
    def is_valid(self) -> bool:
        now = int(datetime.timestamp(datetime.utcnow()))
        return now < self.expiry
