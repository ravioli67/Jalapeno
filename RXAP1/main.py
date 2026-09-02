from machine import Computer
from hardware.bootrom import BOOT_ROM


computer = Computer()


# ==========================================
# POWER ON
# ==========================================

computer.power_on()


# ==========================================
# LOAD BOOT ROM
# ==========================================

computer.load_rom(
    BOOT_ROM
)


# ==========================================
# RAM PROGRAM
# ==========================================

ram_program = [

    # LD A,42
    0x3E, 0x42,

    # HALT
    0x76
]


# ==========================================
# LOAD RAM PROGRAM
# ==========================================

computer.load_program(
    ram_program,
    0x1000
)


# ==========================================
# RUN COMPUTER
# ==========================================

computer.run()


# ==========================================
# RESULTS
# ==========================================

print("=" * 50)
print("          RXAP1 BOOT TEST")
print("=" * 50)
print()

print("CPU HALTED")
print()

print(
    "PC =",
    hex(computer.cpu.reg.pc)
)

print(
    "SP =",
    hex(computer.cpu.reg.sp)
)

print(
    "A  =",
    hex(computer.cpu.reg.a)
)

print(
    "ROM ENABLED =",
    computer.memory.rom_enabled
)

print()

print("=" * 50)