# Sharie Rhea
# 09.05.26
# SNHU CS680


class BitReader:
    """Utility class to read individual bits directly from a bytearray."""

    def __init__(self, data: bytearray | bytes, start_byte: int = 0, padding_amount: int = 0):
        self.data = data
        self.byte_index = start_byte
        # start at MSB
        self.bit_offset = 7
        self.total_bits = (len(data) - start_byte) * 8 - padding_amount
        self.bits_read = 0

    def next_bit(self) -> int:
        """Returns the next bit as 0 or 1."""
        if self.bits_read >= self.total_bits:
            raise StopIteration

        # extract the bit with bitwise shift and mask
        current_byte = self.data[self.byte_index]
        bit = (current_byte >> self.bit_offset) & 1

        # move forward, adjusting to next byte if needed
        self.bit_offset -= 1
        if self.bit_offset < 0:
            self.bit_offset = 7
            self.byte_index += 1

        self.bits_read += 1
        return bit

    def read_byte_as_int(self) -> int:
        """Helper method to return the next 8 bits as an integer."""
        byte_val = 0
        for _ in range(8):
            byte_val = (byte_val << 1) | self.next_bit()
        return byte_val


class BitWriter:
    """Helper class to accumulate individual bits and write them directly to a bytearray."""

    def __init__(self):
        self.buffer = bytearray()
        self.current_byte = 0
        self.bit_count = 0
        self.total_bits = 0

    def write_bit(self, bit: int) -> None:
        """Write a single bit (0 or 1)."""
        # shift buffer and append
        self.current_byte = (self.current_byte << 1) | (bit & 1)
        self.bit_count += 1
        self.total_bits += 1

        # flush each byte as it's filled
        if self.bit_count == 8:
            self.buffer.append(self.current_byte)
            self.current_byte = 0
            self.bit_count = 0

    def write_bits(self, bit_string: str) -> None:
        """Convenience method to write a sequence of bits."""
        for char in bit_string:
            self.write_bit(1 if char == "1" else 0)

    def write_byte_code(self, code: int) -> None:
        """Helper method to write an 8-bit integer, MSB to LSB."""
        for i in range(7, -1, -1):
            self.write_bit((code >> i) & 1)

    def write_code(self, val: int, length: int) -> None:
        """Helper method to integer bit pattern with a specific length."""
        for i in range(length - 1, -1, -1):
            # extract position i and mask
            bit = (val >> i) & 1

            # update the current byte and incrememt counters
            self.current_byte = (self.current_byte << 1) | bit
            self.bit_count += 1
            self.total_bits += 1

            # flush to buffer if this byte is full
            if self.bit_count == 8:
                self.buffer.append(self.current_byte)
                self.current_byte = 0
                self.bit_count = 0

    def flush(self) -> int:
        """Pad remaining bits in the current byte if necessary, append to the buffer. Returns number of padding bits."""
        if self.bit_count == 0:
            return 0

        padding_amount = 8 - self.bit_count
        self.current_byte <<= padding_amount
        self.buffer.append(self.current_byte)

        # reset state
        self.current_byte = 0
        self.bit_count = 0

        return padding_amount
