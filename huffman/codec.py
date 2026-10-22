from collections import Counter
from typing import Optional

from huffman.bitstream import BitWriter, BitReader
from huffman.node import HuffmanNode
from huffman.tree import HuffmanTree


def build_frequency_table(data: bytes) -> dict[int, int]:
    return dict(Counter(data))


def build_tree_and_codes(
        data: bytes
) -> tuple[HuffmanTree, dict[int, str]]:
    frequencies = build_frequency_table(data)

    tree = HuffmanTree(frequencies)
    codes = tree.generate_codes()

    return tree, codes


def encode(
        data: bytes,
        codes: dict[int, str]
) -> tuple[bytes, int]:
    writer = BitWriter()

    for byte_value in data:
        _write_code(
            writer,
            codes[byte_value]
        )
    return writer.finish()


def decode(
        packed_data: bytes,
        root: Optional[HuffmanNode],
        padding_bits: int
) -> bytes:
    if root is None:
        return b""

    if root.is_leaf():
        return _decode_single_symbol(
            packed_data,
            padding_bits,
            root
        )

    reader = BitReader(
        packed_data,
        padding_bits
    )

    return _decode_tree(
        reader,
        root
    )


def _write_code(
        writer: BitWriter,
        code: str
) -> None:
    for bit_character in code:
        bit = 1 if bit_character == "1" else 0
        writer.write_bit(bit)


def _decode_single_symbol(
        packed_data: bytes,
        padding_bits: int,
        root: HuffmanNode
) -> bytes:
    byte_value = root.byte_value
    if byte_value is None:
        raise ValueError(
            "Leaf node has no byte value"
        )

    symbol_count = (
        len(packed_data) * 8 - padding_bits
    )
    return bytes(
        [byte_value] * symbol_count
    )


def _decode_tree(
        reader: BitReader,
        root: HuffmanNode
) -> bytes:
    decoded_data = bytearray()
    current: HuffmanNode = root

    for bit in reader.read_bits():
        current = _move_to_next_node(
            current,
            bit,
        )

        if current.is_leaf():
            _append_leaf_value(
                decoded_data,
                current
            )
            current = root

    _validate_decode_finished(
        current,
        root
    )
    return bytes(decoded_data)


def _move_to_next_node(
        current: HuffmanNode,
        bit: int
) -> HuffmanNode:
    next_node = (
        current.left
        if bit == 0
        else current.right
    )

    if next_node is None:
        raise ValueError(
            "Invalid Huffman encoded data"
        )

    return next_node


def _append_leaf_value(
        decoded: bytearray,
        node: HuffmanNode
) -> None:
    byte_value = node.byte_value

    if byte_value is None:
        raise ValueError(
            "Leaf node has no byte value"
        )

    decoded.append(byte_value)


def _validate_decode_finished(
        current: HuffmanNode,
        root: HuffmanNode
) -> None:
    if current is not root:
        raise ValueError(
            "Encoded data ended in the middle "
            "of a Huffman code"
        )