import os
import sys
from pathlib import Path
from tempfile import TemporaryFile


def main(
    text: str,
    *,
    count_bytes: bool = False,
    count_lines: bool = False,
    count_words: bool = False,
    count_characters: bool = False,
    filepath: str = "",
) -> str:
    default = (
        not count_bytes and not count_lines and not count_words and not count_characters
    )
    result = "  "

    if count_lines or default:
        num_lines = len(text.splitlines())
        result += f"{num_lines}  "

    if count_words or default:
        word_separators = {"\n", "\r", "\t", "", " "}
        num_words = 0 if text[-1] in word_separators else 1
        in_word = True
        for c in text:
            if c in word_separators:
                if in_word:
                    num_words += 1
                in_word = False
            else:
                in_word = True
        result += f"{num_words} "

    if count_bytes or default:
        num_bytes = len(bytes(text, encoding="utf-8"))
        result += f"{num_bytes} "

    if count_characters:
        num_chars = len(text)
        result += f"{num_chars} "

    result += f"{filepath}"
    return result


def _read_text(filepath: Path | None) -> tuple[str, str]:
    if filepath is None:
        sys.stdin = TemporaryFile()
        return os.fdopen(0).read(), ""
    return filepath.read_text(), str(filepath)

if __name__ == "__main__":
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
    text, filepath = _read_text(args.filepath)

    print(
        main(
            text,
            count_bytes=args.count_bytes,
            count_lines=args.count_lines,
            count_words=args.count_words,
            count_characters=args.count_characters,
            filepath=filepath
        )
    )
