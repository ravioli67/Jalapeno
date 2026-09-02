from cpu import Z80
from hardware.memory_map import MemoryMap
from hardware.io import IO


class Computer:

    def __init__(self):

        # ==============================
        # HARDWARE
        # ==============================

        self.memory = MemoryMap()

        self.io = IO(self)

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
    # LOAD RAM PROGRAM
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
    # LOAD ROM
    # ==================================

    def load_rom(
        self,
        program,
        address=0x0000
    ):

        self.memory.load_rom(
            program,
            address
        )


    # ==================================
    # ROM CONTROL
    # ==================================

    def disable_rom(self):

        self.memory.disable_rom()


    def enable_rom(self):

        self.memory.enable_rom()


    # ==================================
    # RUN
    # ==================================

    def run(self):

        if not self.powered_on:

            raise RuntimeError(
                "Computer is powered off"
            )

        self.cpu.run()