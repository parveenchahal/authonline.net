from logging import Logger
import uuid
from datetime import datetime, timedelta
from models import Session
from storage.storage import Storage
from crypto import Certificate
import base64
import hashlib
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

class SessionHandler():

    __logger: Logger
    __storage: Storage
    __next_validation: timedelta
    __certificate: Certificate

    def __init__(self, logger: Logger, storage: Storage, certificate: Certificate):
        self.__logger = logger
        self.__storage = storage
        self.__next_validation = timedelta(minutes=1)
        self.__certificate = certificate

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
        data = self.__storage.add_or_update(key, session)
        return session

    def get(self, username: str, session_id: str, seq_no: int) -> Session:
        key = self.__generate_key(username, session_id)
        data = self.__storage.get(key)
        return Session(**data)

    def __get_sig(self, data: str) -> str:
        h = hashlib.sha256(data.encode('UTF-8', errors='strict')).hexdigest()
        key = self.__certificate.get()[0]['key']
        key = base64.b64decode(key.encode('UTF-8', errors='strict')).decode('UTF-8', errors='strict')
        encryptor = PKCS1_OAEP.new(RSA.importKey(key))
        enc = encryptor.encrypt(h.encode('UTF-8', errors='strict'))
        return base64.b64encode(enc)

    def sign(self, session: Session) -> str:
        s = session.to_json_string()
        s = s.encode('UTF-8', errors='strict')
        s = base64.b64encode(s)
        base64_encoded = s.decode('UTF-8', errors='strict')
        sig = self.__get_sig(base64_encoded)
        return f'{base64_encoded}.{sig}'



    def delete(self, username: str, session_id: str) -> bool:
        key = self.__generate_key(username, session_id)
        return self.__storage.delete(key)
