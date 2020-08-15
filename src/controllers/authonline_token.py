from logging import Logger
from flask_restful import request
from controllers.abstract_controller import Controller
from crypto.jwt import JWTHandler
from session.models import Session
from access_token_payload import generate_access_token_payload_using_session as _generate_access_token_payload_using_session
import auth_filter
from common.utils import to_json_string

class AuthOnlineToken(Controller):

    _jwt_handler: JWTHandler

    def __init__(self, logger: Logger, jwt_handler: JWTHandler):
        super().__init__(logger)
        self._jwt_handler = jwt_handler

    @auth_filter.validate_session
    def get(self):
        remote_addr = request.remote_addr
        cookie: str = request.cookies.get("session")
        session = Session(**(JWTHandler.decode_payload(cookie.split('.')[1])))
        payload = _generate_access_token_payload_using_session(session, remote_addr)
        credentials = self._jwt_handler.encode(payload.to_dict())
        return self._json_response({'access_token': credentials})
