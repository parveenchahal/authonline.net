from abc import abstractmethod

class Storage():
    @abstractmethod
    def get(self, key: str) -> dict:
        raise NotImplementedError()
    
    @abstractmethod
    def add_or_update(self, key: str, data: dict) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, key: str) -> bool:
        raise NotImplementedError()
