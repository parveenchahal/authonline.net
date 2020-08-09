from logging import Logger
from flask_restful import request
from controllers.abstract_controller import Controller
from crypto import JWTTokenHandler
from common.utils import decode_base64
from session.models import Session


class AuthOnlineToken(Controller):

    __jwt_token_handler: JWTTokenHandler

    def __init__(self, logger: Logger, jwt_token_handler: JWTTokenHandler):
        super().__init__(logger)
        self.__jwt_token_handler = jwt_token_handler

    def __generate_payload_using_session(self, session: Session, remote_addr: str = None) -> dict:
        token_payload = {
            'aud': session.resource,
            'scp': 'user_impersonation',
            'sub': session.sid,
            'username': session.username,
            'amr': session.amr,
        }
        if remote_addr is not None:
            token_payload['remote_addr'] = remote_addr
        return token_payload

    def get(self):
        remote_addr = request.remote_addr
        cookie: str = request.cookies.get("session")
        session = Session.from_json_string(Session, decode_base64(cookie.split('.')[1]))
        self.__jwt_token_handler.get(self.__generate_payload_using_session(session, remote_addr))