from abc import abstractmethod
class Certificate(object):
    @abstractmethod
    def get(self) -> list:
        raise NotImplementedError()