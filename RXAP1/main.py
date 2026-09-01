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

    # ==========================================
    # SBC HL,BC
    # ==========================================

    # LD HL,2000
    0x21, 0x00, 0x20,

    # LD BC,0100
    0x01, 0x00, 0x01,

    # Clear Carry
    # XOR A
    0xAF,

    # SBC HL,BC
    0xED, 0x42,


    # ==========================================
    # SBC HL,DE
    # ==========================================

    # LD DE,0020
    0x11, 0x20, 0x00,

    # SBC HL,DE
    0xED, 0x52,


    # ==========================================
    # SBC HL,HL
    # ==========================================

    0xED, 0x62,


    # ==========================================
    # HALT
    # ==========================================

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

print("HL =", hex(cpu.get_hl()))
print("BC =", hex(cpu.get_bc()))
print("DE =", hex(cpu.get_de()))
print("SP =", hex(cpu.sp))
print("F  =", hex(cpu.f))

print("B  =", hex(cpu.b))
print("C  =", hex(cpu.c))
print("D  =", hex(cpu.d))
print("E  =", hex(cpu.e))
print("A  =", hex(cpu.a))
print("Memory[4000] =", hex(memory.read(0x4000)))

print("DE =", hex(cpu.get_de()))
print("HL =", hex(cpu.get_hl()))
print("BC =", hex(cpu.get_bc()))

print("A  =", hex(cpu.a))

print()
print("Alternate registers:")

print("BC' =", hex(
    (cpu.reg.b_alt << 8) | cpu.reg.c_alt
))

print("DE' =", hex(
    (cpu.reg.d_alt << 8) | cpu.reg.e_alt
))

print("HL' =", hex(
    (cpu.reg.h_alt << 8) | cpu.reg.l_alt
))

print("A'  =", hex(cpu.reg.a_alt))

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