from logging import Logger
import uuid
from datetime import datetime, timedelta
from common.authonline.session.models import Session
from common.databases.nosql import DatabaseOperations
from common.crypto.jwt import JWTHandler
from common.databases.nosql.models import DatabaseEntryModel
from common import exceptions
from common.utils import dict_to_obj

class SessionHandler():

    _logger: Logger
    _db_op: DatabaseOperations
    _refresh_session_interval: timedelta
    _jwt_handler: JWTHandler
    _force_refresh_before_raf_expiry: timedelta = timedelta(minutes=2)

    def __init__(
        self,
        logger: Logger,
        db_op: DatabaseOperations,
        jwt_handler: JWTHandler,
        refresh_session_interval: timedelta = timedelta(minutes=5)):
        self._logger = logger
        self._db_op = db_op
        self._refresh_session_interval = refresh_session_interval
        self._jwt_handler = jwt_handler
        if refresh_session_interval <= self._force_refresh_before_raf_expiry:
            raise ValueError('refresh_session_interval should be greater than 2 minutes.')

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
        db_entry = DatabaseEntryModel(**{
            'id': sid,
            'partition_key': object_id,
            'data': session.to_dict()
        })
        self._db_op.insert_or_update(db_entry)
        return session
    
    def refresh(self, session: Session) -> Session:
        #
        #TODO: Need to refactor
        #
        db_entry = self._db_op.get(session.sid, session.oid)
        if db_entry is None:
            return None
        s = dict_to_obj(Session, db_entry.data)
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
        db_entry.data = s.to_dict()
        try:
            self._db_op.insert_or_update(db_entry)
        except exceptions.EtagMismatchError:
            db_entry = self._db_op.get(session.sid, session.oid)
            if db_entry is None:
                return None
            s = dict_to_obj(Session, db_entry.data)
            if s.is_expired:
                return None
        return s

    def get(self, object_id: str, session_id: str) -> Session:
        data = self._db_op.get(session_id, object_id)
        if data is not None:
            s = dict_to_obj(Session, data.data)
            if not s.is_expired:
                return s
        return None

    def sign(self, session: Session) -> str:
        signed_session = self._jwt_handler.encode(session.to_dict())
        return signed_session

    def expires(self, object_id: str, session_id: str):
        db_entry = self._db_op.get(session_id, object_id)
        if db_entry is None:
            return
        s = dict_to_obj(Session, db_entry.data)
        s.exp = int(datetime.utcnow().timestamp())
        db_entry.data = s.to_dict()
        db_entry.etag = '*'
        return self._db_op.insert_or_update(db_entry)
