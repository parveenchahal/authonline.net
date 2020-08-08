from flask_restful import Resource
from logging import Logger


class Controller(Resource):

    _logger: Logger

    def __init__(self, logger: Logger):
        self._logger = logger

    def get(self):
        pass

    def post(self):
        pass

