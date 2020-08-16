from .abstract_controller import Controller
import config
from flask import redirect
from flask_restful import request
from logging import Logger
from google_oauth import GoogleOauth
import http_responses
import exceptions
from session import SessionHandler
from urllib.parse import urlparse, ParseResult
from common.utils import parse_json, to_json_string
from user_info import UserInfoHandler


class GoogleSignInController(Controller):

    _google_oauth: GoogleOauth
    _session_handler: SessionHandler
    _userinfo_handler: UserInfoHandler

    def __init__(self, logger: Logger, google_oauth: GoogleOauth, session_handler: SessionHandler, userinfo_handler: UserInfoHandler):
        super().__init__(logger)
        self._google_oauth = google_oauth
        self._session_handler = session_handler
        self._userinfo_handler = userinfo_handler

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

    def _auth(self, args: dict):
        self._validate_auth_request(args)
        code = args.get("code")
        scopes = args.get("scope")
        state = parse_json(args.get("state"))

        resource = state.get('resource')
        redirect_uri = state.get('redirect_uri')
        user_state_param = state.get('state')

        credentials = self._google_oauth.get_token_using_authorization_code(code, scopes, config.google_token_signin.RedirectUri)

        username = credentials['username']
        session = self._session_handler.create(username, ["Google login",], resource, config.common.SessionExpiry)
        self._userinfo_handler.fetch_and_store_from_google(session.usr, session.sid, credentials['access_token'])

        signed_session = self._session_handler.sign(session)
        return redirect(f'{redirect_uri}?state={user_state_param}&session={signed_session}', code=302)
        

    def get(self, type: str = ""):
        try:
            args = request.args
            if "auth".__eq__(type):
                return self._auth(args)
            elif "".__eq__(type) or "/".__eq__(type):
                login_url = config.LoginUrl
                login_url = f'{login_url}&state={to_json_string(args)}'
                return redirect(login_url, code=302)
            else:
                return http_responses.NotFoundResponse()
        except exceptions.LoginFailureError as e:
            self._logger.exception(e)
            return http_responses.UnauthorizedResponse()
        except exceptions.MissingParamError as e:
            self._logger.exception(e)
            return http_responses.BadRequestResponse()
        except Exception as e:
            self._logger.exception(e)
            return http_responses.InternalServerErrorResponse()
