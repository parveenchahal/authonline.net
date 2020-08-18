from flask_restful import request
from datetime import datetime
from ._abstract_controller import Controller
from session import SessionHandler
from session.models import Session
from crypto.jwt import JWTHandler
import auth_filter
import http_responses
from http_responses.models import MessageResponseModel

class LogoutController(Controller):

    _session_handler: SessionHandler

    def __init__(self, logger, session_handler: SessionHandler):
        super().__init__(logger)
        self._session_handler = session_handler

    @auth_filter.validate_session(set_cookie_for_refreshed_session=False)
    def get(self):
        cookie: str = request.cookies.get("session")
        session = Session(**(JWTHandler.decode_payload(cookie.split('.')[1])))
        self._session_handler.delete(session.usr, session.sid)
        msg = MessageResponseModel(**{
            "message": "You are successfully logged out."})
        res = http_responses.JSONResponse(msg)
        res.set_cookie("session", "", expires=datetime.utcnow())
        return res