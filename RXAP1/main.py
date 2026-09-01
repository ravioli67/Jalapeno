from cpu import Z80
from memory import Memory


memory = Memory()
cpu = Z80(memory)

cpu.reset()


# ==================================================
# DD CB TEST
# ==================================================

program = [

    # IX = 0x4000
    0xDD, 0x21, 0x00, 0x40,

    # (IX+2) = 0x81
    0xDD, 0x36, 0x02, 0x81,

    # RLC (IX+2)
    # 0x81 -> 0x03
    0xDD, 0xCB, 0x02, 0x06,

    # SET bit 7,(IX+2)
    # 0x03 -> 0x83
    0xDD, 0xCB, 0x02, 0xFE,

    # RES bit 0,(IX+2)
    # 0x83 -> 0x82
    0xDD, 0xCB, 0x02, 0x86,

    # BIT bit 7,(IX+2)
    0xDD, 0xCB, 0x02, 0x7E,

    # ==================================================
    # FD CB TEST
    # ==================================================

    # IY = 0x5000
    0xFD, 0x21, 0x00, 0x50,

    # (IY-1) = 0x01
    0xFD, 0x36, 0xFF, 0x01,

    # SET bit 3,(IY-1)
    # 0x01 -> 0x09
    0xFD, 0xCB, 0xFF, 0xDE,

    # RES bit 0,(IY-1)
    # 0x09 -> 0x08
    0xFD, 0xCB, 0xFF, 0x86,

    # HALT
    0x76
]


memory.load(
    program,
    0x0000
)


print("=" * 50)
print("          Z80 INDEXED CB TEST")
print("=" * 50)
print()


cpu.run()


print()
print("CPU HALTED")
print()

print("IX =", hex(cpu.ix))
print("IY =", hex(cpu.iy))

print()
print("Memory[4002] =", hex(
    memory.read(0x4002)
))

print("Memory[4FFF] =", hex(
    memory.read(0x4FFF)
))

print()
print("F =", hex(cpu.f))
print("PC =", hex(cpu.pc))

print()
print("=" * 50)