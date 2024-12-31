import enum
from collections.abc import Iterator
from typing import Annotated, Any


class JsonSyntax(enum.Enum):
    LEFT_BRACE = 0
    RIGHT_BRACE = 1
    COLON = 2
    COMMA = 3
    LEFT_BRACKET = 4
    RIGHT_BRACKET = 5


type Token = (
    JsonSyntax
    | Annotated[str, "used for keys or string values only"]
    | float
    | int
    | bool
    | None
)


def parse(
    tokens: Iterator[Token],
) -> dict[str, Any] | list[Any]:
    try:
        lead = next(tokens)
    except StopIteration:
        raise ValueError
    if lead is JsonSyntax.LEFT_BRACE:
        result = _parse_object(tokens)
    elif lead is JsonSyntax.LEFT_BRACKET:
        result = _parse_array(tokens)
    else:
        raise ValueError(f"invalid leading token {lead}")
    for t in tokens:
        raise ValueError(f"invalid end character {t}")
    return result


def _parse_object(tokens: Iterator[Token]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in tokens:
        if key is JsonSyntax.RIGHT_BRACE:
            return result
        if key is JsonSyntax.COMMA:
            try:
                key = next(tokens)
            except StopIteration:
                raise ValueError

        if not isinstance(key, str):
            raise ValueError(f"key {key} should be a string")

        if next(tokens) is not JsonSyntax.COLON:
            raise ValueError

        value = _handle_leading_token(next(tokens), tokens)
        result[key] = value
    raise ValueError


def _parse_array(tokens: Iterator[Token]) -> list[Any]:
    result: list[Any] = []
    tail_is_comma = False
    for t in tokens:
        if t is JsonSyntax.RIGHT_BRACKET:
            if tail_is_comma:
                raise ValueError(
                    "the last element of an array should be a value, got comma"
                )
            return result
        if t is JsonSyntax.COMMA:
            if not result:
                raise ValueError("comma was found before value in list")
            tail_is_comma = True
            continue
        value = _handle_leading_token(t, tokens)
        result.append(value)
        tail_is_comma = False
    raise ValueError


def _handle_leading_token(
    t: Token, tokens: Iterator[Token]
) -> dict[str, Any] | list[Any] | str | bool | int | float | None:
    if t is JsonSyntax.LEFT_BRACE:
        return _parse_object(tokens)
    elif t is JsonSyntax.LEFT_BRACKET:
        return _parse_array(tokens)
    elif isinstance(t, (str, bool, int, float)) or t is None:
        return t
    raise ValueError(f"got {t}")
