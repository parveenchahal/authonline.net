from base64 import b64decode
from common.utils import string_to_bytes, parse_json
from common.abstract_model import Model
from typing import Dict
from dataclasses import dataclass

@dataclass
class Certificate(Model):
    private_key: bytes
    certificate: bytes

    @staticmethod
    def from_json_string(cls, json_data: str):
        d:Dict[str] = parse_json(json_data)
        bd = {
            'private_key': b64decode(string_to_bytes(d['key'])),
            'certificate': b64decode(string_to_bytes(d['crt']))
        }
        return cls(**bd)