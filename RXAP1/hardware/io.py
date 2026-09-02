class IO:

    ROM_CONTROL_PORT = 0x00

    CONSOLE_OUTPUT_PORT = 0x01
    CONSOLE_INPUT_PORT = 0x02


    def __init__(self, computer=None):

        self.ports = {}

        self.computer = computer


    # ==================================
    # READ
    # ==================================

    def read(self, port):

        port &= 0xFFFF


        # ==================================
        # CONSOLE INPUT
        # ==================================

        if port == self.CONSOLE_INPUT_PORT:

            if self.computer is not None:

                return self.computer.console.read_char()

            return 0x00


        return self.ports.get(
            port,
            0xFF
        )


    # ==================================
    # WRITE
    # ==================================

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


        # ==================================
        # CONSOLE OUTPUT
        # ==================================

        elif port == self.CONSOLE_OUTPUT_PORT:

            if self.computer is not None:

                self.computer.console.write_char(
                    value
                )


    # ==================================
    # CLEAR
    # ==================================

    def clear(self):

        self.ports.clear()