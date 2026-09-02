from .memory import Memory
from .rom import ROM


class MemoryMap:

    def __init__(self):

        # ==================================
        # MEMORY SIZES
        # ==================================

        self.rom_size = 0x1000      # 4 KB
        self.ram_size = 0x10000     # 64 KB

        # ==================================
        # HARDWARE
        # ==================================

        self.rom = ROM(self.rom_size)

        self.ram = Memory(self.ram_size)

        # ROM is visible after reset
        self.rom_enabled = True


    # ==================================
    # READ
    # ==================================

    def read(self, address):

        address &= 0xFFFF

        if self.rom_enabled and address < self.rom_size:

            return self.rom.read(address)

        return self.ram.read(address)


    # ==================================
    # WRITE
    # ==================================

    def write(self, address, value):

        address &= 0xFFFF

        if self.rom_enabled and address < self.rom_size:

            raise PermissionError(
                "Cannot write to ROM"
            )

        self.ram.write(
            address,
            value
        )


    # ==================================
    # LOAD RAM
    # ==================================

    def load(self, program, start_address=0):

        for offset, value in enumerate(program):

            self.write(
                start_address + offset,
                value
            )


    # ==================================
    # LOAD ROM
    # ==================================

    def load_rom(self, program, start_address=0):

        self.rom.load(
            program,
            start_address
        )


    # ==================================
    # DISABLE ROM
    # ==================================

    def disable_rom(self):

        self.rom_enabled = False


    # ==================================
    # ENABLE ROM
    # ==================================

    def enable_rom(self):

        self.rom_enabled = True


    # ==================================
    # CLEAR
    # ==================================

    def clear(self):

        self.ram.clear()
        self.rom.clear()

        self.rom_enabled = True