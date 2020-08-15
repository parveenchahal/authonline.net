from flask_restful import Resource, ResponseBase as _Response
from logging import Logger
from common.utils import to_json_string


class Controller(Resource):

    _logger: Logger

    def __init__(self, logger: Logger):
        self._logger = logger

    def get(self):
        pass

    def post(self):
        pass

    def _json_response(self, data, http_status=200):
        if isinstance(data, (list, dict)):
            data = to_json_string(data)
        return _Response(response=data, status=http_status, mimetype='application/json')