import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO


@dataclass(frozen=True, slots=True)
class Counts:
    bytes: int | None = None
    lines: int | None = None
    words: int | None = None
    characters: int | None = None


def count_in_stream(
    file: TextIO,
    *,
    count_bytes: bool = False,
    count_lines: bool = False,
    count_words: bool = False,
    count_characters: bool = False,
) -> Counts:
    default = (
        not count_bytes and not count_lines and not count_words and not count_characters
    )

    num_lines = 0 if count_lines or default else None
    num_words = 0 if count_words or default else None
    num_characters = 0 if count_characters else None
    num_bytes = 0 if count_bytes or default else None

    for line in file:
        if num_lines is not None:
            num_lines += 1
        if num_words is not None:
            num_words += len(line.split())
        if num_characters is not None:
            num_characters += len(line)
        if num_bytes is not None:
            num_bytes += len(line.encode())

    return Counts(
        bytes=num_bytes, lines=num_lines, words=num_words, characters=num_characters
    )


def format(c: Counts, *, extra: str = "") -> str:
    result = ""
    if c.lines is not None:
        result += f"{c.lines}  "
    if c.words is not None:
        result += f"{c.words}  "
    if c.characters is not None:
        result += f"{c.characters}  "
    if c.bytes is not None:
        result += f"{c.bytes}  "
    result += extra
    return result


def main(
    file: TextIO,
    *,
    count_bytes: bool = False,
    count_lines: bool = False,
    count_words: bool = False,
    count_characters: bool = False,
    extra: str = "",
    write_to: TextIO = sys.stdout,
) -> None:
    
    
    counts = count_in_stream(
        file,
        count_bytes=count_bytes,
        count_lines=count_lines,
        count_words=count_words,
        count_characters=count_characters,
    )

    result = format(counts, extra=extra)
    print(result, file=write_to)
    file.close()


def _cli():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=Path, nargs="?", default=None)
    parser.add_argument("-c", dest="count_bytes", action="store_true", default=False)
    parser.add_argument("-l", dest="count_lines", action="store_true", default=False)
    parser.add_argument("-w", dest="count_words", action="store_true", default=False)
    parser.add_argument(
        "-m", dest="count_characters", action="store_true", default=False
    )
    args = parser.parse_args()
    if not sys.stdin.isatty():
        file, name = sys.stdin, ""
    else:
        filepath: Path | None = args.filepath
        if filepath is None:
            sys.exit(1)
        elif filepath.is_dir():
            print(f"pyccwc: {filepath} is a directory")
            sys.exit(2)
        file, name = open(filepath), str(filepath)

    main(
        file,
        count_bytes=args.count_bytes,
        count_lines=args.count_lines,
        count_words=args.count_words,
        count_characters=args.count_characters,
        extra=name,
        write_to=sys.stdout,
    )


if __name__ == "__main__":
    _cli()
