from logging import Logger
import uuid
from datetime import datetime, timedelta
from session.models import Session
from storage.storage import Storage
from crypto import RSASignature
from common.utils import encode_base64


class SessionHandler():

    __logger: Logger
    __storage: Storage
    __next_validation: timedelta
    __rsa_signature: RSASignature

    def __init__(self, logger: Logger, storage: Storage, rsa_signature: RSASignature):
        self.__logger = logger
        self.__storage = storage
        self.__next_validation = timedelta(minutes=1)
        self.__rsa_signature = rsa_signature

    def __generate_key(self, username: str, sid: str) -> str:
        key = f"{username}-{sid}"
        key = str(uuid.uuid5(uuid.NAMESPACE_OID, key))
        return key

    def create(self, username: str, resource:str, expiry: timedelta) -> Session:
        now_utc = datetime.utcnow()
        exp = int(datetime.timestamp(now_utc + expiry))

        sid = str(uuid.uuid5(uuid.NAMESPACE_OID, f"{id} + {str(exp)}"))
        next_validation = int(datetime.timestamp(now_utc + self.__next_validation))

        session = Session(
            sid=sid,
            username=username,
            resource=resource,
            expiry=exp,
            next_validation=next_validation,
            seq_num=1
        )
        
        key = self.__generate_key(session.username, session.sid)
        data = self.__storage.add_or_update(key, session.to_dict())
        return Session(**data)

    def get(self, username: str, session_id: str, seq_no: int) -> Session:
        key = self.__generate_key(username, session_id)
        data = self.__storage.get(key)
        return Session(**data)

    def sign(self, session: Session) -> str:
        s = session.to_json_string()
        e_s = encode_base64(s, remove_padding=True)
        header, sig = self.__rsa_signature.get_signature(e_s)
        return f'{header}.{e_s}.{sig}'



    def delete(self, username: str, session_id: str) -> bool:
        key = self.__generate_key(username, session_id)
        return self.__storage.delete(key)
