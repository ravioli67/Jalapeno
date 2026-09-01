from cpu import Z80
from hardware.memory import Memory
from hardware.io import IO


class Computer:

    def __init__(self):

        # ==============================
        # HARDWARE
        # ==============================

        self.memory = Memory(65536)

        self.io = IO()

        # ==============================
        # CPU
        # ==============================

        self.cpu = Z80(
            self.memory,
            self.io
        )

        # ==============================
        # POWER STATE
        # ==============================

        self.powered_on = False


    # ==================================
    # POWER ON
    # ==================================

    def power_on(self):

        self.memory.clear()

        self.io.clear()

        self.cpu.reset()

        self.powered_on = True


    # ==================================
    # LOAD PROGRAM
    # ==================================

    def load_program(
        self,
        program,
        address=0x0000
    ):

        self.memory.load(
            program,
            address
        )


    # ==================================
    # RUN
    # ==================================

    def run(self):

        if not self.powered_on:

            raise RuntimeError(
                "Computer is powered off"
            )

        self.cpu.run()