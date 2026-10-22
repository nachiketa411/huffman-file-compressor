from huffman.HuffmanTree import HuffmanTree
from utils.utils import (
    build_frequency_table,
    read_file,
    encode_packed,
    decode_packed
)


def main() -> None:
    # 1. Read original file
    data = read_file("./assets/My Washington Driving License  (1).pdf")

    # 2. Build Frequency Table
    frequencies = build_frequency_table(data)

    # 3. Build Huffman Tree
    tree = HuffmanTree(frequencies)

    # 4. Generate Huffman Code
    codes = tree.build_code()

    # assert tree.root is not None
    # assert tree.root.frequency == len(data)

    # 5. Pack huffman bits into actual bytes
    packed_data, padding_bits = encode_packed(
        data,
        codes,
    )

    # 6. Decode directly from packed bytes
    decoded_data = decode_packed(
        packed_data,
        tree.root,
        padding_bits,
    )

    print("=== Packed Huffman Test ===")
    print("Original size:", len(data), "bytes")
    print("Packed size:", len(packed_data), "bytes")
    print("Padding bits:", padding_bits)
    print("Decoded size:", len(decoded_data), "bytes")
    print("Decoded correctly:", decoded_data == data)

    if data:
        compression_ratio = len(packed_data) / len(data)

        print(
            f"Payload compression ratio: "
            f"{compression_ratio:.2%}"
        )

if __name__ == "__main__":
    main()