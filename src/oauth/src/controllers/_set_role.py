from jinja2.utils import clear_caches
from common import Controller
from common import http_responses
from common.storage import Storage
from common.storage.models import StorageEntryModel
from ..roles.models import RoleAssignmentModel
from flask_restful import request

class SetRoleController(Controller):

    _storage: Storage

    def __init__(self, logger, storage: Storage):
        super().__init__(logger)
        self._storage = storage

    def post(self):
        try:
            role_name = None
            client_id = None
            object_id = None
            try:
                role_name = request.headers['role_name']
            except KeyError:
                return http_responses.BadRequestResponse('role_name header not found.')
                
            try:
                client_id = request.headers['client_id']
            except KeyError:
                return http_responses.BadRequestResponse('client_id header not found.')

            try:
                object_id = request.headers['object_id']
            except KeyError:
                return http_responses.BadRequestResponse('object_id header not found.')

            role_assignment = RoleAssignmentModel(role_name=role_name, object_id=object_id, client_id=client_id)
            storage_entry = StorageEntryModel(role_assignment.object_id, role_assignment, role_assignment.client_id)
            self._storage.add_or_update(storage_entry)
        except Exception as e:
            self._logger.exception(e)
            return http_responses.InternalServerErrorResponse()
