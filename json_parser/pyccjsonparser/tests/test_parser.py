from typing import Any

import pytest

from pyccjsonparser.parser import parse, InvalidJson


@pytest.mark.parametrize(
    "input, output",
    [
        ("{}", {}),
        ('{"key": "value"}', {"key": "value"}),
        ('{  "k ey"   :    "val\tue"  \n}', {"k ey": "val\tue"}),
        ('{"key": "value",\n"key2": "value"}', {"key": "value", "key2": "value"}),
        (
            '{"key1": true, "key2": false, "key3": null, "key4": "value", "key5": 101}',
            {"key1": True, "key2": False, "key3": None, "key4": "value", "key5": 101},
        ),
        (
            '{"key": "value", "key-n": 101, "key-o": {}, "key-l": []}',
            {"key": "value", "key-n": 101, "key-o": {}, "key-l": []},
        ),
        (
            '{"key": "", "key-n": 101, "key-o": { "inner key": "inner value"},"key-l": ["list value"]}',
            {
                "key": "",
                "key-n": 101,
                "key-o": {"inner key": "inner value"},
                "key-l": ["list value"],
            },
        ),
    ],
)
def test_valid_cases(input: str, output: dict[str, Any]):
    assert output == parse(input)


@pytest.mark.parametrize(
    "input",
    [
        "",
        '""',
        '{"key": "value",}',
        '{"key": "value", key2: "value"}',
        '{"key1": true,"key2": False,"key3": null,\n "key4": "value", "key5": 101}',
        """{"key": "value","key-n": 101, "key-o": {"inner key": "inner value"}, "key-l": ['list value']}""",
    ],
)
def test_invalid_cases(input: str):
    with pytest.raises(InvalidJson):
        parse(input)
