import string
from typing import Any, Callable, Protocol, TypeVar


class InvalidJson(Exception):
    pass


def parse(source: str, /) -> dict[str, Any] | list[Any]:
    if not source:
        raise InvalidJson
    if source.startswith("{"):
        result: dict[str, Any] = {}
        update_op = _update_dict
        end = "}"
    elif source.startswith("["):
        raise InvalidJson
    else:
        raise InvalidJson
    i = _ignore_spaces(0, source)
    return _parse(i, source, result, update_op, end)[1]


T = TypeVar("T")


def _parse(
    i: int, source: str, container: T, update_op: Callable[[int, str, T], int], end: str
) -> tuple[int, T]:
    if source == "{}" or source == "[]":
        return i, container
    i = _ignore_spaces(i, source)
    i = update_op(i + 1, source, container)
    i = _ignore_spaces(i +1, source)
    if i == -1:
        return i, container
    while i < len(source):
        c = source[i]
        if c == ",":
            i = _ignore_spaces(i, source)
            i = update_op(i + 1, source, container)
            i = _ignore_spaces(i, source)
        elif c == end:
            j = _ignore_spaces(i + 1, source)
            if j != -1:
                raise InvalidJson
            return i, container
        else:
            i, _ = _grab_until(i, source, ",}]")
    raise InvalidJson


def _update_dict(i: int, source: str, container: dict[str, Any], /) -> int:
    if i == -1:
        raise InvalidJson
    i = _ignore_spaces(i, source)
    i, key = _grab_key(i, source)
    i = _ignore_spaces(i+1, source)
    if source[i] != ":":
        raise InvalidJson
    i = _ignore_spaces(i + 1, source)
    i, value = _grab_value(i, source)
    container[key] = value
    return i


def _update_list(i: int, source: str, container: list[Any], /) -> int:
    if i == -1:
        raise InvalidJson
    while i < len(source):
        i = _ignore_spaces(i + 1, source)
        i, value = _grab_value(i, source)
        container.append(value)
    return i


_SPACES = set(string.whitespace)


def _ignore_spaces(i: int, source: str) -> int:
    """
    Return the index of the next character that is not a space. Returns `-1` if
    all subsequent characters are spaces.
    """
    if i == -1:
        raise InvalidJson
    for j in range(i, len(source)):
        c = source[j]
        if c not in _SPACES:
            return j
    return -1


def _grab_key(i: int, source: str) -> tuple[int, str]:
    if i == -1:
        raise InvalidJson
    buffer = source[i]
    if buffer != '"':
        raise InvalidJson
    quotes_count = 1
    for j in range(i + 1, len(source), 1):
        c = source[j]
        buffer += c
        if c == '"':
            quotes_count += 1
            if quotes_count >= 2:
                break
    else:
        raise InvalidJson
    return j, buffer[1:-1]

def _grab_value(i: int, source: str) -> tuple[int, None | bool | int | float |str | list[Any], dict[str, Any]]:
    if i == -1:
        raise InvalidJson
    c = source[i]
    if c == "{":
        return _parse(i, source, {}, _update_dict, "}")
    elif c == "[":
        return _parse(i, source, [], _update_list, "]")
    else:
        if c == '"':
            i, value = _grab_until(i + 1, source, '"')
            value = value[:-1]
        elif c == "t":
            _grab_while(i, source, 'true')
            i, value = i + 3, True
        elif c == "f":
            _grab_while(i, source, 'false')
            i, value = i + 4, False
        elif c == "n":
            _grab_while(i, source, 'null')
            i, value = i + 3, None
        elif c.isdecimal():
            i, value = _grab_until(i, source, _SPACES.union(".]}"))
            if value.endswith("."):
                raise InvalidJson
            if value.endswith("}") or value.endswith("]"):
                value = value[:-1]
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    raise InvalidJson
        else:
            raise InvalidJson
    
        return i, value

class _Container(Protocol):
    def __contains__(self, a: Any) -> bool:
        ...

def _grab_until(i: int, source: str, to_stop: _Container) -> tuple[int, str]:
    if i == -1:
        raise InvalidJson
    buffer = ""
    for j in range(i, len(source)):
        c = source[j]
        buffer += c
        if c in to_stop:
            return j, buffer
    raise InvalidJson

def _grab_while(i: int, source: str, expected: str) -> None:
    if i == -1:
        raise InvalidJson
    for j in range(len(expected)):
        if source[i + j] != expected[j]:
            raise InvalidJson