from uuid import UUID
from datetime import datetime, timedelta
from models import Session
from storage.storage import Storage

class SessionHandler():

    __storage: Storage
    __next_validation: timedelta

    def __init__(self, storage: Storage):
        self.__storage = storage
        self.__next_validation = timedelta(minutes=1)

    def __generate_key(self, username: str, session_id: str) -> str:
        return f"{session.username}-{session.session_id}"

    def create(self, username: str, expiry_timedelta: timedelta) -> Session:
        now_utc = datetime.utcnow()
        sid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{id} + {str(now_utc)}"))
        expiry = now_utc + expiry_timedelta
        next_validation = now_utc + self.__next_validation
        session = Session(
            session_id=sid,
            username=username,
            expiry=expiry,
            next_validation=next_validation,
            seq_num=1
        )
        key = self.__generate_key(session.username, session.session_id)
        data = self.__storage.add_or_update(key, session)
        return Session(**data)

    def get(self, username: str, session_id: str) -> Session:
        key = self.__generate_key(username, session_id)
        data = self.__storage.get(key)
        return Session(**data)

    def delete(self, username: str, session_id: str) -> bool:
        key = self.__generate_key(username, session_id)
        return self.__storage.delete(key)
