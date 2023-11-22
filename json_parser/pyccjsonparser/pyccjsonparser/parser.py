import string
from enum import Enum
from typing import Any


class InvalidJson(Exception):
    pass


class _Item(Enum):
    KEY = 1
    VALUE = 2
    NOTHING = 3


def parse(source: str, /) -> dict[str, Any]:
    if not source:
        raise InvalidJson
    if source == "{}":
        return {}
    spaces = set(string.whitespace)
    i = 0
    buffer_for = _Item.NOTHING
    key_sentinel, value_sentinel = object(), object()
    parsed_value = value_sentinel
    parsed_key = key_sentinel
    buffer = ""
    result = {}
    while i < len(source):
        if buffer_for is _Item.KEY:
            c = source[i]
            parsed_value = value_sentinel
            if c in spaces:
                i += 1
                continue
            for j in range(i, len(source) -1, 1):
                buffer += source[j]
                if buffer.count('"') == 2:
                    buffer_for = _Item.NOTHING
                    break
            else:
                raise InvalidJson
            parsed_key = buffer[1:-1]
            buffer = ""
            i = j
        elif buffer_for is _Item.VALUE:
            c = source[i]
            if c in spaces:
                i += 1
                continue
            for j in range(i, len(source) -1, 1):
                buffer += source[j]
                if buffer.count('"') == 2:
                    buffer_for = _Item.NOTHING
                    break
            else:
                raise InvalidJson
            parsed_value = buffer[1:-1]
            buffer = ""
            result[parsed_key] = parsed_value
            parsed_key = key_sentinel
            i = j
        else:
            c = source[i]
            match c:
                case " ":
                    i += 1
                    continue
                case "\t":
                    i += 1
                    continue
                case "\n":
                    i += 1
                    continue
                case "\r":
                    i += 1
                    continue
                case "\v":
                    i += 1
                    continue
                case "\f":
                    i += 1
                    continue
                case "{":
                    buffer_for = _Item.KEY
                case ":":
                    buffer_for = _Item.VALUE
                case ",":
                    buffer_for = _Item.KEY
                case "}":
                    return result

        i += 1
    raise InvalidJson