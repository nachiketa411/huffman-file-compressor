class BitReader:
    def __init__(self, data: bytes, padding_bits: int = 0):
        self.data = data
        self.padding_bits = padding_bits

    def read_bits(self):
        total_bits = len(self.data) * 8 - self.padding_bits
        bits_read = 0

        for byte_value in self.data:
            for bit_position in range(7, -1, -1):
                if bits_read >= total_bits:
                    return
                bit = (byte_value >> bit_position) & 1
                yield bit
                bits_read += 1