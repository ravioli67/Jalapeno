from .registers import Registers

from .flags import (
    S_FLAG,
    Z_FLAG,
    Y_FLAG,
    H_FLAG,
    X_FLAG,
    PV_FLAG,
    N_FLAG,
    C_FLAG,
)

from hardware.io import IO


class Z80:

    def __init__(self, memory, io=None):

        self.memory = memory

        self.io = (
            io
            if io is not None
            else IO()
        )

        self.reg = Registers()

        self.halted = False


    # ==========================================
    # REGISTER COMPATIBILITY
    # ==========================================

    @property
    def a(self):
        return self.reg.a

    @a.setter
    def a(self, value):
        self.reg.a = value & 0xFF


    @property
    def f(self):
        return self.reg.f

    @f.setter
    def f(self, value):
        self.reg.f = value & 0xFF


    @property
    def b(self):
        return self.reg.b

    @b.setter
    def b(self, value):
        self.reg.b = value & 0xFF


    @property
    def c(self):
        return self.reg.c

    @c.setter
    def c(self, value):
        self.reg.c = value & 0xFF


    @property
    def d(self):
        return self.reg.d

    @d.setter
    def d(self, value):
        self.reg.d = value & 0xFF


    @property
    def e(self):
        return self.reg.e

    @e.setter
    def e(self, value):
        self.reg.e = value & 0xFF


    @property
    def h(self):
        return self.reg.h

    @h.setter
    def h(self, value):
        self.reg.h = value & 0xFF


    @property
    def l(self):
        return self.reg.l

    @l.setter
    def l(self, value):
        self.reg.l = value & 0xFF


    @property
    def ix(self):
        return self.reg.ix

    @ix.setter
    def ix(self, value):
        self.reg.ix = value & 0xFFFF


    @property
    def iy(self):
        return self.reg.iy

    @iy.setter
    def iy(self, value):
        self.reg.iy = value & 0xFFFF


    @property
    def sp(self):
        return self.reg.sp

    @sp.setter
    def sp(self, value):
        self.reg.sp = value & 0xFFFF


    @property
    def pc(self):
        return self.reg.pc

    @pc.setter
    def pc(self, value):
        self.reg.pc = value & 0xFFFF


    @property
    def i(self):
        return self.reg.i

    @i.setter
    def i(self, value):
        self.reg.i = value & 0xFF


    @property
    def r(self):
        return self.reg.r

    @r.setter
    def r(self, value):
        self.reg.r = value & 0xFF


    @property
    def im(self):
        return self.reg.im

    @im.setter
    def im(self, value):
        self.reg.im = value


    # ==========================================
    # MEMORY
    # ==========================================

    def read_byte(self, address):

        return self.memory.read(address)


    def write_byte(self, address, value):

        self.memory.write(
            address,
            value
        )


    def fetch_byte(self):

        value = self.read_byte(self.pc)

        self.pc = (
            self.pc + 1
        ) & 0xFFFF

        return value


    def fetch_word(self):

        low = self.fetch_byte()
        high = self.fetch_byte()

        return (
            low
            | (high << 8)
        )


    # ==========================================
    # REGISTER PAIRS
    # ==========================================

    def get_bc(self):
        return self.reg.get_bc()


    def set_bc(self, value):
        self.reg.set_bc(value)


    def get_de(self):
        return self.reg.get_de()


    def set_de(self, value):
        self.reg.set_de(value)


    def get_hl(self):
        return self.reg.get_hl()


    def set_hl(self, value):
        self.reg.set_hl(value)


    # ==========================================
    # RESET
    # ==========================================

    def reset(self):

        self.reg.reset()

        self.halted = False


    # ==========================================
    # PLACEHOLDER EXECUTION
    # ==========================================

    def step(self):

        if self.halted:
            return

        opcode = self.fetch_byte()

        if opcode == 0x00:

            # NOP
            return


        if opcode == 0x76:

            # HALT
            self.halted = True
            return


        raise NotImplementedError(
            f"Opcode {opcode:02X} "
            f"not connected yet at "
            f"{(self.pc - 1) & 0xFFFF:04X}"
        )


    def run(self, max_cycles=1000000):

        cycles = 0

        while (
            not self.halted
            and cycles < max_cycles
        ):

            self.step()

            cycles += 1

        if cycles >= max_cycles:

            raise RuntimeError(
                "CPU exceeded maximum "
                "execution steps"
            )