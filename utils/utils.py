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
            f"char={printable!r} "
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