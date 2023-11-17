import sys
from pathlib import Path

from pyccjsonparser.parser import parse, InvalidJson


def _cli() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)

    args = parser.parse_args()

    file: Path = args.file
    if not file.exists():
        sys.exit(1)
    try:
        parse(file.read_text())
    except InvalidJson:
        sys.exit(2)


if __name__ == "__main__":
    _cli()
