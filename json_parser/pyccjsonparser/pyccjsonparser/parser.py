import string
from enum import Enum
from typing import Any, Callable, Protocol, TypeVar


class InvalidJson(Exception):
    pass


def parse(source: str, /) -> dict[str, Any] | list[Any]:
    result = _parse(source)
    if isinstance(result, (dict, list)):
        return result
    raise InvalidJson


class _ObjectType(Enum):
    ARRAY = 1
    OBJECT = 2


def _parse(source: str) -> None | bool | int | float | str | list[Any] | dict[str, Any]:
    if not source:
        raise InvalidJson
    if source.startswith('"') and source.endswith('"'):
        return source[1:-1]
    elif source[0].isdecimal() and source[-1].isdecimal():
        try:
            return int(source)
        except ValueError:
            try:
                return float(source)
            except ValueError:
                raise InvalidJson
    elif source == "true":
        return True
    elif source == "false":
        return False
    elif source == "null":
        return None
    elif source.startswith("{") and source.endswith("}"):
        dict_container: dict[str, Any] = {}
        end = "}"
        object_type = _ObjectType.OBJECT
    elif source.startswith("[") and source.endswith("]"):
        list_container: list[Any] = []
        end = "]"
        object_type = _ObjectType.ARRAY
    else:
        raise InvalidJson

    i = 0
    while i < len(source):
        c = source[i]
        if c == ",":
            i = _advance_until_or_fail(
                i + 1,
                source,
                lambda x: x in '"[{'
                or (x.isdecimal() and object_type is _ObjectType.ARRAY),
                fail_predicate=lambda x: (
                    x.isalnum() and object_type is _ObjectType.OBJECT
                )
                or x in "]}",
            )
        elif c == end:
            if object_type is _ObjectType.OBJECT:
                return dict_container
            else:
                return list_container
        elif c in "[{":
            i = _advance_until_or_fail(i + 1, source, _is_not_space)
            if source[i] in ",.":
                raise InvalidJson
        else:
            if object_type is _ObjectType.OBJECT:
                i = _advance_until_or_fail(i, source, lambda x: x == '"')
                i, key = _grab_key(i, source)
                i = _advance_until_or_fail(i + 1, source, lambda x: x == ":")
                i = _advance_until_or_fail(i + 1, source, _is_not_space)
                j = _find_value_ends(i, source)
                parsed_value = _parse(source[i : j + 1])
                dict_container[key] = parsed_value
                i = j + 1
            else:
                i = _advance_until_or_fail(
                    i, source, lambda x: x in '"tfn' or x.isdecimal()
                )
                j = _find_value_ends(i, source)
                parsed_value = _parse(source[i : j + 1])
                list_container.append(parsed_value)
                i = j + 1
            i = _advance_until_or_fail(i, source, lambda x: x in ",}]")
    raise InvalidJson


def _is_not_space(x: str) -> bool:
    return x not in _SPACES


_SPACES = set(string.whitespace)


def _grab_key(i: int, source: str) -> tuple[int, str]:
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


def _find_value_ends(i: int, source: str) -> int:
    try:
        c = source[i]
    except IndexError:
        raise InvalidJson
    if c == "{":
        return _advance_until_closed(i, source, "{", "}")
    elif c == "[":
        return _advance_until_closed(i, source, "[", "]")
    else:
        if c == '"':
            j = _advance_until_or_fail(i + 1, source, lambda x: x == '"')
            return j
        elif c == "t":
            _valid_while(i, source, "true")
            return i + 3
        elif c == "f":
            _valid_while(i, source, "false")
            return i + 4
        elif c == "n":
            _valid_while(i, source, "null")
            return i + 3
        elif c.isdecimal():
            j = _advance_until_or_fail(
                i, source, predicate=lambda x: x in _SPACES.union(",}]")
            )
            return j - 1
        else:
            raise InvalidJson


def _advance_until_closed(i: int, source: str, open: str, close: str) -> int:
    sum = 0
    for j in range(i, len(source)):
        c = source[j]
        if c == open:
            sum += 1
        if c == close:
            sum -= 1

        if sum == 0:
            return j
    raise InvalidJson


def _advance_until_or_fail(
    i: int,
    source: str,
    predicate: Callable[[str], bool],
    fail_predicate: Callable[[str], bool] | None = None,
) -> int:
    if fail_predicate is None:
        fail_predicate = _return_false
    for j in range(i, len(source)):
        c = source[j]
        if predicate(c):
            return j
        if fail_predicate(c):
            raise InvalidJson
    return -1


def _return_false(_: str) -> bool:
    return False


def _valid_while(i: int, source: str, expected: str) -> None:
    for j in range(len(expected)):
        if source[i + j] != expected[j]:
            raise InvalidJson
