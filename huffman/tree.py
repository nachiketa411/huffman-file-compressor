import heapq
from typing import Optional

from huffman.node import HuffmanNode


class HuffmanTree:
    def __init__(self, frequencies: dict[int, int]):
        self.frequencies = frequencies
        self.root: Optional["HuffmanNode"] = None
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

    def generate_codes(self) -> dict[int, str]:
        codes: dict[int, str] = {}

        if self.root is None:
            return codes

        if self.root.is_leaf():
            byte_value = self.root.byte_value
            if byte_value is None:
                raise ValueError("Leaf node has no byte value")

            codes[byte_value] = "0"
            return codes

        self._generate_codes_recursive(
            node=self.root,
            current_code="",
            codes=codes
        )

        return codes

    def _generate_codes_recursive(
            self,
            node: HuffmanNode,
            current_code: str,
            codes: dict[int, str]
    ) -> None:
        if node.is_leaf():
            byte_value = node.byte_value
            if byte_value is None:
                raise ValueError("Leaf node has no byte value")

            codes[byte_value] = current_code
            return

        if node.left is not None:
            self._generate_codes_recursive(
                node.left,
                current_code + "0",
                codes
            )

        if node.right is not None:
            self._generate_codes_recursive(
                node.right,
                current_code + "1",
                codes
            )