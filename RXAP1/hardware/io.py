class IO:

    def __init__(self):
        self.ports = {}

    def read(self, port):

        port &= 0xFFFF

        return self.ports.get(
            port,
            0xFF
        )

    def write(self, port, value):

        port &= 0xFFFF
        value &= 0xFF

        self.ports[port] = value

    def clear(self):

        self.ports.clear()