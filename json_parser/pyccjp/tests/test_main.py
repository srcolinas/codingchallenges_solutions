import pathlib

import pytest

from pyccjp import main


@pytest.mark.parametrize(
    "payload",
    [
        "",
        '{"key": "value",}',
        '{"key": "value", key2: "value"}',
        '{"key1": true,"key2": False,"key3": null,"key4": "value","key5": 101}',
        '{"key": "value","key-n": 101,"key-o": {"inner key": "inner value"}, "key-l": [\'list value\']}',
        '[""'
    ],
)
def test_1_for_invalid_json(payload: str, tmp_path: pathlib.Path):
    filepath = tmp_path / "invalid.json"
    filepath.write_text(payload)

    code = main.main(filepath)
    assert code == 1


def test_2_for_file_doesnot_exist(tmp_path: pathlib.Path):
    filepath = tmp_path / "doesnot_exist.json"

    code = main.main(filepath)

    assert code == 2


@pytest.mark.parametrize(
    "payload",
    [
        "{}",
        '{"key": "value"}',
        '{"key": "value","key2": "value"}',
        '{"key1": true,"key2": false,"key3": null,"key4": "value","key5": 101}',
        '{"key": "value","key-n": 101,"key-o": {}, "key-l": []}',
        '{"key": "","key-n": 101,"key-o": {"inner key": "inner value"},"key-l": ["list value"]}',
    ],
)
def test_0_for_valid_json(payload: str, tmp_path: pathlib.Path):
    filepath = tmp_path / "valid.json"
    filepath.write_text(payload)

    code = main.main(filepath)

    assert code == 0
