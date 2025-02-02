from typing import cast

from src.huffman import HuffmanTree


def test_build_with_single_element_has_no_children():
    tree = HuffmanTree.from_frequenceies({"a": 3})
    assert tree.children is None


def test_build_with_single_element_has_right_weight():
    tree = HuffmanTree.from_frequenceies({"a": 3})
    assert tree.weight == 3


def test_build_from_two_elements_has_right_weight():
    tree = HuffmanTree.from_frequenceies({"a": 3, "b": 4})
    left, right = cast(tuple[HuffmanTree, HuffmanTree], tree.children)
    assert tree.weight == 7
    assert left.weight == 3
    assert right.weight == 4


def test_build_from_three_elements():
    tree = HuffmanTree.from_frequenceies({"z": 2, "k": 7, "m": 24})
    subtree, first = cast(tuple[HuffmanTree, HuffmanTree], tree.children)
    second, thrid = cast(tuple[HuffmanTree, HuffmanTree], subtree.children)

    assert tree.weight == 33
    assert tree.key is None

    assert subtree.key is None
    assert subtree.weight == 9
    assert subtree.children is not None

    assert first.key == "m"
    assert first.children is None
    assert first.weight == 24

    assert second.key == "z"
    assert second.children is None
    assert second.weight == 2

    assert thrid.key == "k"
    assert thrid.children is None
    assert thrid.weight == 7
