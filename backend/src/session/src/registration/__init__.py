from typing import List
import uuid
from common.storage import Storage
from common.storage.models import StorageEntryModel
from common.utils import dict_to_obj
from .models import SessionRegistrationDetailsModel

class SessionRegistrationHandler(object):

    _storage: Storage

    def __init__(self, storage: Storage):
        self._storage = storage

    def get(self, client_id: str) -> SessionRegistrationDetailsModel:
        storage_entry = self._storage.get(client_id, 0)
        if storage_entry is not None:
            return dict_to_obj(SessionRegistrationDetailsModel, storage_entry.data)
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
        storage_entry = StorageEntryModel(reg_details.client_id, 0, reg_details.to_dict())
        self._storage.add_or_update(storage_entry)

