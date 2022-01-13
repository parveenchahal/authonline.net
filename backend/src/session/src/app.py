import os
from datetime import timedelta
import logging
from flask import Flask
from flask_restful import Api
from redis import Redis

from common import AADToken
from common.cache.redis import RedisCache
from common.crypto import CertificateFromKeyvault
from common.crypto.rsa import RSAPrivateKeyHandler, RSAPublicKeyHandler
from common.crypto.jwt import JWTHandler
from common.key_vault import KeyVaultSecret
from common.storage.cosmos import CosmosClientBuilderFromKeyvaultSecret
from .session import init_session_validator
from common.storage.cosmos import create_cosmos_container_handler, \
                                create_database_container_if_not_exists
from . import config
from .controllers import LogoutController, GoogleSignInController, \
                        PublicCertificatesController, UserInfoController, \
                        RefreshSessionTokenController, SessionRegistrationController
from .google_oauth import GoogleOauth
from .session import SessionHandler
from .user_info import UserInfoHandler
from .user import UserHandler
from .registration import SessionRegistrationHandler

config.init()

app = Flask(__name__)
api = Api(app)

redis_client = Redis(host='redis-service.default')

logger = logging.getLogger('werkzeug')
#logger.setLevel(logging.ERROR)

#============================== AAD Token ==========================================
AAD_IDENTITY_TENANT = os.environ['AAD_IDENTITY_TENANT']
AAD_IDENTITY_CLIENTID = os.environ['AAD_IDENTITY_CLIENTID']
AAD_IDENTITY_SECRET = os.environ['AAD_IDENTITY_SECRET']
key_vault_token = AADToken(
    AAD_IDENTITY_CLIENTID,
    AAD_IDENTITY_SECRET,
    'https://vault.azure.net',
    tenant=AAD_IDENTITY_TENANT)
#===================================================================================


#============================== Create Signing Certificate Handler =================
secret = KeyVaultSecret(
    config.common.KeyVaultName,
    config.common.SigningCertificateName,
    key_vault_token)
signing_certificate_handler = CertificateFromKeyvault(
    secret,
    RedisCache(redis_client, timedelta(hours=1),
    namespace="public_certificate"))
#===================================================================================


#============================== Create Storage handlers ============================
secret = KeyVaultSecret(
    config.common.KeyVaultName,
    config.common.CosmosDbConnectionStrings,
    key_vault_token)
client_builder = CosmosClientBuilderFromKeyvaultSecret(secret)
create_database_container_if_not_exists(
    client_builder,
    config.common.DatebaseName,
    ('user_principal', 'session', 'user_principal_info', 'registration_for_session'),
    config.common.CosmosOfferThroughput)
session_storage_container = create_cosmos_container_handler(
    config.common.DatebaseName,
    'session',
    timedelta(hours=1),
    client_builder)
user_storage_container = create_cosmos_container_handler(
    config.common.DatebaseName,
    'user_principal',
    timedelta(hours=1),
    client_builder)
user_info_storage_container = create_cosmos_container_handler(
    config.common.DatebaseName,
    'user_principal_info',
    timedelta(hours=1),
    client_builder)
registration_for_session_storage_container = create_cosmos_container_handler(
    config.common.DatebaseName,
    'registration_for_session',
    timedelta(hours=1),
    client_builder)

userinfo_handler = UserInfoHandler(logger, user_info_storage_container)
user_handler = UserHandler(user_storage_container)
#===================================================================================


#============================== Create JWT Handler =================================
rsa_private_key_handler = RSAPrivateKeyHandler(signing_certificate_handler)
rsa_public_key_handler = RSAPublicKeyHandler(signing_certificate_handler)
jwt_handler = JWTHandler(rsa_private_key_handler, rsa_public_key_handler)
#===================================================================================


#============================== Create session handler =============================
session_handler = SessionHandler(
    logger,
    session_storage_container,
    jwt_handler,
    refresh_session_interval=config.common.RefreshSessionAfterInterval)
#===================================================================================


#============================== Create registration handler ========================
session_registration_handler = SessionRegistrationHandler(
    registration_for_session_storage_container)
#===================================================================================


#============================== Init Auth filter ===================================
init_session_validator(logger, jwt_handler)
#===================================================================================


#============================== Register login/logout controller =========================
api.add_resource(
    LogoutController, '/logout', endpoint="logout", resource_class_args=(logger, session_handler,))
#===================================================================================


#============================== Register Public Certificate controller =============
api.add_resource(
    PublicCertificatesController,
    '/session/public_certificates',
    endpoint="session_public_certificates",
    resource_class_args=(logger, signing_certificate_handler,))
#====================================================================================

#============================== Session Registration controller =============
api.add_resource(
    SessionRegistrationController,
    '/session/registration',
    endpoint="session_registration",
    resource_class_args=(logger, session_registration_handler,))
#====================================================================================

#============================== Register Userinfo controller =======================
api.add_resource(
    UserInfoController,
    '/session/userinfo',
    endpoint="oauth2_userinfo",
    resource_class_args=(logger, userinfo_handler,))
#====================================================================================


#============================== Session refresh ====================================
api.add_resource(
    RefreshSessionTokenController,
    '/session/refresh',
    endpoint="session_refresh",
    resource_class_args=(logger, session_handler,))
#====================================================================================


#============================== Register GoogleSignIn controllers ===================
google_oauth = GoogleOauth()
api.add_resource(
    GoogleSignInController,
    '/session/googlesignin',
    endpoint="googlesignin",
    resource_class_args=(
        logger,
        google_oauth,
        session_handler,
        user_handler,
        userinfo_handler,
        session_registration_handler,))
api.add_resource(
    GoogleSignInController,'/session/googlesignin/<type>',
    endpoint="googlesignin/type",
    resource_class_args=(
        logger,
        google_oauth,
        session_handler,
        user_handler,
        userinfo_handler,
        session_registration_handler,))
#====================================================================================


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
