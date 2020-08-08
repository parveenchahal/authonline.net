import json
from base64 import b64encode, b64decode
from typing import Any

def bytes_to_string(b: bytes) -> str:
    return b.decode('UTF-8', errors='strict')

def string_to_bytes(s: str) -> bytes:
    return s.encode('UTF-8', errors='strict')

def encode_base64(data) -> str:
    if isinstance(data, bytes):
        return bytes_to_string(b64encode(data))
    if isinstance(data, str):
        return bytes_to_string(b64encode(string_to_bytes(data)))
    raise ValueError("Format is not supported")

def decode_base64(data) -> str:
    if isinstance(data, bytes):
        return bytes_to_string(b64decode(data))
    if isinstance(data, str):
        return bytes_to_string(b64decode(string_to_bytes(data)))
    raise ValueError("Format is not supported")

def parse_json(json_string: str):
    return json.loads(json_string)

def json_to_obj(cls, json_string: str) -> Any:
    j = parse_json(json_string)
    return cls(**j)

def to_json_string(d: dict) -> str:
    return json.dumps(d)