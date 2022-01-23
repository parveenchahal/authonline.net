from flask_restful import request
from common.authonline.session.models import Session
from common.crypto.jwt import JWTHandler
from common import Controller
from common import http_responses
from common.http_responses.models import SessionTokenResponse
from ..session import SessionHandler, validate_session

class RefreshSessionTokenController(Controller):

    _session_handler: SessionHandler

    def __init__(self, logger, session_handler: SessionHandler):
        super().__init__(logger)
        self._session_handler = session_handler

    @validate_session(ignore_refresh_expiry=True)
    def get(self):
        session_token = request.headers['Session']
        session = Session(**(JWTHandler.decode_payload(session_token.split('.')[1])))
        session = self._session_handler.refresh(session)
        if session is None:
            return http_responses.UnauthorizedResponse('Session can not be refreshed.')
        refreshed_session_token = self._session_handler.sign(session)
        return http_responses.JSONResponse(SessionTokenResponse(**{
            'session': refreshed_session_token
        }))