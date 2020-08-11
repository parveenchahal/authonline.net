from abc import abstractmethod
from jwt.jwk import AbstractJWKBase

class SigningKeyHandler(object):

    @abstractmethod
    def get(self) -> AbstractJWKBase:
        raise NotImplementedError()