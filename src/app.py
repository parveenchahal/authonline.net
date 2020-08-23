import os
import logging
from flask import Flask
from flask_restful import Api
import config
from controllers import LoginController, LogoutController, GoogleSignInController, PublicCertificatesController, AuthOnlineTokenController, UserInfoController
from google_oauth import GoogleOauth
from storage.cosmos import create_cosmos_container_handler, create_database_container_if_not_exists
from common.key_vault import KeyVaultSecret
from common import AADToken
from session import SessionHandler
from crypto import CertificateFromKeyvault
from crypto.jwt import RSAPrivateKeyHandler, RSAPublicKeyHandler
from datetime import timedelta
from crypto.jwt import JWTHandler
import auth_filter
from user_info import UserInfoHandler
from user import UserHandler
from registration import SessionRegistrationHandler
from storage.cosmos import CosmosClientBuilderFromKeyvaultSecret

config.init()

app = Flask(__name__)
api = Api(app)

logger = logging.getLogger('werkzeug')
#logger.setLevel(logging.ERROR)

#============================== AAD Token ==========================================
AAD_IDENTITY_TENANT = os.environ['AAD_IDENTITY_TENANT']
AAD_IDENTITY_CLIENTID = os.environ['AAD_IDENTITY_CLIENTID']
AAD_IDENTITY_SECRET = os.environ['AAD_IDENTITY_SECRET']
key_vault_token = AADToken(AAD_IDENTITY_CLIENTID, AAD_IDENTITY_SECRET, 'https://vault.azure.net', tenant=AAD_IDENTITY_TENANT)
#===================================================================================


#============================== Create Signing Certificate Handler =================
secret = KeyVaultSecret(config.common.KeyVaultName, config.common.SigningCertificateName, key_vault_token)
signing_certificate_handler = CertificateFromKeyvault(secret, timedelta(hours=1))
#===================================================================================


#============================== Create Storage handlers ============================
secret = KeyVaultSecret(config.common.KeyVaultName, config.common.CosmosDbConnectionStrings, key_vault_token)
client_builder = CosmosClientBuilderFromKeyvaultSecret(secret)
create_database_container_if_not_exists(client_builder, config.common.DatebaseName, ('user', 'session', 'user_info', 'registration_for_session'))
session_storage_container = create_cosmos_container_handler(config.common.DatebaseName, 'session', timedelta(hours=1), client_builder)
user_storage_container = create_cosmos_container_handler(config.common.DatebaseName, 'user', timedelta(hours=1), client_builder)
user_info_storage_container = create_cosmos_container_handler(config.common.DatebaseName, 'user_info', timedelta(hours=1), client_builder)
registration_for_session_storage_container = create_cosmos_container_handler(config.common.DatebaseName, 'registration_for_session', timedelta(hours=1), client_builder)

userinfo_handler = UserInfoHandler(logger, user_info_storage_container)
user_handler = UserHandler(user_storage_container)
#===================================================================================


#============================== Create JWT Handler =================================
rsa_private_key_handler = RSAPrivateKeyHandler(signing_certificate_handler)
rsa_public_key_handler = RSAPublicKeyHandler(signing_certificate_handler)
jwt_handler = JWTHandler(rsa_private_key_handler, rsa_public_key_handler)
#===================================================================================


#============================== Create session handler =============================
session_handler = SessionHandler(logger, session_storage_container, jwt_handler, refresh_session_interval=config.common.RefreshSessionAfterInterval)
#===================================================================================


#============================== Create registration handler ========================
session_registration_handler = SessionRegistrationHandler(registration_for_session_storage_container)
#===================================================================================


#============================== Init Auth filter ===================================
auth_filter.init_logger(logger)
auth_filter.init_session_auth_filter(jwt_handler, session_handler)
#===================================================================================


#============================== Register login/logout controllers =========================
api.add_resource(LoginController, '/login', endpoint="login", resource_class_args=(logger,))
api.add_resource(LogoutController, '/logout', endpoint="logout", resource_class_args=(logger, session_handler,))
#===================================================================================


#============================== Register Public Certificate controllers =============
api.add_resource(PublicCertificatesController, '/oauth2/public_certificates', endpoint="oauth2_public_certificates", resource_class_args=(logger, signing_certificate_handler,))
api.add_resource(PublicCertificatesController, '/session/public_certificates', endpoint="session_public_certificates", resource_class_args=(logger, signing_certificate_handler,))
#====================================================================================


#============================== Register Userinfo controllers =======================
api.add_resource(UserInfoController, '/userinfo', endpoint="oauth2_userinfo", resource_class_args=(logger, userinfo_handler,))
#====================================================================================


#============================== Register GoogleSignIn controllers ===================
google_oauth = GoogleOauth()
api.add_resource(GoogleSignInController, '/googlesignin', endpoint="googlesignin", resource_class_args=(logger, google_oauth, session_handler, user_handler, userinfo_handler, session_registration_handler,))
api.add_resource(GoogleSignInController, '/googlesignin/<type>', endpoint="googlesignin/type", resource_class_args=(logger, google_oauth, session_handler, user_handler, userinfo_handler, session_registration_handler,))
#====================================================================================


api.add_resource(AuthOnlineTokenController, '/oauth2/token', endpoint="authonline_token", resource_class_args=(logger, jwt_handler,))





if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)