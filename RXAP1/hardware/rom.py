class ROM:

    def __init__(self, size):

        self.size = size
        self.data = bytearray(size)


    def read(self, address):

        address &= 0xFFFF

        if address >= self.size:
            raise ValueError("ROM address out of range")

        return self.data[address]


    def write(self, address, value):

        # ROM is read-only.
        raise PermissionError(
            "Cannot write to ROM"
        )


    def load(self, program, start_address=0):

        for offset, value in enumerate(program):

            address = start_address + offset

            if address >= self.size:
                raise ValueError(
                    "Program does not fit in ROM"
                )

            self.data[address] = value & 0xFF


    def clear(self):

        self.data = bytearray(self.size)