from common.abstract_model import Model as _Model

class UserInfoModel(_Model):
    username: str = None
    name: str = None
    first_name: str = None
    last_name: str = None
    email: str = None
    email_verified: bool = None,
    photo_url: str = None

