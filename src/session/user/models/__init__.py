from dataclasses import dataclass
from common import Model


@dataclass
class UserModel(Model):
    username: str
    object_id: str
    auth_method: str