import sys
from pathlib import Path

from pyccjsonparser.parser import parse, InvalidJson


def main(file: Path):
    if not file.exists():
        return 1
    try:
        parse(file.read_text())
    except InvalidJson:
        return 2
    return 0


def _cli() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)

    args = parser.parse_args()

    code = main(args.file)
    sys.exit(code)


if __name__ == "__main__":
    _cli()
