from typing import Optional


class HuffmanNode:
    def __init__(
            self,
            frequency: int = 0,
            byte_value: Optional[int] = None,
            left: Optional["HuffmanNode"] = None,
            right: Optional["HuffmanNode"] = None
    ):
        self.byte_value = byte_value
        self.frequency = frequency
        self.left = left
        self.right = right

    @classmethod
    def leaf(
            cls,
            byte_value: int,
            frequency: int
    ) -> "HuffmanNode":
        return cls(
            frequency=frequency,
            byte_value=byte_value
        )

    @classmethod
    def parent(
            cls,
            left: "HuffmanNode",
            right: "HuffmanNode"
    ) -> "HuffmanNode":
        return cls(
            frequency=left.frequency + right.frequency,
            left=left,
            right=right
        )

    def is_leaf(self) -> bool:
        return self.byte_value is not None

    # checks if the current node is LESS THAN the other
    def __lt__(self, other: "HuffmanNode") -> bool:
        return self.frequency < other.frequency