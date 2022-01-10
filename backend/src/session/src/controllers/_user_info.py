from flask_restful import request
from common.session.models import Session
from common import Controller
from common.crypto.jwt import JWTHandler
from common.http_responses import JSONResponse
from ..user_info import UserInfoHandler
from ..session import validate_session

class UserInfoController(Controller):

    _userinfo_handler: UserInfoHandler

    def __init__(self, logger, userinfo_handler: UserInfoHandler):
        super().__init__(logger)
        self._userinfo_handler = userinfo_handler

    @validate_session
    def get(self):
        session_token = request.headers['Session']
        session = Session(**(JWTHandler.decode_payload(session_token.split('.')[1])))
        user_info = self._userinfo_handler.get(session.oid, session.sid)
        return JSONResponse(user_info)