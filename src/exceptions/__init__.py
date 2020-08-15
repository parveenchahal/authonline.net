class LoginFailureError(Exception):
    pass

class MissingParamError(Exception):
    pass

class CannotBeCalledMoreThanOnceError(Exception):
    pass

class SessionCookieNotFoundError(Exception):
    pass

class SessionExpiredError(Exception):
    pass

class JWTTokenInvalidSignatureError(Exception):
    pass