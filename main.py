from pathlib import Path

from huffman.codec import (
    build_tree_and_codes,
    decode,
    encode,
)


def main() -> None:
    input_path = Path("./assets/My Washington Driving License  (1).pdf")
    data = input_path.read_bytes()

    tree, codes = build_tree_and_codes(data)

    packed_data, padding_bits = encode(
        data,
        codes,
    )
    decoded_data = decode(
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