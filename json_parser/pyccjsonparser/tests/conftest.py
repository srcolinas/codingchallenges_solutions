from pathlib import Path

import pytest


def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--extra", action="store", type=Path)
