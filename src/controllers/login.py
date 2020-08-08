import os
import urllib.parse
from flask import redirect, render_template
from controllers import Controller
from flask_restful import request, url_for, ResponseBase as Response
import config

class Login(Controller):

    def get(self):
        args = request.args
        resource = args.get("resource", None)
        if resource is None:
            resource = config.common.BaseUrl
        file_path = os.path.join(os.getcwd(), "src/statics/login.html")
        with open(file_path, 'r') as f:
            data = f.read()
            data = data.replace("?", resource)
        return Response(data, mimetype='text/html')