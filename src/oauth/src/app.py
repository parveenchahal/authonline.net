import os
import logging
from flask import Flask
from flask_restful import Api
from . import config
from .controllers import PublicCertificatesController, AuthOnlineTokenController
from common.storage.cosmos import create_cosmos_container_handler
from common.key_vault import KeyVaultSecret
from common import AADToken
from common.crypto import CertificateFromKeyvault
from common.crypto.jwt import RSAPrivateKeyHandler, RSAPublicKeyHandler
from datetime import timedelta
from common.crypto.jwt import JWTHandler
from common import auth_filter
from common.storage.cosmos import CosmosClientBuilderFromKeyvaultSecret

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
session_storage_container = create_cosmos_container_handler(config.common.DatebaseName, 'session', timedelta(hours=1), client_builder)
#===================================================================================


#============================== Create JWT Handler =================================
rsa_private_key_handler = RSAPrivateKeyHandler(signing_certificate_handler)
rsa_public_key_handler = RSAPublicKeyHandler(signing_certificate_handler)
jwt_handler = JWTHandler(rsa_private_key_handler, rsa_public_key_handler)
#===================================================================================


#============================== Init Auth filter ===================================
auth_filter.init_session_validator(logger, jwt_handler)
#===================================================================================


#============================== Register Public Certificates controllers ============
api.add_resource(PublicCertificatesController, '/oauth2/public_certificates', endpoint="oauth2_public_certificates", resource_class_args=(logger, signing_certificate_handler,))
#====================================================================================


api.add_resource(AuthOnlineTokenController, '/oauth2/token', endpoint="authonline_token", resource_class_args=(logger, jwt_handler,))


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)