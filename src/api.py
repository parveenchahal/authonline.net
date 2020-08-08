import logging
from flask import Flask
from flask_restful import Api
import config
from controllers import GoogleSignInController, Login
from google_oauth import GoogleOauth
from storage import DictCache
from session import SessionHandler
from crypto import CertificateFromKeyvault, RSASignature
from datetime import timedelta


config.init()

app = Flask(__name__)
api = Api(app)

logger = logging.getLogger('werkzeug')
#logger.setLevel(logging.ERROR)


api.add_resource(Login, '/login', endpoint="login", resource_class_args=(logger,))

google_oauth = GoogleOauth()
certificate_handler = CertificateFromKeyvault(config.common.SigningCertificateUri, timedelta(hours=1), config.common.KeyVaultAuthTokenUri)
rsa_signature = RSASignature(certificate_handler)
session_handler = SessionHandler(logger, DictCache(), rsa_signature)

api.add_resource(GoogleSignInController, '/googlesignin', endpoint="googlesignin", resource_class_args=(logger, google_oauth, session_handler,))
api.add_resource(GoogleSignInController, '/googlesignin/<type>', endpoint="googlesignin/type", resource_class_args=(logger, google_oauth, session_handler,))

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)