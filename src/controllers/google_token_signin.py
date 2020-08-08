from controllers.abstract_controller import Controller
import config.google_token_signin as config
from flask import redirect
from flask_restful import request
from logging import Logger
from google_oauth import GoogleOauth
from error_responses import Unauthorized, BadRequest, NotFound, InternalServerError
import exceptions
from session import SessionHandler


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
            raise exceptions.MissingParam("code is missing")
        scopes = args.get("scope", None)
        if scopes is None:
            raise exceptions.MissingParam("scopes is missing")

    def __auth(self, args: dict):
        self.__validate_auth_request(args)
        code = args.get("code", None)
        scopes = args.get("scope", None)
        tokens = self.__google_oauth.get_token_authorization_code(code, scopes, config.RedirectUri)
        id_token = tokens['id_token']

        

    def get(self, type: str = ""):
        try:
            args = request.args
            if "auth".__eq__(type):
                return self.__auth(args)
            elif "".__eq__(type) or "/".__eq__(type):
                return redirect(config.LoginUrl, code=302)
            else:
                return NotFound()
        except exceptions.LoginFailure as e:
            self._logger.exception(e)
            return Unauthorized()
        except exceptions.MissingParam as e:
            self._logger.exception(e)
            return BadRequest()
        except Exception as e:
            self._logger.exception(e)
            return InternalServerError()
