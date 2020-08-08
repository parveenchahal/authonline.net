import logging
from flask import Flask
from flask_restful import Api
import config
from controllers import GoogleSignInController
from google_oauth import GoogleOauth
from storage import DictCache
from session import SessionHandler
from crypto import CertificateFromKeyvault
from datetime import timedelta

app = Flask(__name__)
api = Api(app)

logger = logging.getLogger('werkzeug')
logger.setLevel(logging.ERROR)



api.add_resource(GoogleSignInController, '/googlesignin', "/googlesignin/", endpoint="googlesignin")

google_oauth = GoogleOauth(DictCache())
session_handler = SessionHandler(logger, DictCache(), CertificateFromKeyvault(config.common.SigningCertificateUri, timedelta(hours=1), config.common.KeyVaultAuthTokenUri))
api.add_resource(GoogleSignInController, '/googlesignin/<type>', endpoint="googlesignin/type", resource_class_args=(logger, google_oauth, session_handler,))

if __name__ == '__main__':
    config.init()
    app.run(debug=False, host="0.0.0.0", port=5000)