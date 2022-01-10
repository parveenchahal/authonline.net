from logging import Logger
from flask_restful import request
from common import Controller, http_responses, exceptions
from common.session.models import Session
from common.crypto.jwt import JWTHandler
from .. import config
from ..registration import SessionRegistrationHandler
from ..session import validate_session

class SessionRegistrationController(Controller):

    _session_registration_handler: SessionRegistrationHandler

    def __init__(self, logger: Logger, session_registration_handler: SessionRegistrationHandler):
        super().__init__(logger)
        self._session_registration_handler = session_registration_handler

    @validate_session
    def get(self):
        args = request.args
        try:
            session_token = request.headers['Session']
            session = Session(**(JWTHandler.decode_payload(session_token.split('.')[1])))
            if session.app != config.common.AuthonlineClientId:
                raise exceptions.Unauthorized('User should be logged in for authonline.net to use this API.')
            client_id = args.get('client_id', None)
            if client_id is None:
                raise exceptions.MissingParamError('Query param client_id is not provided.')
            reg_details = self._session_registration_handler.get(client_id)
            if reg_details is None:
                raise exceptions.NotFoundError(f'Registration for client_id {client_id} is not found.')
            if session.oid not in reg_details.owners:
                raise exceptions.Unauthorized('You are not authorized to see these registration details.')
            return http_responses.JSONResponse(reg_details)
        except exceptions.MissingParamError as e:
            self._logger.exception(e)
            return http_responses.BadRequestResponse(str(e))
        except exceptions.Unauthorized as e:
            return http_responses.UnauthorizedResponse(str(e))
        except exceptions.NotFoundError as e:
            return http_responses.NotFoundResponse(str(e))
        except Exception as e:
            self._logger.exception(e)
            return http_responses.InternalServerErrorResponse()
