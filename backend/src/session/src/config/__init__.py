from . import common
from . import google_token_signin as google_token_signin


def init():
    google_token_signin.init()
    common.init()
