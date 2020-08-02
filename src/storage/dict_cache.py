from storage.storage import Storage
class DictCache(Storage):

    def __init__(self):
        self.__dict = {}

    def get(self, key: str):
        return self.__dict.get(key, None)

    def add_or_update(self, key: str, data: dict):
        self.__dict[key] = data
    
    def delete(self, key: str):
        self.__dict.pop(key, None)

    