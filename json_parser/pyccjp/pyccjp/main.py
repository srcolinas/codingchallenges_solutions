import pathlib
from collections.abc import Iterator

from . import lexer, parser


def main(file: pathlib.Path) -> int:
    if not file.exists():
        print("File doesn't exist")
        return 2

    try:
        parser.parse(lexer.lex(_character_iterator(file)))
    except ValueError as e:
        print(f"File has invalid content, got error {e}")
        return 1

    return 0


def _character_iterator(file: pathlib.Path) -> Iterator[str]:
    with open(file, "r") as f:
        for line in f:
            for c in line:
                yield c


def _cli() -> None:
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=pathlib.Path)
    args = parser.parse_args()
    code = main(args.file)
    sys.exit(code)


if __name__ == "__main__":
    _cli()
