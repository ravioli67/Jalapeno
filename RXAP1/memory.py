class Memory:
    def __init__(self, size=65536):
        self.size = size
        self.data = bytearray(size)

    def read(self, address):
        return self.data[address & 0xFFFF]

    def write(self, address, value):
        self.data[address & 0xFFFF] = value & 0xFF

    def load(self, data, start=0):
        for i, value in enumerate(data):
            self.write(start + i, value)

    def clear(self):
        self.data = bytearray(self.size)