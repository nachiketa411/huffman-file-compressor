class BitWriter:
    def __init__(self):
        self._buffer = bytearray()
        self._current_byte = 0
        self._num_bits_filled = 0

    def _flush_current_byte(self):
        self._buffer.append(self._current_byte)
        self._current_byte = 0
        self._num_bits_filled = 0

    def write_bit(self, bit: int) -> None:
        if bit not in (0, 1):
            raise ValueError("Bit must be 0 or 1")

        self._current_byte = (
            (self._current_byte << 1) | bit
        )
        self._num_bits_filled += 1

        if self._num_bits_filled == 8:
            self._flush_current_byte()

    def finish(self) -> tuple[bytes, int]:
        padding_bits = 0
        if self._num_bits_filled > 0:
            padding_bits = 8 - self._num_bits_filled
            self._current_byte <<= padding_bits

            self._flush_current_byte()
        return bytes(self._buffer), padding_bits


class BitReader:
    def __init__(self, data: bytes, padding_bits: int = 0):
        if not 0 <= padding_bits <= 7:
            raise ValueError(
                "Padding bits must be between 0 and 7"
            )
        self._data = data
        self._padding_bits = padding_bits

    def read_bits(self):
        total_bits = len(self._data) * 8 - self._padding_bits
        bits_read = 0

        for byte_value in self._data:
            for bit_position in range(7, -1, -1):
                if bits_read >= total_bits:
                    return
                bit = (byte_value >> bit_position) & 1
                yield bit
                bits_read += 1