import logging
from flask import Flask
from flask_restful import Api
import config
from controllers import GoogleSignInController, Login, PublicCertificate, AuthOnlineToken
from google_oauth import GoogleOauth
from storage import DictCache
from session import SessionHandler
from crypto import CertificateFromKeyvault, RSAKeyHandler
from datetime import timedelta
from crypto import JWTTokenHandler

config.init()

app = Flask(__name__)
api = Api(app)

logger = logging.getLogger('werkzeug')
#logger.setLevel(logging.ERROR)


api.add_resource(Login, '/login', endpoint="login", resource_class_args=(logger,))

google_oauth = GoogleOauth()
certificate_handler = CertificateFromKeyvault(config.common.SigningCertificateUri, timedelta(hours=1), config.common.KeyVaultAuthTokenUri)
rsa_key_handler = RSAKeyHandler(certificate_handler)
jwt_token_handler = JWTTokenHandler(rsa_key_handler)
session_handler = SessionHandler(logger, DictCache(), jwt_token_handler)
api.add_resource(GoogleSignInController, '/googlesignin', endpoint="googlesignin", resource_class_args=(logger, google_oauth, session_handler,))
api.add_resource(GoogleSignInController, '/googlesignin/<type>', endpoint="googlesignin/type", resource_class_args=(logger, google_oauth, session_handler,))

certificate_handler = CertificateFromKeyvault(config.common.SigningCertificateUri, timedelta(hours=1), config.common.KeyVaultAuthTokenUri)
api.add_resource(PublicCertificate, '/public_certificate', endpoint="public_certificate", resource_class_args=(logger, certificate_handler,))

certificate_handler = CertificateFromKeyvault(config.common.SigningCertificateUri, timedelta(hours=1), config.common.KeyVaultAuthTokenUri)
rsa_key_handler = RSAKeyHandler(certificate_handler)
jwt_token_handler = JWTTokenHandler(rsa_key_handler)
api.add_resource(AuthOnlineToken, '/oauth2/token', endpoint="authonline_token", resource_class_args=(logger, jwt_token_handler,))

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)