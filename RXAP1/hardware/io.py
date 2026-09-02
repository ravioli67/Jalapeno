class IO:

    ROM_CONTROL_PORT = 0x00

    def __init__(self, computer=None):
        self.ports = {}
        self.computer = computer

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

        # ==================================
        # ROM CONTROL
        # ==================================

        if port == self.ROM_CONTROL_PORT:

            if value == 0x00:

                if self.computer is not None:
                    self.computer.disable_rom()

    def clear(self):

        self.ports.clear()