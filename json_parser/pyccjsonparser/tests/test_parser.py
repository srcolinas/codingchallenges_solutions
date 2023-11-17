from pyccjsonparser.parser import parse


def test_empty_object():
    assert {} == parse("\{\}")
