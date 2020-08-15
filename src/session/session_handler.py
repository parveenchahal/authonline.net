from logging import Logger
import uuid
from datetime import datetime, timedelta
from session.models import Session
from storage.storage import Storage
from crypto.jwt import JWTHandler
from storage.models import StorageEntryModel


class SessionHandler():

    _logger: Logger
    _storage: Storage
    _refresh_session_interval: timedelta
    _jwt_handler: JWTHandler

    def __init__(self, logger: Logger, storage: Storage, jwt_handler: JWTHandler, refresh_session_interval: timedelta = timedelta(minutes=5)):
        self._logger = logger
        self._storage = storage
        self._refresh_session_interval = refresh_session_interval
        self._jwt_handler = jwt_handler

    def __generate_key(self, usr: str, sid: str) -> str:
        key = f"{usr}-{sid}"
        key = str(uuid.uuid5(uuid.NAMESPACE_OID, key))
        return key

    def create(self, username: str, amr: list, resource:str, expiry: timedelta) -> Session:
        now_utc = datetime.utcnow()
        exp = int(datetime.timestamp(now_utc + expiry))

        sid = str(uuid.uuid5(uuid.NAMESPACE_OID, f"{id} + {str(exp)}"))
        next_validation = int(datetime.timestamp(now_utc + self._refresh_session_interval))

        session = Session(
            sid=sid,
            amr=amr,
            usr=username,
            res=resource,
            exp=exp,
            raf=next_validation,
            sqn=1
        )
        key = self.__generate_key(session.usr, session.sid)
        storage_entry = StorageEntryModel(**{
            "key": key,
            "data": session
        })
        self._storage.add_or_update(storage_entry)
        return session
    
    def refresh(self, session: Session) -> Session:
        #
        #TODO: Need to add retires if pre-condition fails
        #
        storage_entry = self._storage.get(self.__generate_key(session.usr, session.sid), Session)
        if storage_entry is None:
            return None
        s: Session = storage_entry.data
        if s.is_expired:
            return None
        if s.sqn - session.sqn > 1:
            self.delete(s.usr, s.sid)
            return None
        if not s.refresh_required:
            return s
        s.sqn = s.sqn + 1
        s.raf = int(datetime.timestamp(datetime.utcnow() + self._refresh_session_interval))
        storage_entry.data = s
        self._storage.add_or_update(storage_entry)
        return s

    def get(self, username: str, session_id: str, seq_no: int) -> Session:
        key = self.__generate_key(username, session_id)
        data = self._storage.get(key, Session)
        if data is not None:
            s = Session(**(data.data))
            if not s.is_expired:
                return s
        return None

    def sign(self, session: Session) -> str:
        signed_session = self._jwt_handler.encode(session.to_dict())
        return signed_session

    def delete(self, username: str, session_id: str) -> bool:
        key = self.__generate_key(username, session_id)
        return self._storage.delete(key)
