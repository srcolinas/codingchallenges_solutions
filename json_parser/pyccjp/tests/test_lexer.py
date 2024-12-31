import pytest

from pyccjp.lexer import lex, JsonSyntax, Token


@pytest.mark.parametrize(
    "payload,expected",
    [
        ("", []),
        ("  ", []),
        ("\n", []),
        ("{", [JsonSyntax.LEFT_BRACE]),
        ("}", [JsonSyntax.RIGHT_BRACE]),
        ("{}", [JsonSyntax.LEFT_BRACE, JsonSyntax.RIGHT_BRACE]),
        ("{}\n", [JsonSyntax.LEFT_BRACE, JsonSyntax.RIGHT_BRACE]),
        ("\n{}", [JsonSyntax.LEFT_BRACE, JsonSyntax.RIGHT_BRACE]),
        ("{\n}", [JsonSyntax.LEFT_BRACE, JsonSyntax.RIGHT_BRACE]),
    ],
)
def test_handling_of_braces_and_empty_strings(payload: str, expected: list[Token]):
    tokens = lex(iter(payload))
    assert list(tokens) == expected


@pytest.mark.parametrize(
    "payload",
    [
        '{"key": "value"}',
        '{\n\t"key":"value"}',
        '{"key": "value"}\n\t',
        '{"key":\n\t"value"}',
    ],
)
def test_size_1_object_with_string_values(payload: str):
    tokens = lex(iter(payload))
    assert list(tokens) == [
        JsonSyntax.LEFT_BRACE,
        "key",
        JsonSyntax.COLON,
        "value",
        JsonSyntax.RIGHT_BRACE,
    ]


def test_size_n_object():
    tokens = lex(iter('{"key": "value", "key2": "value2"}'))
    assert list(tokens) == [
        JsonSyntax.LEFT_BRACE,
        "key",
        JsonSyntax.COLON,
        "value",
        JsonSyntax.COMMA,
        "key2",
        JsonSyntax.COLON,
        "value2",
        JsonSyntax.RIGHT_BRACE,
    ]


def test_ValueError_for_unquoted_key():
    result = lex(iter('{key: "value"}'))
    next(result)
    with pytest.raises(ValueError):
        next(result)


def test_object_with_string_numeric_or_null_values():
    tokens = lex(
        iter(
            '{"key1": true,"key2": false,"key3": null,"key4": "value","key5": 101, "key6": 3.1416}'
        )
    )
    assert list(tokens) == [
        JsonSyntax.LEFT_BRACE,
        "key1",
        JsonSyntax.COLON,
        True,
        JsonSyntax.COMMA,
        "key2",
        JsonSyntax.COLON,
        False,
        JsonSyntax.COMMA,
        "key3",
        JsonSyntax.COLON,
        None,
        JsonSyntax.COMMA,
        "key4",
        JsonSyntax.COLON,
        "value",
        JsonSyntax.COMMA,
        "key5",
        JsonSyntax.COLON,
        101,
        JsonSyntax.COMMA,
        "key6",
        JsonSyntax.COLON,
        3.1416,
        JsonSyntax.RIGHT_BRACE,
    ]
