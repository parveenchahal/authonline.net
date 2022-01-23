from typing import List
import uuid
from common.databases.nosql import DatabaseOperations
from common.databases.nosql.models import DatabaseEntryModel
from common.utils import dict_to_obj
from .models import SessionRegistrationDetailsModel

class SessionRegistrationHandler(object):

    _db_op: DatabaseOperations

    def __init__(self, db_op: DatabaseOperations):
        self._db_op = db_op

    def get(self, client_id: str) -> SessionRegistrationDetailsModel:
        db_entry = self._db_op.get(client_id, 0)
        if db_entry is not None:
            return dict_to_obj(SessionRegistrationDetailsModel, db_entry.data)
        return None

    def _validate_reg_details(self, obj: SessionRegistrationDetailsModel):
        if obj.client_id is None or obj.client_id == '':
            raise ValueError('resource can not be None or empty')
        if obj.resource is None or obj.resource == '':
            raise ValueError('resource can not be None or empty')
        if obj.owners is None or len(obj.owners) == 0:
            raise ValueError('owners list can not be None or empty')
        if obj.redirect_uris is None or len(obj.redirect_uris) == 0:
            raise ValueError('redirect_uris can not be None or empty')

    def create(self, resourse: str, owners: List[str], redirect_uris: List[str]):
        client_id = str(uuid.uuid4())
        reg_details = SessionRegistrationDetailsModel(client_id, resourse, owners, redirect_uris)
        self.update(reg_details)

    def update(self, reg_details: SessionRegistrationDetailsModel):
        self._validate_reg_details(reg_details)
        db_entry = DatabaseEntryModel(reg_details.client_id, 0, reg_details.to_dict())
        self._db_op.insert_or_update(db_entry)

