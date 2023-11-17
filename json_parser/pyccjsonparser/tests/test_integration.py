import subprocess
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "file,exit_code",
    [
        (Path("doesnt-exist.extension"), 1),
        (Path("..") / "tests" / "step1" / "valid.json", 0),
        (Path("..") / "tests" / "step1" / "invalid.json", 2),
    ],
)
def test(file: Path, exit_code: int, program: str):
    proc = subprocess.run(f"{program} {file}")
    assert proc.returncode == exit_code


@pytest.fixture()
def program():
    subprocess.run("poetry shell")
    return "pyccjsonparser"
