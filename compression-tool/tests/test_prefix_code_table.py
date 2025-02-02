from src.huffman import HuffmanTree, create_prefix_code_table


def test_handles_single_element():
    tree = HuffmanTree(weight=3, key="a")
    table = create_prefix_code_table(tree)
    assert table == {"a": "0"}


def test_handles_two_elements():
    tree = HuffmanTree(
        weight=7,
        children=(
            HuffmanTree(weight=4, key="b"),
            HuffmanTree(weight=3, key="a"),
        ),
    )
    table = create_prefix_code_table(tree)
    assert table == {"a": "1", "b": "0"}


def test_handles_three_elements():
    tree = HuffmanTree(
        weight=33,
        children=(
            HuffmanTree(
                weight=9,
                children=(
                    HuffmanTree(weight=2, key="z"),
                    HuffmanTree(weight=7, key="k"),
                ),
            ),
            HuffmanTree(weight=24, key="m"),
        ),
    )
    table = create_prefix_code_table(tree)
    assert table == {"z": "00", "k": "01", "m": "1"}
