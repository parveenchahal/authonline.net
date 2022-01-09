from logging import Logger
from flask import redirect
from flask_restful import request
from common import http_responses, exceptions
from common.utils import parse_json, to_json_string
from session.src.registration.models import SessionRegistrationDetailsModel
from . import Controller
from .. import config
from ..google_oauth import GoogleOauth
from ..session import SessionHandler
from ..user_info import UserInfoHandler
from ..user import UserHandler
from ..registration import SessionRegistrationHandler


class GoogleSignInController(Controller):

    AUTH_METHOD: str = 'GoogleSignIn'
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

    def _validate_with_registered_details(self, data: dict, registered_details: SessionRegistrationDetailsModel):
        redirect_uri = data.get('redirect_uri')
        if not redirect_uri in registered_details.redirect_uris:
            raise exceptions.IncorrectValue(
                f'Redirect uri {redirect_uri} is not registered for given client_id.')

    def _auth(self, args: dict):
        self._validate_auth_request(args)

        state: dict = parse_json(args.get("state"))
        client_id = state.get('client_id')

        registered_details = self._session_registration_handler.get(client_id)
        if registered_details is None:
            raise exceptions.IncorrectValue(f'Client id {client_id} not found.')

        self._validate_with_registered_details(state, registered_details)

        code = args.get("code")
        scopes = args.get("scope")
        credentials = self._google_oauth.get_token_using_authorization_code(code, scopes, config.google_token_signin.RedirectUri)

        username = credentials['username']

        user = self._user_handler.get_or_create(username, self.AUTH_METHOD)
        self._userinfo_handler.fetch_and_store_from_google(user.object_id, credentials['access_token'])

        session = self._session_handler.create(username, user.object_id, client_id, ["GoogleSignIn",], registered_details.resource, config.common.SessionExpiry)

        signed_session = self._session_handler.sign(session)
        redirect_uri = state.get('redirect_uri')
        user_state_param = state.get('state')
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
