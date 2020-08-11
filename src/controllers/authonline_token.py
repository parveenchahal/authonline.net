from logging import Logger
from flask_restful import request
from controllers.abstract_controller import Controller
from crypto import JWTTokenHandler
from session.models import Session
from access_token_payload import generate_access_token_payload_using_session as _generate_access_token_payload_using_session

class AuthOnlineToken(Controller):

    __jwt_token_handler: JWTTokenHandler

    def __init__(self, logger: Logger, jwt_token_handler: JWTTokenHandler):
        super().__init__(logger)
        self.__jwt_token_handler = jwt_token_handler        

    def get(self):
        remote_addr = request.remote_addr
        cookie: str = request.cookies.get("session")
        session = Session.from_json_string(Session, JWTTokenHandler.decode_payload(cookie.split('.')[1]))
        payload = _generate_access_token_payload_using_session(session, remote_addr)
        credentials = self.__jwt_token_handler.sign(payload.to_dict())
        return credentials, 200
