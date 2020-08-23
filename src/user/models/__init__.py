from dataclasses import dataclass
from common.abstract_model import Model


@dataclass
class UserModel(Model):
    username: str
    object_id: str
    auth_method: str