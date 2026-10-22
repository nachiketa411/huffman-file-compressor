from collections import Counter
from typing import Optional

from huffman.HuffmanNode import HuffmanNode
from utils.BitReader import BitReader
from utils.BitWriter import BitWriter


def read_file(path: str):
    with (open(path, "rb") as file):
        return file.read()

def build_frequency_table(data: bytes) -> dict[int, int]:
    return dict(Counter(data))

'''
ASCII characters are divided into printable characters. 
It begins from 32 which is a Space character and ends 
with 126, which is tilde(~) character.
'''
def print_frequency_table(frequency_table: dict[int, int]) -> None:
    for byte_value, frequency in sorted(frequency_table.items()):
        printable = chr(byte_value) if 32 <= byte_value <= 126 else "."
        print(
            f"byte={byte_value:3} "
            f"char={printable!r}"
            f"frequency={frequency}"
        )

def print_codes(codes: dict[int, str]) -> None:
    for byte_value, code in sorted(codes.items()):
        printable = chr(byte_value) if 32 <= byte_value <= 126 else "."

        print(
            f"byte={byte_value:3} "
            f"char={printable!r} "
            f"code={code}"
        )

def encode_data(data: bytes, codes: dict[int, str]) -> str:
    encoded_parts: list[str] = []
    for byte_value in data:
        encoded_parts.append(codes[byte_value])

    return "".join(encoded_parts)

def decode_data(encoded_data: str, root: Optional[HuffmanNode]) -> bytes:
    if root is None:
        return b""

    if root.is_leaf():
        assert root.byte_value is not None
        return bytes(
            [root.byte_value] * len(encoded_data)
        )

    decoded_data = bytearray()
    current: HuffmanNode = root

    for bit in encoded_data:
        if bit == "0":
            next_node = current.left
        else:
            next_node = current.right

        if next_node is None:
            raise ValueError("Invalid Huffman Code")

        current = next_node

        if current.is_leaf():
            byte_value = current.byte_value
            if byte_value is None:
                raise ValueError("Leaf node has no byte value")

            decoded_data.append(byte_value)
            current = root

    return bytes(decoded_data)

def encode_packed(
        data: bytes,
        codes: dict[int, str]
) -> tuple[bytes, int]:
    writer = BitWriter()
    for byte_value in data:
        code = codes[byte_value]
        for bit in code:
            writer.write_bit(
                1 if bit == "1" else 0
            )

    return writer.finish()

def decode_packed(
        packed_data: bytes,
        root: Optional[HuffmanNode],
        padding_bits: int
) -> bytes:
    if root is None:
        return b""

    reader = BitReader(
        packed_data,
        padding_bits
    )

    if root.is_leaf():
        byte_value = root.byte_value
        if byte_value is None:
            raise ValueError("Leaf Node has no Byte Value")

        number_of_bits = (
            len(packed_data) * 8 - padding_bits
        )
        return bytes(
            [byte_value] * number_of_bits
        )

    decoded = bytearray()
    current: HuffmanNode = root
    for bit in reader.read_bits():
        if bit == 0:
            next_node = current.left
        else:
            next_node = current.right

        if next_node is None:
            raise ValueError("Invalid Huffman Encoded Data")

        current = next_node
        if current.is_leaf():
            byte_value = current.byte_value
            if byte_value is None:
                raise ValueError("Leaf Node has no byte Value")

            decoded.append(byte_value)
            current = root

    if current is not root:
        raise ValueError(
            "Encoded data ended in the middle of a Huffman Code"
        )
    return bytes(decoded)