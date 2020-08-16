from datetime import datetime
from crypto.jwt import JWTHandler
from session.models import Session
from session import SessionHandler
import exceptions
from logging import Logger

class SessionValidator(object):

    _logger: Logger
    _jwt_handler: JWTHandler
    _session_handler: SessionHandler

    def __init__(self, logger: Logger, jwt_handler: JWTHandler, session_handler: SessionHandler):
        self._logger = logger
        self._jwt_handler = jwt_handler
        self._session_handler = session_handler

    def _validate_payload(self, session: Session) -> Session:
        if session.is_expired:
            raise exceptions.SessionExpiredError()
        if session.refresh_required:
            session = self._session_handler.refresh(session)
            if session is not None:
                return session
            raise exceptions.SessionExpiredError()
        return None

    def validate(self, session_string: str) -> (str, int):
        payload = self._jwt_handler.decode(session_string, verify_signature=False)
        refreshed_session = self._validate_payload(Session(**payload))
        if refreshed_session is not None:
            signed_session = self._session_handler.sign(refreshed_session)
            return signed_session, refreshed_session.exp
        return None, None