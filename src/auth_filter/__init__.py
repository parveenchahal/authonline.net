from datetime import datetime
import pytz
import functools
from flask_restful import request, abort, original_flask_make_response as make_response, ResponseBase as Response
from crypto.jwt import JWTHandler
import exceptions
from session.models import Session
from session import SessionHandler
from auth_filter.session_validator import SessionValidator
import http_responses
from logging import Logger

_logger: Logger
_session_validator: SessionValidator = None

def init_logger(logger: Logger):
    global _logger
    _logger = logger

def init_session_auth_filter(jwt_handler: JWTHandler, session_handler: SessionHandler):
    global _session_validator
    if _session_validator is None:
        _session_validator = SessionValidator(_logger, jwt_handler, session_handler)
        return
    raise exceptions.CannotBeCalledMoreThanOnceError("init_session_auth_filter can't be called more than once")

def _validate_session(f, set_cookie_for_refreshed_session, *args, **kwargs):
    global _session_validator
    refreshed_session = None
    expiry = None
    try:
        session_cookie = request.cookies.get("session", None)
        if session_cookie is None:
            raise exceptions.SessionCookieNotFoundError()
        refreshed_session, expiry = _session_validator.validate(session_cookie)
    except exceptions.SessionCookieNotFoundError as ex:
        _logger.exception(ex)
        return http_responses.UnauthorizedResponse("Session can't be validated")
    except Exception as ex:
        _logger.exception(ex)
        #raise ex
        err_res = http_responses.UnauthorizedResponse("Session can't be validated")
        err_res.set_cookie('session', "", expires=datetime.utcnow(), secure=True, httponly=True)
        return err_res
    res = f(*args, **kwargs)
    if set_cookie_for_refreshed_session and refreshed_session is not None:
        _logger.info("cookie refreshed")
        expiry = datetime.fromtimestamp(expiry, pytz.utc)
        res.set_cookie('session', refreshed_session, expires=expiry, secure=True, httponly=True)
    return res

def validate_session(f=None, set_cookie_for_refreshed_session=True):
    is_callable = callable(f)
    if is_callable:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return _validate_session(f, set_cookie_for_refreshed_session, *args, **kwargs)
        return wrapper
    else:
        def inner(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                return _validate_session(f, set_cookie_for_refreshed_session, *args, **kwargs)
            return wrapper
        return inner
