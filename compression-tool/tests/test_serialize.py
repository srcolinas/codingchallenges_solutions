import pytest
from src import serialize
from src.huffman import HuffmanTree


def test_first_byte_starts_with_extra_on_bit():
    result = serialize.create_payload("a", {"a": "1" * 7})
    assert result == b"\xff"


def test_last_byte_appears_first():
    result = serialize.create_payload("ab", {"a": "0" * 8, "b": "1" * 7})
    assert result == b"\xff\x00"


def test_small_payload_codes_are_grouped_in_bytes():
    result = serialize.create_payload("abc", {"a": "1", "b": "111", "c": "111"})
    assert result == b"\xff"


def test_big_payload_codes_are_grouped_in_bytes():
    result = serialize.create_payload("a", {"a": "0" * 8 + "1" * 7})
    assert result == b"\xff\x00"


def test_restore_payload_ignores_leading_bit_and_turns_left():
    result = serialize.restore_payload(
        int("10", 2).to_bytes(1),
        HuffmanTree(
            weight=-1,
            children=(
                HuffmanTree(weight=-1, key="a"),
                HuffmanTree(weight=-1, key="b"),
            ),
        ),
    )
    assert result == "a"


def test_restore_payload_ignores_leading_bit_and_turns_right():
    result = serialize.restore_payload(
        int("11", 2).to_bytes(1),
        HuffmanTree(
            weight=-1,
            children=(
                HuffmanTree(weight=-1, key="a"),
                HuffmanTree(weight=-1, key="b"),
            ),
        ),
    )
    assert result == "b"


def test_restore_payload_with_left_loaded_tree():
    result = serialize.restore_payload(
        b"#",
        HuffmanTree(
            weight=-1,
            children=(
                HuffmanTree(
                    weight=-1,
                    children=(
                        HuffmanTree(weight=-1, key="a"),
                        HuffmanTree(weight=-1, key="b"),
                    ),
                ),
                HuffmanTree(weight=-1, key="c"),
            ),
        ),
    )
    assert result == "abc"


def test_restore_payload_with_right_loaded_tree():
    result = serialize.restore_payload(
        b"6",
        HuffmanTree(
            weight=-1,
            children=(
                HuffmanTree(weight=-1, key="s"),
                HuffmanTree(
                    weight=-1,
                    children=(
                        HuffmanTree(weight=-1, key="L"),
                        HuffmanTree(weight=-1, key="e"),
                    ),
                ),
            ),
        ),
    )
    assert result == "Les"


@pytest.mark.parametrize(
    "frequencies,header",
    [
        ({"a": 12}, b"a-\x0c"),
        ({"a": 256}, b"a-\x01\x00"),
        ({"a": 12, "b": 256}, b"a-\x0c,b-\x01\x00"),
        ({"á": 1}, b"\xc3\xa1-\x01"),
    ],
)
def test_header_values(frequencies: dict[str, int], header: bytes):
    result = serialize.create_header(frequencies)
    assert result.startswith(header)
    assert result.endswith(b"\n**\n")


def test_header_doesnot_write_content():
    header = serialize.create_header({"a": 0})
    _, content = header.split(b"\n**\n")
    assert content == b""


@pytest.mark.parametrize(
    "frequencies,header",
    [
        ({"a": 12}, b"a-\x0c"),
        ({"a": 256}, b"a-\x01\x00"),
        ({"a": 12, "b": 256}, b"a-\x0c,b-\x01\x00"),
        ({"á": 1}, b"\xc3\xa1-\x01"),
        ({"a": 1, ",": 12}, b"a-\x01,,-\x0c"),
        ({"a": 1, "-": 12}, b"a-\x01,--\x0c"),
    ],
)
def test_restored_frequencies_values(
    frequencies: dict[str, int], header: bytes
):
    result = serialize.restore_frequencies(header)
    assert result == frequencies
