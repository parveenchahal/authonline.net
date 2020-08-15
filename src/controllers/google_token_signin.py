from controllers.abstract_controller import Controller
import config.google_token_signin as config
from flask import redirect
from flask_restful import request
from logging import Logger
from google_oauth import GoogleOauth
from error_responses import Unauthorized, BadRequest, NotFound, InternalServerError
import exceptions
from session import SessionHandler
from urllib.parse import urlparse, ParseResult
from common.utils import parse_json, to_json_string

class GoogleSignInController(Controller):

    __google_oauth: GoogleOauth
    __session_handler: SessionHandler

    def __init__(self, logger: Logger, google_oauth: GoogleOauth, session_handler: SessionHandler):
        super().__init__(logger)
        self.__google_oauth = google_oauth
        self.__session_handler = session_handler

    def __validate_auth_request(self, args: dict):
        code = args.get("code", None)
        if code is None:
            raise exceptions.MissingParamError("code is missing")
        scopes = args.get("scope", None)
        if scopes is None:
            raise exceptions.MissingParamError("scopes is missing")
        state = args.get("state", None)
        if state is None:
            raise exceptions.MissingParamError("state is missing")

    def __auth(self, args: dict):
        self.__validate_auth_request(args)
        code = args.get("code")
        scopes = args.get("scope")
        state = parse_json(args.get("state"))

        resource = state.get('resource')
        redirect_uri = state.get('redirect_uri')
        user_state_param = state.get('state')

        credentials = self.__google_oauth.get_token_authorization_code(code, scopes, config.RedirectUri)
        username = credentials['username']
        session = self.__session_handler.create(username, ["Google login",], resource, config.common.SessionExpiry)
        signed_session = self.__session_handler.sign(session)
        return redirect(f'{redirect_uri}?state={user_state_param}&session={signed_session}', code=302)
        

    def get(self, type: str = ""):
        try:
            args = request.args
            if "auth".__eq__(type):
                return self.__auth(args)
            elif "".__eq__(type) or "/".__eq__(type):
                login_url = config.LoginUrl
                login_url = f'{login_url}&state={to_json_string(args)}'
                return redirect(login_url, code=302)
            else:
                return NotFound()
        except exceptions.LoginFailureError as e:
            self._logger.exception(e)
            return Unauthorized()
        except exceptions.MissingParamError as e:
            self._logger.exception(e)
            return BadRequest()
        except Exception as e:
            self._logger.exception(e)
            return InternalServerError()
