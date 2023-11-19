from pyccjsonparser.parser import parse, InvalidJson

import pytest


def test_empty_string():
    with pytest.raises(InvalidJson):
        parse("")


def test_empty_object():
    assert {} == parse("\{\}")
