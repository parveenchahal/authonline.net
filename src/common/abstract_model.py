import copy
from common.utils import parse_json as _parse_json, json_to_obj as _json_to_obj, to_json_string as _to_json_string
from typing import Any
from dataclasses import dataclass

@dataclass
class Model(object):

    def to_dict(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        return d

    def to_json_string(self) -> str:
        return _to_json_string(self.to_dict())

    @staticmethod
    def from_json_string(cls, json_data: str) -> Any:
        return _json_to_obj(cls, json_data)