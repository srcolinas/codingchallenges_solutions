from pyccwc.main import main

import pytest


def test_only_byte_count():
    result = main("aa\x01\x02b桜", count_bytes=True)
    assert result == "  8 "


def test_only_number_of_lines():
    result = main("first\nthree\nlines", count_lines=True)

    assert result == "  3  "


@pytest.mark.parametrize(
    "content,num", [("pa la \t bro\n ta", 4), ("pa la \t bro\n ta\r", 4)]
)
def test_only_number_of_words(content: str, num: int):
    result = main(content, count_words=True)

    assert result == f"  {num} "


def test_only_number_of_characters():
    result = main("桜の花abc", count_characters=True)

    assert result == "  6 "


def test_default():
    result = main("桜の花abc\n asdf\x01\t\x02\x03")

    assert result == "  2  3 22 "


def test_filepath_is_appended():
    result = main("桜の花abc\n asdf\x01\t\x02\x03", filepath="text.txt")

    assert result == "  2  3 22 text.txt"