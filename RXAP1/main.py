from machine import Computer


computer = Computer()


# ==========================================
# POWER ON
# ==========================================

computer.power_on()


# ==========================================
# TEST PROGRAM
# ==========================================

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


# ==========================================
# TEST DATA
# ==========================================

source = 0x4000
destination = 0x5000

data = [
    0x10,
    0x20,
    0x30,
    0x40
]


for i, value in enumerate(data):

    computer.memory.write(
        source + i,
        value
    )


# ==========================================
# LOAD PROGRAM
# ==========================================

computer.load_program(
    program,
    0x0000
)


# ==========================================
# RUN
# ==========================================

computer.run()


# ==========================================
# RESULTS
# ==========================================

print("=" * 50)
print("          RXAP1 COMPUTER TEST")
print("=" * 50)
print()

print("CPU HALTED")
print()

print(
    "HL =",
    hex(computer.cpu.get_hl())
)

print(
    "DE =",
    hex(computer.cpu.get_de())
)

print(
    "BC =",
    hex(computer.cpu.get_bc())
)

print(
    "F  =",
    hex(computer.cpu.reg.f)
)

print(
    "PC =",
    hex(computer.cpu.reg.pc)
)

print()

print("Destination:")

print([
    hex(
        computer.memory.read(
            destination + i
        )
    )
    for i in range(4)
])

print()

print("=" * 50)