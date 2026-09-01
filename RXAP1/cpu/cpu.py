from .registers import Registers

from .cb import execute_cb
from .ed import execute_ed
from .indexed import execute_indexed
from .opcodes import execute_opcode

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


    # ==================================================
    # REGISTER PROPERTIES
    # ==================================================

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


    # ==================================================
    # MEMORY
    # ==================================================

    def read_byte(self, address):

        return self.memory.read(
            address
        )


    def write_byte(self, address, value):

        self.memory.write(
            address,
            value
        )


    def fetch_byte(self):

        value = self.read_byte(
            self.pc
        )

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


    # ==================================================
    # REGISTER PAIRS
    # ==================================================

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


    # ==================================================
    # 8-BIT REGISTER ACCESS
    # ==================================================

    def read_r(self, index):

        index &= 7

        if index == 0:
            return self.b

        if index == 1:
            return self.c

        if index == 2:
            return self.d

        if index == 3:
            return self.e

        if index == 4:
            return self.h

        if index == 5:
            return self.l

        if index == 6:

            return self.read_byte(
                self.get_hl()
            )

        if index == 7:
            return self.a


    def write_r(self, index, value):

        index &= 7
        value &= 0xFF

        if index == 0:
            self.b = value

        elif index == 1:
            self.c = value

        elif index == 2:
            self.d = value

        elif index == 3:
            self.e = value

        elif index == 4:
            self.h = value

        elif index == 5:
            self.l = value

        elif index == 6:

            self.write_byte(
                self.get_hl(),
                value
            )

        elif index == 7:
            self.a = value


    # ==================================================
    # I/O
    # ==================================================

    def io_read(self, port):

        return self.io.read(
            port
        )


    def io_write(self, port, value):

        self.io.write(
            port,
            value
        )


    # ==================================================
    # STACK
    # ==================================================

    def push_word(self, value):

        value &= 0xFFFF

        self.sp = (
            self.sp - 1
        ) & 0xFFFF

        self.write_byte(
            self.sp,
            (value >> 8) & 0xFF
        )

        self.sp = (
            self.sp - 1
        ) & 0xFFFF

        self.write_byte(
            self.sp,
            value & 0xFF
        )


    def pop_word(self):

        low = self.read_byte(
            self.sp
        )

        self.sp = (
            self.sp + 1
        ) & 0xFFFF

        high = self.read_byte(
            self.sp
        )

        self.sp = (
            self.sp + 1
        ) & 0xFFFF

        return (
            low
            | (high << 8)
        )


    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.reg.reset()

        self.halted = False


    # ==================================================
    # INSTRUCTION EXECUTION
    # ==================================================

    def step(self):

        if self.halted:
            return

        opcode = self.fetch_byte()


        # ==================================================
        # DD PREFIX — IX
        # ==================================================

        if opcode == 0xDD:

            execute_indexed(
                self,
                0xDD
            )

            return


        # ==================================================
        # FD PREFIX — IY
        # ==================================================

        if opcode == 0xFD:

            execute_indexed(
                self,
                0xFD
            )

            return


        # ==================================================
        # CB PREFIX
        # ==================================================

        if opcode == 0xCB:

            cb_opcode = self.fetch_byte()

            execute_cb(
                self,
                cb_opcode
            )

            return


        # ==================================================
        # ED PREFIX
        # ==================================================

        if opcode == 0xED:

            ed_opcode = self.fetch_byte()

            execute_ed(
                self,
                ed_opcode
            )

            return


        # ==================================================
        # NORMAL OPCODES
        # ==================================================

        execute_opcode(
            self,
            opcode
        )


    # ==================================================
    # RUN
    # ==================================================

    def run(self, max_steps=1_000_000):

        steps = 0

        while (
            not self.halted
            and steps < max_steps
        ):

            self.step()

            steps += 1

        if steps >= max_steps:

            raise RuntimeError(
                "CPU exceeded maximum "
                "execution steps"
            )