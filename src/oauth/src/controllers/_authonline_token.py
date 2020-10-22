from logging import Logger
from typing import Type
from flask_restful import request
from common import Controller
from common.crypto.jwt import JWTHandler
from common.session.models import Session
from ..access_token_payload import generate_access_token_payload_using_session as _generate_access_token_payload_using_session
from common import auth_filter
from common.utils import to_json_string
from common import http_responses
from common.http_responses.models import Oath2TokenResponse
from .. import config
from common.storage import Storage
from ..roles.models import RoleAssignmentModel
from ..registration.models import Oauth2RegistrationModel

class AuthOnlineTokenController(Controller):

    _jwt_handler: JWTHandler
    _oauth2_registration_storage: Storage
    _role_assignment_storage: Storage

    def __init__(self, logger: Logger, oauth2_registration_storage: Storage, role_assignment_storage: Storage, jwt_handler: JWTHandler):
        super().__init__(logger)
        self._oauth2_registration_storage = oauth2_registration_storage
        self._role_assignment_storage = role_assignment_storage
        self._jwt_handler = jwt_handler

    @auth_filter.validate_session
    def get(self):
        session_token = request.headers['Authorization']
        session_token = session_token.split(' ', 1)[1]
        session = Session(**(JWTHandler.decode_payload(session_token.split('.')[1])))
        storage_entry = self._role_assignment_storage.get(session.oid, session.app, RoleAssignmentModel)
        role_assignment = RoleAssignmentModel(storage_entry.data)

        storage_entry = self._oauth2_registration_storage.get(session.app, 0, Oauth2RegistrationModel)
        oauth2_registration: Oauth2RegistrationModel = storage_entry.data
        scp = oauth2_registration.roles.get(role_assignment.role_name, role_assignment.role_name)

        payload = _generate_access_token_payload_using_session(session, config.common.BaseUrl, scp)
        access_token = self._jwt_handler.encode(payload.to_dict())
        token_response = Oath2TokenResponse(**{
            "access_token": access_token
        })
        return http_responses.JSONResponse(token_response)
