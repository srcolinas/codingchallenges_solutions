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
    
    _consume_until_end(tokens)
    return result

def _consume_until_end(tokens: Iterator[Token]) -> None:
    i = -1
    for i, t in enumerate(tokens):
        if i > 0:
            raise ValueError(f"incorrect finish token")
        if t is JsonSyntax.RIGHT_BRACE:
            break
    else:
        if i > -1:
            raise ValueError(f"incorrect finish token")
    for t in tokens:
        raise ValueError(f"incorrect finish token")
            

def _parse_object(tokens: Iterator[Token]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in tokens:
        if key is JsonSyntax.RIGHT_BRACE:
            break
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

    return result


def _parse_array(tokens: Iterator[Token]) -> list[Any]:
    result: list[Any] = []
    for t in tokens:
        if t is JsonSyntax.RIGHT_BRACKET:
            break
        if t is JsonSyntax.COMMA:
            continue
        value = _handle_leading_token(t, tokens)
        result.append(value)
    return result


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

