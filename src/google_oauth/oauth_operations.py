import os
from oauth2client import client
from oauth2client.client import OAuth2Credentials
from httplib2 import Http
from storage import Storage

class GoogleOauth:

    __storage: Storage

    def __init__(self, storage: Storage):
        if not isinstance(storage, Storage):
            raise TypeError("cache variable is not type of Cache class")
        self.__storage = storage
        self.__http = Http()

    def get_token_authorization_code(self, auth_code:str, scopes:list, redirect_uri:str) -> dict:
        secret = os.environ['GOOGLE_OAUTH_SECRET_FILE_PATH']
        credentials = client.credentials_from_clientsecrets_and_code(secret, scopes, auth_code, redirect_uri=redirect_uri)
        if credentials:
            email = credentials.id_token["email"]
            self.__storage.add_or_update(email, credentials)
        return self.__tokens_output(credentials)

    def get_silent_token(self, id:str) -> dict:
        data = self.__storage.get(id)
        credentials = OAuth2Credentials(**data)
        if credentials is None:
            return None
        if not credentials.access_token_expired:
            return self.__tokens_output(credentials)
        credentials = self.__storage.refresh(self.__http)
        self.__storage.add_or_update(id, credentials)
        return self.__tokens_output(credentials)

    def revoke(self, id:str):
        credentials = self.__storage.get(id)
        if credentials is None:
            return
        credentials.revoke(self.__http)
        self.__storage.delete(id)

    def __tokens_output(self, credentials:OAuth2Credentials) -> dict:
        return {
            'id_token': credentials.token_response["id_token"],
            'access_token': credentials.token_response["access_token"]
        }