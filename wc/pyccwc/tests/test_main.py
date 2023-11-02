from io import StringIO

import pytest

from pyccwc.main import count_in_stream, format, Counts


def test_only_byte_count():
    result = count_in_stream(StringIO("aa\x01\x02b桜"), count_bytes=True)
    assert result == Counts(bytes=8)


def test_only_number_of_lines():
    result = count_in_stream(StringIO("first\nthree\nlines"), count_lines=True)
    assert result == Counts(lines=3)


@pytest.mark.parametrize(
    "content,num", [("pa la \t bro\n ta", 4), ("pa la \t bro\n ta\r", 4)]
)
def test_only_number_of_words(content: str, num: int):
    result = count_in_stream(StringIO(content), count_words=True)
    assert result == Counts(words=num)


def test_only_number_of_characters():
    result = count_in_stream(StringIO("桜の花abc"), count_characters=True)
    assert result == Counts(characters=6)


def test_default():
    result = count_in_stream(StringIO("桜の花abc\n asdf\x01\t\x02\x03"))
    assert result == Counts(lines=2, words=3, bytes=22)


@pytest.mark.parametrize(
    "input,extra,output",
    [
        (Counts(lines=4), "", "4  "),
        (Counts(words=5), "", "5  "),
        (Counts(bytes=6), "", "6  "),
        (Counts(characters=7), "", "7  "),
        (Counts(lines=4, words=5), "", "4  5  "),
        (Counts(lines=4, bytes=7), "", "4  7  "),
        (Counts(lines=4, words=5, characters=6), "", "4  5  6  "),
        (Counts(lines=4, words=5, bytes=7), "", "4  5  7  "),
        (Counts(lines=4, words=5, characters=6, bytes=7), "", "4  5  6  7  "),
    ],
)
def test_format(input: Counts, extra: str, output: str):
    assert format(input, extra=extra) == output
