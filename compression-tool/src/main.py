import collections
import pathlib
from typing import cast

from src import huffman, serialize


def main(file: pathlib.Path) -> int:
    if not file.exists():
        return 1

    if file.suffix == ".pyccct":
        return _uncompress(file)
    return _compress(file)


def _compress(file: pathlib.Path) -> int:
    content = file.read_text("utf-8-sig")

    counts = cast(dict[str, int], collections.Counter(content))
    tree = huffman.HuffmanTree.from_frequenceies(counts)
    table = cast(dict[str, str], huffman.create_prefix_code_table(tree))

    header = serialize.create_header(counts)
    payload = serialize.create_payload(content, table)
    newfile = file.with_suffix(file.suffix + ".pyccct")
    newfile.write_bytes(header + payload)
    return 0


def _uncompress(file: pathlib.Path) -> int:
    content = file.read_bytes()

    header, payload = content.split(b"\n**\n")

    frequencies = serialize.restore_frequencies(header)
    tree = huffman.HuffmanTree.from_frequenceies(frequencies)
    source = serialize.restore_payload(payload, tree)

    newfile = file.with_suffix("")
    newfile.write_text(source, "utf-8-sig")
    return 0


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
