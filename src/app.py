import logging
from flask import Flask
from flask_restful import Api
import config
from controllers import Login, Logout, GoogleSignInController, PublicCertificates, AuthOnlineToken
from google_oauth import GoogleOauth
from storage import StorageDictCache
from session import SessionHandler
from crypto import CertificateFromKeyvault
from crypto.jwt import RSAPrivateKeyHandler, RSAPublicKeyHandler
from datetime import timedelta
from crypto.jwt import JWTHandler
import auth_filter

config.init()

app = Flask(__name__)
api = Api(app)

logger = logging.getLogger('werkzeug')
#logger.setLevel(logging.ERROR)

auth_filter.init_logger(logger)

api.add_resource(Login, '/login', endpoint="login", resource_class_args=(logger,))

google_oauth = GoogleOauth()
certificate_handler = CertificateFromKeyvault(config.common.SigningCertificateUri, timedelta(hours=1), config.common.KeyVaultAuthTokenUri)
rsa_private_key_handler = RSAPrivateKeyHandler(certificate_handler)
rsa_public_key_handler = RSAPublicKeyHandler(certificate_handler)
jwt_handler = JWTHandler(rsa_private_key_handler, rsa_public_key_handler)
session_handler = SessionHandler(logger, StorageDictCache(), jwt_handler, refresh_session_interval=config.common.RefreshSessionAfterInterval)
api.add_resource(GoogleSignInController, '/googlesignin', endpoint="googlesignin", resource_class_args=(logger, google_oauth, session_handler,))
api.add_resource(GoogleSignInController, '/googlesignin/<type>', endpoint="googlesignin/type", resource_class_args=(logger, google_oauth, session_handler,))

certificate_handler = CertificateFromKeyvault(config.common.SigningCertificateUri, timedelta(hours=1), config.common.KeyVaultAuthTokenUri)
api.add_resource(PublicCertificates, '/oauth2/public_certificates', endpoint="oauth2_public_certificates", resource_class_args=(logger, certificate_handler,))
api.add_resource(PublicCertificates, '/session/public_certificates', endpoint="session_public_certificates", resource_class_args=(logger, certificate_handler,))

rsa_private_key_handler = RSAPrivateKeyHandler(certificate_handler)
rsa_public_key_handler = RSAPublicKeyHandler(certificate_handler)
jwt_handler = JWTHandler(rsa_private_key_handler, rsa_public_key_handler)
api.add_resource(AuthOnlineToken, '/oauth2/token', endpoint="authonline_token", resource_class_args=(logger, jwt_handler,))

rsa_private_key_handler = RSAPrivateKeyHandler(certificate_handler)
rsa_public_key_handler = RSAPublicKeyHandler(certificate_handler)
jwt_handler = JWTHandler(rsa_private_key_handler, rsa_public_key_handler)
auth_filter.init_session_auth_filter(jwt_handler, session_handler)

api.add_resource(Logout, '/logout', endpoint="logout", resource_class_args=(logger, session_handler,))

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)