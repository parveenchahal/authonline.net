import logging
from flask import Flask
from flask_restful import Api
import config
from controllers import GoogleSignInController
from google_oauth import GoogleOauth
from cache import DictCache

app = Flask(__name__)
api = Api(app)

google_oauth = GoogleOauth(DictCache())
api.add_resource(GoogleSignInController, '/googlesignin', "/googlesignin/", endpoint="googlesignin")
api.add_resource(GoogleSignInController, '/googlesignin/<type>', endpoint="googlesignin/type", resource_class_args=(google_oauth,))

if __name__ == '__main__':
    #logger = logging.getLogger('werkzeug')
    #logger.setLevel(logging.ERROR)
    config.init()
    app.run(debug=False, host="0.0.0.0", port=5000)