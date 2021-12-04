from logging import Logger
import uuid
from datetime import datetime, timedelta
from common.session.models import Session
from common.storage import Storage
from common.crypto.jwt import JWTHandler
from common.storage.models import StorageEntryModel
from common import exceptions
from common.utils import dict_to_obj

class SessionHandler():

    _logger: Logger
    _storage: Storage
    _refresh_session_interval: timedelta
    _jwt_handler: JWTHandler
    _force_refresh_before_raf_expiry: timedelta = timedelta(minutes=1)

    def __init__(
        self,
        logger: Logger,
        storage: Storage,
        jwt_handler: JWTHandler,
        refresh_session_interval: timedelta = timedelta(minutes=5)):
        self._logger = logger
        self._storage = storage
        self._refresh_session_interval = refresh_session_interval
        self._jwt_handler = jwt_handler


    def create(
        self,
        username: str,
        object_id:str,
        app_id:str,
        amr: list,
        resource:str,
        expiry: timedelta) -> Session:
        now_utc = datetime.utcnow()
        exp = int(datetime.timestamp(now_utc + expiry))

        sid = str(uuid.uuid5(uuid.NAMESPACE_OID, f"{id} + {str(exp)}"))
        next_validation = int(datetime.timestamp(now_utc + self._refresh_session_interval))

        session = Session(
            sid=sid,
            amr=amr,
            oid=object_id,
            app=app_id,
            usr=username,
            res=resource,
            exp=exp,
            raf=next_validation,
            sqn=1
        )
        storage_entry = StorageEntryModel(**{
            'id': sid,
            'partition_key': object_id,
            'data': session.to_dict()
        })
        self._storage.add_or_update(storage_entry)
        return session
    
    def refresh(self, session: Session) -> Session:
        #
        #TODO: Need to refactor
        #
        storage_entry = self._storage.get(session.sid, session.oid)
        if storage_entry is None:
            return None
        s = dict_to_obj(Session, storage_entry.data)
        if s.is_expired:
            return None
        if s.sqn - session.sqn > 1:
            self.expires(s.oid, s.sid)
            return None
        if not s.refresh_required and \
            datetime.fromtimestamp(s.raf) - datetime.utcnow() > self._force_refresh_before_raf_expiry:
            return s
        s.sqn = s.sqn + 1
        s.raf = int(datetime.timestamp(datetime.utcnow() + self._refresh_session_interval))
        storage_entry.data = s.to_dict()
        try:
            self._storage.add_or_update(storage_entry)
        except exceptions.EtagMismatchError:
            storage_entry = self._storage.get(session.sid, session.oid)
            if storage_entry is None:
                return None
            s = dict_to_obj(Session, storage_entry.data)
            if s.is_expired:
                return None
        return s

    def get(self, object_id: str, session_id: str) -> Session:
        data = self._storage.get(session_id, object_id)
        if data is not None:
            s = dict_to_obj(Session, data.data)
            if not s.is_expired:
                return s
        return None

    def sign(self, session: Session) -> str:
        signed_session = self._jwt_handler.encode(session.to_dict())
        return signed_session

    def expires(self, object_id: str, session_id: str):
        storage_entry = self._storage.get(session_id, object_id)
        if storage_entry is None:
            return
        s = dict_to_obj(Session, storage_entry.data)
        s.exp = int(datetime.utcnow().timestamp())
        storage_entry.data = s.to_dict()
        storage_entry.etag = '*'
        return self._storage.add_or_update(storage_entry)
