from flask_restful import request
from datetime import datetime
from common import Controller
from ..session import SessionHandler
from common.session.models import Session
from common.crypto.jwt import JWTHandler
from common import auth_filter
from common import http_responses
from common.http_responses.models import MessageResponseModel

class LogoutController(Controller):

    _session_handler: SessionHandler

    def __init__(self, logger, session_handler: SessionHandler):
        super().__init__(logger)
        self._session_handler = session_handler

    @auth_filter.validate_session
    def get(self):
        session_token = request.headers['Authorization']
        session_token = session_token.split(' ', 1)[1]
        session = Session(**(JWTHandler.decode_payload(session_token.split('.')[1])))
        self._session_handler.expires(session.oid, session.sid)
        msg = MessageResponseModel(**{
            "message": "You are successfully logged out."})
        return http_responses.JSONResponse(msg)