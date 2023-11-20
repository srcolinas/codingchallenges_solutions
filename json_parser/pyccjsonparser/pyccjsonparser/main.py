import logging
import sys
from pathlib import Path

from pyccjsonparser.parser import parse, InvalidJson


def main(file: Path):
    if not file.exists():
        logging.debug("File doesn't exists")
        return 1
    
    content = file.read_text()
    try:
        parse(content)
    except InvalidJson:
        logging.debug("File has invalid content")
        return 2

    logging.debug("File is ok")
    return 0


def _cli() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("-v", action="store_true")

    args = parser.parse_args()

    if args.v:
        logging.getLogger().setLevel(logging.DEBUG)

    code = main(args.file)
    sys.exit(code)


if __name__ == "__main__":
    _cli()
