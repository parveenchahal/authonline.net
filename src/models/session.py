from dataclasses import dataclass
from dataclasses_json import dataclass_json
import json
from datetime import datetime

class Session:
    session_id: str
    username: str
    expiry: datetime
    next_validation: datetime
    seq_num: int
    etag: str = "*"

    def __init__(self, session_id: str, username: str, expiry: datetime, next_validation: datetime, seq_num: int, etag: str = "*"):
        self.session_id = session_id
        self.username = username
        self.expiry = expiry
        self.next_validation = next_validation
        self.seq_num = seq_num
        self.etag = etag

    @property
    def is_valid(self) -> bool:
        now = datetime.utcnow()
        return now < self.expiry
