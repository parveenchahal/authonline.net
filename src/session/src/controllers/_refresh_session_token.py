from flask_restful import request
from ..session import SessionHandler
from common.session.models import Session
from common.crypto.jwt import JWTHandler
from common import Controller
from common import auth_filter
from common import http_responses
from common.http_responses.models import SessionTokenResponse

class RefreshSessionTokenController(Controller):

    _session_handler: SessionHandler

    def __init__(self, logger, session_handler: SessionHandler):
        super().__init__(logger)
        self._session_handler = session_handler

    @auth_filter.validate_session(ignore_refresh_expiry=True)
    def get(self):
        session_token = request.headers['Authorization']
        session_token = session_token.split(' ', 1)[1]
        session = Session(**(JWTHandler.decode_payload(session_token.split('.')[1])))
        session = self._session_handler.refresh(session)
        if session is None:
            return http_responses.UnauthorizedResponse('Session can not be refreshed.')
        refreshed_session_token = self._session_handler.sign(session)
        return http_responses.JSONResponse(SessionTokenResponse(**{
            'session': refreshed_session_token
        }))