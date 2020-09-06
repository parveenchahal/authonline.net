import os
import urllib.parse as urlparse
from flask import redirect, render_template
from common import Controller
from flask_restful import request, url_for, ResponseBase as Response
from .. import config
from common import exceptions
from common import http_responses

class LoginController(Controller):

    def _validate_query_params(self, args: dict):
        client_id = args.get("client_id", None)
        if client_id is None:
            raise exceptions.MissingParamError("client_id is missing")
        resource = args.get("resource", None)
        if resource is None:
            raise exceptions.MissingParamError("resource is missing")
        redirect_uri = args.get("redirect_uri", None)
        if redirect_uri is None:
            raise exceptions.MissingParamError("redirect_uri is missing")

    def _update_page_with_values(self, page: str, args: dict):
        resource = args.get('resource')
        client_id = args.get('client_id')
        redirect_uri = args.get('redirect_uri')
        state = args.get('state', '')
        page = page.replace("$resource$", resource)
        page = page.replace("$redirect_uri$", redirect_uri)
        page = page.replace("$state$", state)
        page = page.replace("$client_id$", client_id)
        return page

    def get(self):
        try:
            args = request.args
            self._validate_query_params(args)
            resource = args.get("resource", None)
            if resource is None:
                resource = config.common.BaseUrl
            file_path = os.path.join(os.getcwd(), "statics/login.html")
            with open(file_path, 'r') as f:
                data = f.read()
                data = self._update_page_with_values(data, args)
                return Response(data, mimetype='text/html')
        except exceptions.MissingParamError as e:
            self._logger.exception(e)
            return http_responses.BadRequestResponse(str(e))
        except Exception as e:
            self._logger.exception(e)
            return http_responses.InternalServerErrorResponse()