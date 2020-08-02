from controllers.abstract_controller import Controller
import config.google_token_signin as config
from flask import redirect
from flask_restful import request
from google_oauth import GoogleOauth


class GoogleSignInController(Controller):

    __google_oauth: GoogleOauth

    def __init__(self, google_oauth:GoogleOauth=None):
        self.__google_oauth = google_oauth

    def __auth(self, args:dict):
        code = args.get("code", None)
        login_success = False    
        if code is not None:
            scopes = args.get("scope", None)
            if scopes is not None:
                scopes = scopes.split(" ")
            else:
                return None, 400
            login_success = self.__google_oauth.get_token_authorization_code(code, scopes, config.RedirectUri)
        else:
            return None, 400
        if login_success:
            return login_success, 200
        else:
            return None, 401

    def __token(self, id:str):
        return self.__google_oauth.get_silent_token(id), 200


    def get(self, type:str=""):
        args = request.args
        if "auth".__eq__(type):
            return self.__auth(args)
        elif "token".__eq__(type):
            return self.__token(args.get("email", None))
        elif "".__eq__(type) or "/".__eq__(type):
            return redirect(config.LoginUrl, code=302)
        else:
            return None, 404
