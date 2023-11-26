import string
from typing import Any


class InvalidJson(Exception):
    pass


def parse(source: str, /) -> dict[str, Any] | list[Any]:
    source = source.strip()
    if source:
        result = _parse(source)
        if isinstance(result, (dict, list)):
            return result
    raise InvalidJson


Primitives = None | bool | int | float | str | list[Any] | dict[str, Any]


def _parse(source: str) -> Primitives:
    if source.isdigit():
        try:
            return int(source)
        except ValueError:
            raise InvalidJson
    elif source[0].isdigit() and source[-1].isdigit() and "." in source:
        try:
            return float(source)
        except ValueError:
            raise InvalidJson
    elif source.startswith('"') and source.endswith('"'):
        return source[1:-1]
    elif source == "true":
        return True
    elif source == "false":
        return False
    elif source == "null":
        return None
    elif source.startswith("{") and source.endswith("}"):
        return _parse_object(source)
    elif source.startswith("[") and source.endswith("]"):
        return _parse_array(source)

    raise InvalidJson


def _parse_object(source: str) -> dict[str, Any]:
    result = {}
    source = source[1:-1].strip()
    while source:
        source = source.lstrip()
        key, source = _parse_key(source)
        source = source.lstrip()
        if source[0] != ":":
            raise InvalidJson
        source = source[1:].lstrip()
        value, source = _get_next_value(source)
        result[key] = _parse(value)
        if len(source) > 1:
            source = source.lstrip(",")
        if source == ",":
            raise InvalidJson
    return result


def _parse_array(source: str) -> list[Any]:
    result = []
    source = source[1:-1].strip()
    while source:
        value, source = _get_next_value(source)
        result.append(_parse(value))
        source = source.lstrip(",")
    return result


def _parse_key(source: str) -> tuple[str, str]:
    if not source.startswith('"'):
        raise InvalidJson
    source = source[1:]
    end_quote_index = source.find('"')
    if end_quote_index == -1:
        raise InvalidJson
    key = source[:end_quote_index]
    source = source[end_quote_index + 1 :]
    return key, source


def _get_next_value(source: str) -> tuple[str, str]:
    c = source[0]
    if c == "{":
        i = _advance_until_closed(source, "{", "}") + 1
    elif c == "[":
        i = _advance_until_closed(source, "[", "]") + 1
    else:
        if c == '"':
            i = source.find('"', 1) + 1
            if i == -1:
                raise InvalidJson
        elif c == "t":
            i = 4
        elif c == "f":
            i = 5
        elif c == "n":
            i = 4
        elif c.isdecimal():
            for i in range(len(source)):
                c = source[i]
                if c in _END_OF_NUMBER:
                    break
            else:
                i = len(source)

        else:
            raise InvalidJson
    return source[:i], source[i:]


_END_OF_NUMBER = set(string.whitespace).union(",}]")


def _advance_until_closed(source: str, open: str, close: str) -> int:
    sum = 0
    for j in range(len(source)):
        c = source[j]
        if c == open:
            sum += 1
        if c == close:
            sum -= 1

        if sum == 0:
            return j
    raise InvalidJson
