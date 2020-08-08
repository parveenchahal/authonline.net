import os
from oauth2client import client
from oauth2client.client import OAuth2Credentials
import exceptions

class GoogleOauth:

    def get_token_authorization_code(self, auth_code: str, scopes: list, redirect_uri: str) -> dict:
        secret = os.environ['GOOGLE_OAUTH_SECRET_FILE_PATH']
        credentials = client.credentials_from_clientsecrets_and_code(secret, scopes, auth_code, redirect_uri=redirect_uri)
        if credentials:
            return self.__tokens_output(credentials)
        raise exceptions.LoginFailure("Not able to sign in with given code")

    def __tokens_output(self, credentials: OAuth2Credentials) -> dict:
        return {
            'username': credentials.id_token['email'],
            'id_token': credentials.token_response["id_token"],
            'access_token': credentials.token_response["access_token"]
        }
