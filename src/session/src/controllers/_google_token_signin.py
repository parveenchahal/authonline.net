from . import Controller
from .. import config
from flask import redirect
from flask_restful import request
from logging import Logger
from ..google_oauth import GoogleOauth
from common import http_responses, exceptions
from ..session import SessionHandler
from urllib.parse import urlparse, ParseResult
from common.utils import parse_json, to_json_string
from ..user_info import UserInfoHandler
from ..user import UserHandler
from ..registration import SessionRegistrationHandler
from ..registration.models import SessionRegistrationDetailsModel


class GoogleSignInController(Controller):

    _google_oauth: GoogleOauth
    _session_handler: SessionHandler
    _userinfo_handler: UserInfoHandler
    _user_handler: UserHandler
    _session_registration_handler: SessionRegistrationHandler

    def __init__(self,
        logger: Logger,
        google_oauth: GoogleOauth,
        session_handler: SessionHandler,
        user_handler: UserHandler,
        userinfo_handler: UserInfoHandler,
        session_registration_handler: SessionRegistrationHandler):
        super().__init__(logger)
        self._google_oauth = google_oauth
        self._session_handler = session_handler
        self._userinfo_handler = userinfo_handler
        self._user_handler = user_handler
        self._session_registration_handler = session_registration_handler

    def _validate_auth_request(self, args: dict):
        code = args.get("code", None)
        if code is None:
            raise exceptions.MissingParamError("code is missing")
        scopes = args.get("scope", None)
        if scopes is None:
            raise exceptions.MissingParamError("scopes is missing")
        state = args.get("state", None)
        if state is None:
            raise exceptions.MissingParamError("state is missing")

    def _validate_with_registered_details(self, data):
        client_id = data.get('client_id')
        resource = data.get('resource')
        redirect_uri = data.get('redirect_uri')

        registered_details = self._session_registration_handler.get(client_id)

        if registered_details is None:
            raise exceptions.IncorrectValue(f'Client id {client_id} not found.')

        if resource not in registered_details.resources:
            raise exceptions.IncorrectValue(f'Resource {resource} is not registered for given client_id.')
        
        if not redirect_uri in registered_details.redirect_uris:
            raise exceptions.IncorrectValue(f'Redirect uri {redirect_uri} is not registered for given client_id.')

    def _auth(self, args: dict):
        self._validate_auth_request(args)
        code = args.get("code")
        scopes = args.get("scope")
        state = parse_json(args.get("state"))

        self._validate_with_registered_details(state)

        resource = state.get('resource')
        redirect_uri = state.get('redirect_uri')
        client_id = state.get('client_id')

        user_state_param = state.get('state')

        credentials = self._google_oauth.get_token_using_authorization_code(code, scopes, config.google_token_signin.RedirectUri)

        username = credentials['username']

        user = self._user_handler.get_or_create(username, 'GoogleSignIn')

        session = self._session_handler.create(username, user.object_id, client_id, ["GoogleSignIn",], resource, config.common.SessionExpiry)
        self._userinfo_handler.fetch_and_store_from_google(user.object_id, session.sid, credentials['access_token'])

        signed_session = self._session_handler.sign(session)
        return redirect(f'{redirect_uri}?state={user_state_param}&session={signed_session}', code=302)
        

    def get(self, type: str = ""):
        try:
            args = request.args
            if "auth".__eq__(type):
                return self._auth(args)
            elif "".__eq__(type) or "/".__eq__(type):
                login_url = config.google_token_signin.LoginUrl
                login_url = f'{login_url}&state={to_json_string(args)}'
                return redirect(login_url, code=302)
            else:
                return http_responses.NotFoundResponse()
        except exceptions.LoginFailureError as e:
            self._logger.exception(e)
            return http_responses.UnauthorizedResponse(str(e))
        except (exceptions.MissingParamError, exceptions.IncorrectValue) as e:
            self._logger.exception(e)
            return http_responses.BadRequestResponse(str(e))
        except Exception as e:
            self._logger.exception(e)
            return http_responses.InternalServerErrorResponse()
