from logging import Logger
import uuid
from datetime import datetime, timedelta
from .models import Session
from storage import Storage
from crypto.jwt import JWTHandler
from storage.models import StorageEntryModel
import exceptions

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


    def create(self, username: str, object_id:str, amr: list, resource:str, expiry: timedelta) -> Session:
        now_utc = datetime.utcnow()
        exp = int(datetime.timestamp(now_utc + expiry))

        sid = str(uuid.uuid5(uuid.NAMESPACE_OID, f"{id} + {str(exp)}"))
        next_validation = int(datetime.timestamp(now_utc + self._refresh_session_interval))

        session = Session(
            sid=sid,
            amr=amr,
            oid=object_id,
            usr=username,
            res=resource,
            exp=exp,
            raf=next_validation,
            sqn=1
        )
        storage_entry = StorageEntryModel(**{
            'id': sid,
            'partition_key': object_id,
            'data': session
        })
        self._storage.add_or_update(storage_entry)
        return session
    
    def refresh(self, session: Session) -> Session:
        #
        #TODO: Need to refactor
        #
        storage_entry = self._storage.get(session.sid, session.oid, Session)
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
        try:
            self._storage.add_or_update(storage_entry)
        except exceptions.AlreadyModified:
            storage_entry = self._storage.get(session.sid, session.oid, Session)
            if storage_entry is None:
                return None
            s: Session = storage_entry.data
            if s.is_expired:
                return None
        return s

    def get(self, object_id: str, session_id: str, seq_no: int) -> Session:
        data = self._storage.get(session_id, object_id, Session)
        if data is not None:
            s = Session(**(data.data))
            if not s.is_expired:
                return s
        return None

    def sign(self, session: Session) -> str:
        signed_session = self._jwt_handler.encode(session.to_dict())
        return signed_session

    def delete(self, object_id: str, session_id: str) -> bool:
        return self._storage.delete(session_id, object_id)
