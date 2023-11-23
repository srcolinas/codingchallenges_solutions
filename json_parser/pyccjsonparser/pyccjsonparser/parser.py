import string
from typing import Any


class InvalidJson(Exception):
    pass



def parse(source: str, /) -> dict[str, Any]:
    if not source:
        raise InvalidJson
    if source == "{}":
        return {}
    spaces = set(string.whitespace)
    value_termination_chars = {",", "}"}
    i = 0
    parsing_keyvalue_pair = False
    parsed_key = ""
    result: dict[str, Any] = {}
    while i < len(source):
        if parsing_keyvalue_pair:
            i = _ignore_chars(i, source, spaces)
            i, parsed_key = _grab_key(i, source)
            i = _ignore_chars(i+1, source, spaces)
            if source[i] != ":":
                raise InvalidJson
            i = _ignore_chars(i +1, source, spaces)
            i, value = _grab_value(i, source, value_termination_chars)
            result[parsed_key] = _parse_basic_values(value)
            parsing_keyvalue_pair = False
        else:
            i = _ignore_chars(i, source, spaces)
            match source[i]:
                case "{":
                    i = _ignore_chars(i, source, spaces)
                    parsing_keyvalue_pair = True
                case ",":
                    i = _ignore_chars(i, source, spaces)
                    parsing_keyvalue_pair = True
                case "}":
                    return result
        i += 1
    raise InvalidJson

def _ignore_chars(i: int, source: str, to_ignore: set[str]) -> int:
    for j in range(i, len(source) - 1):
        c = source[j]
        if c not in to_ignore:
            return j
    return i


def _grab_key(i: int, source: str) -> tuple[int, str]:
    buffer = source[i]
    if buffer != '"':
        raise InvalidJson
    quotes_count = 1
    for j in range(i+1, len(source) - 1, 1):
        c = source[j]
        buffer += c
        if c == '"':
            quotes_count += 1
            if quotes_count >= 2:
                break
    else:
        raise InvalidJson
    return j, buffer[1:-1]

def _grab_value(i: int, source: str, termination_chars: set[str]) -> tuple[int, str]:
    buffer = ""
    for j in range(i, len(source) - 1, 1):
        buffer += source[j]
        if source[j+1] in termination_chars:
            return j, buffer
    raise InvalidJson

def _parse_basic_values(buffer: str) -> None | bool | str | int | float:
    buffer = buffer.lstrip().rstrip()
    if buffer.startswith('"') and buffer.endswith('"'):
        return buffer[1:-1]
    elif buffer == "true":
        return True
    elif buffer == "false":
        return False
    elif buffer == "null":
        return None
    else:
        try:
            return int(buffer)
        except ValueError:
            try:
                return float(buffer)
            except ValueError:
                raise InvalidJson
    