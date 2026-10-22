import heapq
from typing import Optional

from huffman.HuffmanNode import HuffmanNode


class HuffmanTree:
    def __init__(self, frequencies: dict[int, int]):
        self.frequencies = frequencies
        self.root: Optional["HuffmanNode"] = None
        self.codes: dict[int, str] = {}
        self.build_tree()

    def build_tree(self):
        min_heap: list[HuffmanNode] = []
        for byte_value, frequency in self.frequencies.items():
            node = HuffmanNode.leaf(
                frequency=frequency,
                byte_value=byte_value
            )
            heapq.heappush(min_heap, node)

        if not min_heap:
            self.root = None
            return

        while len(min_heap) > 1:
            left = heapq.heappop(min_heap)
            right = heapq.heappop(min_heap)

            parent = HuffmanNode.parent(
                left=left,
                right=right
            )
            heapq.heappush(min_heap, parent)

        self.root = min_heap[0]
        return

    def build_code(self) -> dict[int, str]:
        if self.root is None:
            return {}

        if self.root.is_leaf():
            assert self.root.byte_value is not None
            self.codes[self.root.byte_value] = "0"
            return self.codes

        def dfs(node: HuffmanNode, current_code: str) -> None:
            if node.is_leaf():
                assert node.byte_value is not None
                self.codes[node.byte_value] = current_code
                return

            if node.left is not None:
                dfs(node.left, current_code + "0")

            if node.right is not None:
                dfs(node.right, current_code + "1")

        dfs(self.root, "")
        return self.codes