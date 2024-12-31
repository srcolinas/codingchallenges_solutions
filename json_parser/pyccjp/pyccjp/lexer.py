from collections.abc import Iterator
from .parser import Token, JsonSyntax


def lex(payload: Iterator[str]) -> Iterator[Token]:
    for idx, c in enumerate(payload):
        # Match symbols and yield corresponding tokens
        if c == "{":
            yield JsonSyntax.LEFT_BRACE
        elif c == "}":
            yield JsonSyntax.RIGHT_BRACE
        elif c == "[":
            yield JsonSyntax.LEFT_BRACKET
        elif c == "]":
            yield JsonSyntax.RIGHT_BRACKET
        elif c == ":":
            yield JsonSyntax.COLON
        elif c == ",":
            yield JsonSyntax.COMMA
        elif c == '"':
            yield _lex_string(payload)
        elif c == "t":
            yield _lex_true(payload)
        elif c == "f":
            yield _lex_false(payload)
        elif c == "n":
            next(payload), next(payload), next(payload)
            yield None
        elif c in _SPACES:
            continue  # Skip white space characters
        elif c in _NUMERIC_CHARACTERS or c == "-":
            # Lex numeric value and continue depending on next character
            number, next_char = _lex_numeric(payload, c)
            yield number
            yield from _handle_followup_characters(next_char, payload)
        else:
            # Raise an error for invalid characters
            raise ValueError(_ERROR_MSG.format(character=c, index=idx))


def _handle_followup_characters(
    next_char: str, payload: Iterator[str]
) -> Iterator[Token]:
    """
    Handle possible follow-up characters after a number is lexed.
    Yield the appropriate token based on the next character.
    """
    if next_char == '"':
        yield _lex_string(payload)
    elif next_char == "}":
        yield JsonSyntax.RIGHT_BRACE
    elif next_char == "]":
        yield JsonSyntax.RIGHT_BRACKET
    elif next_char == ",":
        yield JsonSyntax.COMMA
    else:
        raise ValueError(f"Unexpected character after number: {next_char}")


def _lex_true(payload: Iterator[str]) -> bool:
    """Lex the 'true' boolean value."""
    next(payload), next(payload), next(payload)
    return True


def _lex_false(payload: Iterator[str]) -> bool:
    """Lex the 'false' boolean value."""
    (
        next(payload),
        next(payload),
        next(payload),
        next(payload),
    )
    return False


def _lex_string(payload: Iterator[str]) -> str:
    """Lex a string enclosed in double quotes."""
    content = ""
    for c in payload:
        if c == '"':
            break
        if not c.isalnum() and c not in _VALID_NON_ALPHANUMERIC_CHARACTERS:
            raise ValueError
        content += c
    return content


_VALID_NON_ALPHANUMERIC_CHARACTERS = {"-", " "}


def _lex_numeric(payload: Iterator[str], c: str) -> tuple[float | int, str]:
    """Lex a numeric value, handling both integers and floats."""
    number = c
    for c in payload:
        if c not in _NUMERIC_CHARACTERS:
            break
        number += c

    # Check for decimal point and continue lexing for a floating-point number
    if c == ".":
        number += c
        for c in payload:
            if c not in _NUMERIC_CHARACTERS:
                break
            number += c
        return float(number), c

    if number.startswith("0"):
        raise ValueError("integer values shouldn't start with 0")
    return int(number), c


# Constants for numeric characters and spaces
_NUMERIC_CHARACTERS = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
_SPACES = {" ", "\t", "\n"}
_ERROR_MSG = "Character {character} at index {index} is not valid"
