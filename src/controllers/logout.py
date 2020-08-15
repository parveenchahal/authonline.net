from flask_restful import request
from datetime import datetime
from controllers.abstract_controller import Controller
from session import SessionHandler
from session.models import Session
from crypto.jwt import JWTHandler
import auth_filter

class Logout(Controller):

    _session_handler: SessionHandler

    def __init__(self, logger, session_handler: SessionHandler):
        super().__init__(logger)
        self._session_handler = session_handler

    @auth_filter.validate_session(set_cookie_for_refreshed_session=False)
    def get(self):
        cookie: str = request.cookies.get("session")
        session = Session(**(JWTHandler.decode_payload(cookie.split('.')[1])))
        self._session_handler.delete(session.usr, session.sid)
        res = self._json_response({"message": "You are successfully logged out."})
        res.set_cookie("session", "", expires=datetime.utcnow())
        return res