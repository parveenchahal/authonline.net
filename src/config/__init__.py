import config
import config.common as common
import config.google_token_signin as google_token_signin


def init():
    config.google_token_signin.init()
    config.common.init()
