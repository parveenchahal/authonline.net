from logging import Logger
from flask_restful import request
from ._abstract_controller import Controller
from crypto.jwt import JWTHandler
from session.models import Session
from access_token_payload import generate_access_token_payload_using_session as _generate_access_token_payload_using_session
import auth_filter
from common.utils import to_json_string
import http_responses
from http_responses.models import Oath2TokenResponse

class AuthOnlineTokenController(Controller):

    _jwt_handler: JWTHandler

    def __init__(self, logger: Logger, jwt_handler: JWTHandler):
        super().__init__(logger)
        self._jwt_handler = jwt_handler

    @auth_filter.validate_session
    def get(self):
        cookie: str = request.cookies.get("session")
        session = Session(**(JWTHandler.decode_payload(cookie.split('.')[1])))
        payload = _generate_access_token_payload_using_session(session)
        access_token = self._jwt_handler.encode(payload.to_dict())
        token_response = Oath2TokenResponse(**{
            "access_token": access_token
        })
        return http_responses.JSONResponse(token_response)
