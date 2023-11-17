# import subprocess
# import sys
# from pathlib import Path

# import pytest


# @pytest.mark.parametrize(
#     "file,exit_code",
#     [
#         (Path("doesnt-exist.extension"), 1),
#         (Path("..") / "tests" / "step1" / "valid.json", 0),
#         (Path("..") / "tests" / "step1" / "invalid.json", 2),
#     ],
# )
# def test(file: Path, exit_code: int):
#     proc = subprocess.run(["pyccjsonparser", f"{file}"], executable=sys.executable)
#     assert proc.returncode == exit_code
