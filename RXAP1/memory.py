class Memory:

    def __init__(self, size=65536):

        self.size = size

        self.data = bytearray(size)

    def read(self, address):

        address &= 0xFFFF

        return self.data[address]

    def write(self, address, value):

        address &= 0xFFFF

        self.data[address] = value & 0xFF

    def load(self, program, start_address=0):

        for offset, value in enumerate(program):

            self.write(
                start_address + offset,
                value
            )

    def clear(self):

        self.data = bytearray(
            self.size
        )