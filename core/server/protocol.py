import json
from typing import Any


ENCODING = "utf-8"


def encode_json(data: Any) -> bytes:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode(ENCODING)


def decode_json(data: bytes | str) -> Any:
    if isinstance(data, bytes):
        data = data.decode(ENCODING)
    return json.loads(data)
