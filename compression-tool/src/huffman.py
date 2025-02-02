import dataclasses
import heapq
from collections.abc import Mapping
from typing import cast


@dataclasses.dataclass(kw_only=True)
class HuffmanTree:
    weight: int
    key: str | None = None
    children: tuple["HuffmanTree", "HuffmanTree"] | None = None

    def __lt__(self, other: "HuffmanTree") -> bool:
        return self.weight < other.weight

    @classmethod
    def from_frequenceies(cls, frequencies: Mapping[str, int]) -> "HuffmanTree":
        trees: list[HuffmanTree] = []
        for k, v in frequencies.items():
            heapq.heappush(trees, cls(weight=v, key=k))

        while len(trees) > 1:
            left = heapq.heappop(trees)
            right = heapq.heappop(trees)
            heapq.heappush(
                trees,
                cls(weight=left.weight + right.weight, children=(left, right)),
            )
        return trees.pop()


def create_prefix_code_table(tree: HuffmanTree) -> dict[str, str]:
    if tree.children is None:
        key = cast(str, tree.key)
        return {key: "0"}

    result = {}
    stack = [(tree, "")]
    while stack:
        root, code = stack.pop()
        if root.children is not None:
            left, right = root.children
            stack.append((left, code + "0"))
            stack.append((right, code + "1"))
            continue
        assert root.key is not None
        result[root.key] = code
    return result
