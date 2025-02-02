import pathlib

from src import main


def test_return_1_if_file_doesnot_exist(tmp_path: pathlib.Path):
    filepath = tmp_path / "doesnot_exist.json"

    code = main.main(filepath)

    assert code == 1


def test_return_0_if_everything_goes_well(tmp_path: pathlib.Path):
    filepath = tmp_path / "test.json"
    filepath.write_text("aabb")

    code = main.main(filepath)

    assert code == 0


def test_target_file_is_written(tmp_path: pathlib.Path):
    filepath = tmp_path / "book.txt"
    filepath.write_text("aaabb")

    main.main(filepath)
    assert (tmp_path / "book.txt.pyccct").is_file()


def test_written_file_contains_header(tmp_path: pathlib.Path):
    filepath = tmp_path / "book.txt"
    filepath.write_text("aaabb")

    main.main(filepath)
    content = (tmp_path / "book.txt.pyccct").read_bytes()
    header, _ = content.split(b"\n**\n")
    assert b"a" in header
    assert b"b" in header


def test_written_file_contains_payload(tmp_path: pathlib.Path):
    filepath = tmp_path / "book.txt"
    filepath.write_text("a")

    main.main(filepath)
    content = (tmp_path / "book.txt.pyccct").read_bytes()
    _, payload = content.split(b"\n**\n")
    assert b"\x02" in payload


def test_there_is_compression(tmp_path: pathlib.Path):
    filepath = tmp_path / "book.txt"
    filepath.write_text("aaaaaaaaabbbbbbbbbbb")

    main.main(filepath)
    assert (
        tmp_path / "book.txt.pyccct"
    ).stat().st_size < filepath.stat().st_size


def test_file_uncompress_restores_file(tmp_path: pathlib.Path):
    filepath = tmp_path / "book.txt.pyccct"
    filepath.write_bytes(b"a-\x00\n**\n\x00")

    main.main(filepath)
    assert filepath.is_file()


def test_file_is_recovered(tmp_path: pathlib.Path):
    filepath = tmp_path / "book.txt.pyccct"
    filepath.write_bytes(b"a-\x00\n**\n\x02")

    main.main(filepath)
    assert (tmp_path / "book.txt").read_text("utf-8-sig") == "a"


def test_small_phrase(tmp_path: pathlib.Path):
    reference = tmp_path / "book.clean.txt"
    reference.write_text("The Project", "utf-8-sig")

    source = tmp_path / "book.txt"
    source.write_text("The Project", "utf-8-sig")

    main.main(source)
    main.main(tmp_path / "book.txt.pyccct")

    assert source.read_text() == reference.read_text()
