from cpu import Z80
from hardware.memory import Memory
from hardware.io import IO


memory = Memory()
io = IO()

cpu = Z80(
    memory,
    io
)

cpu.reset()


# ==================================================
# TEST DATA
# ==================================================

source = 0x4000
destination = 0x5000

data = [
    0x10,
    0x20,
    0x30,
    0x40
]


for i, value in enumerate(data):

    memory.write(
        source + i,
        value
    )


# ==================================================
# PROGRAM
# ==================================================

program = [

    # LD HL,4000
    0x21, 0x00, 0x40,

    # LD DE,5000
    0x11, 0x00, 0x50,

    # LD BC,4
    0x01, 0x04, 0x00,

    # LDIR
    0xED, 0xB0,

    # HALT
    0x76
]


memory.load(
    program,
    0x0000
)


# ==================================================
# RUN
# ==================================================

print("=" * 50)
print("          RXAP1 Z80 TEST")
print("=" * 50)
print()

print("Source:")

print([
    hex(
        memory.read(
            source + i
        )
    )
    for i in range(4)
])

print()


cpu.run()


print("CPU HALTED")
print()

print(
    "HL =",
    hex(cpu.get_hl())
)

print(
    "DE =",
    hex(cpu.get_de())
)

print(
    "BC =",
    hex(cpu.get_bc())
)

print()

print("Destination:")

print([
    hex(
        memory.read(
            destination + i
        )
    )
    for i in range(4)
])

print()

print(
    "F  =",
    hex(cpu.f)
)

print(
    "PC =",
    hex(cpu.pc)
)

print()
print("=" * 50)