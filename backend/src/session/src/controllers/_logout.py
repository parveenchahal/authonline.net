from flask_restful import request
from common import Controller
from common.authonline.session.models import Session
from common.crypto.jwt import JWTHandler
from common import http_responses
from common.http_responses.models import MessageResponseModel
from ..session import SessionHandler, validate_session

class LogoutController(Controller):

    _session_handler: SessionHandler

    def __init__(self, logger, session_handler: SessionHandler):
        super().__init__(logger)
        self._session_handler = session_handler

    @validate_session
    def get(self):
        session_token: str = request.headers['Session']
        session = Session(**(JWTHandler.decode_payload(session_token.split('.')[1])))
        self._session_handler.expires(session.oid, session.sid)
        msg = MessageResponseModel(**{
            "message": "You are successfully logged out."})
        return http_responses.JSONResponse(msg)