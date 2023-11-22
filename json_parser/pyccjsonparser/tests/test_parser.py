from typing import Any

import pytest

from pyccjsonparser.parser import parse, InvalidJson


def test_empty_string():
    with pytest.raises(InvalidJson):
        parse("")


@pytest.mark.parametrize(
    "input, output",
    [
        ("{}", {}),
        ('{"key": "value"}', {"key": "value"}),
        ('{  "k ey"   :    "val\tue"  \n}', {"k ey": "val\tue"}),
        ('{"key": "value","key2": "value"}', {"key": "value", "key2": "value"}),
    ],
)
def test_valid_cases(input: str, output: dict[str, Any]):
    assert output == parse(input)


@pytest.mark.parametrize(
    "input",
    [
        "",
    ],
)
def test_invalid_cases(input: str):
    with pytest.raises(InvalidJson):
        parse(input)
