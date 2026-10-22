class BitWriter:
    def __init__(self):
        self.buffer = bytearray()
        self.current_byte = 0
        self.num_bits_filled = 0

    def _add_byte(self):
        self.buffer.append(self.current_byte)
        self.current_byte = 0
        self.num_bits_filled = 0

    def write_bit(self, bit: int) -> None:
        if bit not in (0, 1):
            raise ValueError("Bit must be 0 or 1")

        self.current_byte = (
            (self.current_byte << 1) | bit
        )
        self.num_bits_filled += 1

        if self.num_bits_filled == 8:
            self._add_byte()

    def finish(self) -> tuple[bytes, int]:
        padding_bits = 0
        if self.num_bits_filled > 0:
            padding_bits = 8 - self.num_bits_filled
            self.current_byte <<= padding_bits

            self._add_byte()
        return bytes(self.buffer), padding_bits