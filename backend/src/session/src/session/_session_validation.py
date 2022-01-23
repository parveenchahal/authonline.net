from logging import Logger
import functools
from flask_restful import request
from common.crypto.jwt import JWTHandler
from common.authonline.session import SessionValidator
from common import exceptions, http_responses

_session_validator: SessionValidator = None
_logger: Logger = None

def init_session_validator(logger: Logger, jwt_handler: JWTHandler):
    global _session_validator, _logger
    if _session_validator is None:
        _session_validator = SessionValidator(logger, jwt_handler)
        _logger = logger
    else:
        raise exceptions.CannotBeCalledMoreThanOnceError(
            "init_session_validator can't be called more than once")

def _validate_session(f, ignore_refresh_expiry, *args, **kwargs):
    session_token: str = None
    try:
        session_token = request.headers['Session']
    except KeyError:
        return http_responses.UnauthorizedResponse("Session token not found in request.")
    try:
        _session_validator.validate(session_token, ignore_refresh_expiry=ignore_refresh_expiry)
    except exceptions.SessionRequiredRefreshError as ex:
        _logger.exception(ex)
        return http_responses.UnauthorizedResponse("Session required refresh.")
    except exceptions.SessionExpiredError as ex:
        _logger.exception(ex)
        return http_responses.UnauthorizedResponse("Session expired.")
    except Exception as ex:
        _logger.exception(ex)
        return http_responses.UnauthorizedResponse("Session token can't be validated")

    return f(*args, **kwargs)

def validate_session(f=None, ignore_refresh_expiry=False):
    is_callable = callable(f)
    if is_callable:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return _validate_session(f, ignore_refresh_expiry, *args, **kwargs)
        return wrapper
    else:
        def inner(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                return _validate_session(f, ignore_refresh_expiry, *args, **kwargs)
            return wrapper
        return inner
