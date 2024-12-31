import pytest

from pyccjp.parser import parse, JsonSyntax, Token


@pytest.mark.parametrize(
    "tokens",
    [
        [],
        [JsonSyntax.RIGHT_BRACE],
        [JsonSyntax.RIGHT_BRACE, JsonSyntax.LEFT_BRACE],
        [JsonSyntax.LEFT_BRACE, JsonSyntax.COLON],
        [JsonSyntax.LEFT_BRACE, JsonSyntax.COMMA],
        [JsonSyntax.LEFT_BRACE, JsonSyntax.RIGHT_BRACE, JsonSyntax.COMMA],
        [JsonSyntax.LEFT_BRACE, "key", JsonSyntax.RIGHT_BRACE],
        [JsonSyntax.LEFT_BRACE, "key", JsonSyntax.COMMA, JsonSyntax.RIGHT_BRACE],
        [JsonSyntax.RIGHT_BRACKET],
        [JsonSyntax.RIGHT_BRACKET, JsonSyntax.LEFT_BRACKET],
        [JsonSyntax.LEFT_BRACKET, JsonSyntax.COLON],
        [JsonSyntax.LEFT_BRACKET, JsonSyntax.COMMA],
        [JsonSyntax.LEFT_BRACKET, "key"],
        [JsonSyntax.LEFT_BRACKET, "key", JsonSyntax.COMMA, JsonSyntax.RIGHT_BRACKET],
        [JsonSyntax.LEFT_BRACKET, JsonSyntax.RIGHT_BRACKET, JsonSyntax.COMMA],
        [JsonSyntax.LEFT_BRACKET, JsonSyntax.COMMA, "key", JsonSyntax.RIGHT_BRACKET],
    ],
)
def test_ValueError_for_invalid_input(tokens: list[Token]):
    tokens = iter(tokens)
    with pytest.raises(ValueError):
        parse(tokens)


def test_parses_empty_object():
    object = parse(iter([JsonSyntax.LEFT_BRACE, JsonSyntax.RIGHT_BRACE]))
    assert object == {}


@pytest.mark.parametrize("value", [True, False, 3, 3.14, "pi", None])
def test_parses_object_with_scalar_value_types(value: bool | int | float | str | None):
    iterator = iter(
        [
            JsonSyntax.LEFT_BRACE,
            "key",
            JsonSyntax.COLON,
            value,
            JsonSyntax.RIGHT_BRACE,
        ]
    )

    assert parse(iterator) == {"key": value}


def test_parses_object_with_multiple_scalar_values():
    iterator = iter(
        [
            JsonSyntax.LEFT_BRACE,
            "true",
            JsonSyntax.COLON,
            True,
            JsonSyntax.COMMA,
            "false",
            JsonSyntax.COLON,
            False,
            JsonSyntax.COMMA,
            "null",
            JsonSyntax.COLON,
            None,
            JsonSyntax.COMMA,
            "float",
            JsonSyntax.COLON,
            3.14,
            JsonSyntax.COMMA,
            "int",
            JsonSyntax.COLON,
            3,
            JsonSyntax.COMMA,
            "string",
            JsonSyntax.COLON,
            "pi",
            JsonSyntax.RIGHT_BRACE,
        ]
    )

    assert parse(iterator) == {
        "true": True,
        "false": False,
        "null": None,
        "float": 3.14,
        "int": 3,
        "string": "pi",
    }


@pytest.mark.parametrize("value", [True, False, 3, 3.14, "pi", None])
def test_parses_array_with_scalar_value_types(value: bool | int | float | str | None):
    iterator = iter(
        [
            JsonSyntax.LEFT_BRACKET,
            value,
            JsonSyntax.RIGHT_BRACKET,
        ]
    )

    assert parse(iterator) == [value]


def test_parses_array_with_multiple_scalar_values():
    iterator = iter(
        [
            JsonSyntax.LEFT_BRACKET,
            True,
            JsonSyntax.COMMA,
            False,
            JsonSyntax.COMMA,
            None,
            JsonSyntax.COMMA,
            3.14,
            JsonSyntax.COMMA,
            3,
            JsonSyntax.COMMA,
            "pi",
            JsonSyntax.RIGHT_BRACKET,
        ]
    )

    assert parse(iterator) == [True, False, None, 3.14, 3, "pi"]


def test_parses_object_with_empty_object_value():
    iterator = iter(
        [
            JsonSyntax.LEFT_BRACE,
            "key",
            JsonSyntax.COLON,
            JsonSyntax.LEFT_BRACE,
            JsonSyntax.RIGHT_BRACE,
            JsonSyntax.RIGHT_BRACE,
        ]
    )

    assert parse(iterator) == {"key": {}}


def test_parses_object_with_empty_array_value():
    iterator = iter(
        [
            JsonSyntax.LEFT_BRACE,
            "key",
            JsonSyntax.COLON,
            JsonSyntax.LEFT_BRACKET,
            JsonSyntax.RIGHT_BRACKET,
            JsonSyntax.RIGHT_BRACE,
        ]
    )

    assert parse(iterator) == {"key": []}


def test_parses_object_in_list():
    iterator = iter(
        [
            JsonSyntax.LEFT_BRACKET,
            JsonSyntax.LEFT_BRACE,
            JsonSyntax.RIGHT_BRACE,
            JsonSyntax.RIGHT_BRACKET,
        ]
    )

    assert parse(iterator) == [{}]


def test_parses_arbitrary_object():
    iterator = iter(
        [
            JsonSyntax.LEFT_BRACE,
            "values",
            JsonSyntax.COLON,
            JsonSyntax.LEFT_BRACKET,
            JsonSyntax.LEFT_BRACE,
            "booleans",
            JsonSyntax.COLON,
            JsonSyntax.LEFT_BRACE,
            "true",
            JsonSyntax.COLON,
            True,
            JsonSyntax.COMMA,
            "false",
            JsonSyntax.COLON,
            False,
            JsonSyntax.RIGHT_BRACE,
            JsonSyntax.RIGHT_BRACE,
            JsonSyntax.COMMA,
            JsonSyntax.LEFT_BRACE,
            "null",
            JsonSyntax.COLON,
            None,
            JsonSyntax.RIGHT_BRACE,
            JsonSyntax.COMMA,
            JsonSyntax.LEFT_BRACE,
            "numbers",
            JsonSyntax.COLON,
            JsonSyntax.LEFT_BRACE,
            "float",
            JsonSyntax.COLON,
            3.14,
            JsonSyntax.COMMA,
            "int",
            JsonSyntax.COLON,
            3,
            JsonSyntax.COMMA,
            "string",
            JsonSyntax.COLON,
            "pi",
            JsonSyntax.RIGHT_BRACE,
            JsonSyntax.RIGHT_BRACE,
            JsonSyntax.RIGHT_BRACKET,
            JsonSyntax.RIGHT_BRACE,
        ]
    )

    assert parse(iterator) == {
        "values": [
            {"booleans": {"true": True, "false": False}},
            {"null": None},
            {"numbers": {"float": 3.14, "int": 3, "string": "pi"}},
        ]
    }
