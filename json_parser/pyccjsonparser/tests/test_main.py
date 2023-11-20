from pathlib import Path

from pyccjsonparser.main import main


def test_file_doesnot_exists(tmp_path: Path):
    code = main(tmp_path / "non-existing")
    assert code == 1


def test_file_is_invalid_json(tmp_path: Path):
    file = tmp_path / "test.json"
    file.write_text("{")
    code = main(file)
    assert code == 2


def test_file_is_valid_json(tmp_path: Path):
    file = tmp_path / "test.json"
    file.write_text("{}")
    code = main(file)
    assert code == 0
