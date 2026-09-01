from cpu import Z80
from memory import Memory


memory = Memory()
cpu = Z80(memory)

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


# Put test data into source memory

for i, value in enumerate(data):

    memory.write(
        source + i,
        value
    )


# ==================================================
# PROGRAM
# ==================================================

program = [

    # HL = 0x4000
    0x21, 0x00, 0x40,

    # DE = 0x5000
    0x11, 0x00, 0x50,

    # BC = 4
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
print("          Z80 ED BLOCK TEST")
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