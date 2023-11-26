from pathlib import Path

import pytest

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


@pytest.mark.parametrize(
    "file",
    [
        Path().absolute().parent / "tests" / "step1" / "valid.json",
        Path().absolute().parent / "tests" / "step2" / "valid.json",
        Path().absolute().parent / "tests" / "step2" / "valid2.json",
        Path().absolute().parent / "tests" / "step3" / "valid.json",
        Path().absolute().parent / "tests" / "step4" / "valid.json",
        Path().absolute().parent / "tests" / "step4" / "valid2.json",
    ],
)
def test_valid_files(file):
    assert 0 == main(file)


@pytest.mark.parametrize(
    "file",
    [
        Path().absolute().parent / "tests" / "step1" / "invalid.json",
        Path().absolute().parent / "tests" / "step2" / "invalid.json",
        Path().absolute().parent / "tests" / "step2" / "invalid2.json",
        Path().absolute().parent / "tests" / "step3" / "invalid.json",
        Path().absolute().parent / "tests" / "step4" / "invalid.json",
    ],
)
def test_invalid_files(file):
    assert 2 == main(file)


def test_extra_files(pytestconfig: pytest.Config):
    dirname = pytestconfig.getoption("extra", None)
    if dirname is None:
        return
    for filepath in Path(dirname).glob("*.json"):
        if filepath.name.startswith("fail"):
            assert 2 == main(filepath)
        elif filepath.name.startswith("pass"):
            assert 0 == main(filepath)
