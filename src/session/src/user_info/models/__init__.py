from dataclasses import dataclass
from common import Model as _Model

@dataclass
class UserInfoModel(_Model):
    object_id: str
    username: str
    name: str
    first_name: str
    last_name: str
    email: str
    email_verified: bool
    photo_url: str

    def to_dict(self):
        return super().to_dict(omit_none=True)
