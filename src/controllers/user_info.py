from flask_restful import request
from session.models import Session
from .abstract_controller import Controller
from user_info import UserInfoHandler
from crypto.jwt import JWTHandler
from http_responses import JSONResponse
import auth_filter

class UserInfo(Controller):

    _userinfo_handler: UserInfoHandler

    def __init__(self, logger, userinfo_handler: UserInfoHandler):
        super().__init__(logger)
        self._userinfo_handler = userinfo_handler

    @auth_filter.validate_session
    def get(self):
        cookie: str = request.cookies.get("session")
        session = Session(**(JWTHandler.decode_payload(cookie.split('.')[1])))
        user_info = self._userinfo_handler.get(session.usr, session.sid)
        return JSONResponse(user_info)