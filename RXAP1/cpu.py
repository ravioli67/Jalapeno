class Z80:

    # ==================================================
    # FLAGS
    # ==================================================

    FLAG_S = 0x80
    FLAG_Z = 0x40
    FLAG_H = 0x10
    FLAG_PV = 0x04
    FLAG_N = 0x02
    FLAG_C = 0x01

    # ==================================================
    # INIT
    # ==================================================

    def __init__(self, memory):

        self.memory = memory

        # 8-bit registers
        self.a = 0
        self.f = 0

        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.h = 0
        self.l = 0

        # Alternate registers
        self.a_alt = 0
        self.f_alt = 0

        self.b_alt = 0
        self.c_alt = 0
        self.d_alt = 0
        self.e_alt = 0
        self.f_alt = 0
        self.h_alt = 0
        self.l_alt = 0

        # Index registers
        self.ix = 0
        self.iy = 0

        # Special registers
        self.sp = 0xFFFF
        self.pc = 0

        self.i = 0
        self.r = 0

        # Interrupt state
        self.iff1 = False
        self.iff2 = False
        self.im = 0

        # CPU state
        self.halted = False
        self.running = True

        # I/O
        self.ports = {}

        # Opcode table
        self.opcodes = [
            self.op_unimplemented
            for _ in range(256)
        ]

        self.build_opcode_table()

    # ==================================================
    # MEMORY
    # ==================================================

    def read_byte(self, address):

        return self.memory.read(
            address & 0xFFFF
        )

    def write_byte(self, address, value):

        self.memory.write(
            address & 0xFFFF,
            value & 0xFF
        )

    def fetch_byte(self):

        value = self.read_byte(
            self.pc
        )

        self.pc = (
            self.pc + 1
        ) & 0xFFFF

        self.r = (
            self.r + 1
        ) & 0x7F

        return value

    def fetch_word(self):

        low = self.fetch_byte()
        high = self.fetch_byte()

        return low | (high << 8)

    # ==================================================
    # I/O PORTS
    # ==================================================

    def io_read(self, port):

        port &= 0xFFFF

        if port in self.ports:
            return self.ports[port] & 0xFF

        return 0xFF

    def io_write(self, port, value):

        port &= 0xFFFF
        value &= 0xFF

        self.ports[port] = value

    # ==================================================
    # REGISTER PAIRS
    # ==================================================

    def get_bc(self):

        return (
            (self.b << 8) |
            self.c
        )

    def set_bc(self, value):

        value &= 0xFFFF

        self.b = (
            value >> 8
        ) & 0xFF

        self.c = value & 0xFF

    def get_de(self):

        return (
            (self.d << 8) |
            self.e
        )

    def set_de(self, value):

        value &= 0xFFFF

        self.d = (
            value >> 8
        ) & 0xFF

        self.e = value & 0xFF

    def get_hl(self):

        return (
            (self.h << 8) |
            self.l
        )

    def set_hl(self, value):

        value &= 0xFFFF

        self.h = (
            value >> 8
        ) & 0xFF

        self.l = value & 0xFF

    # ==================================================
    # FLAGS
    # ==================================================

    def set_flag(self, flag, value):

        if value:
            self.f |= flag
        else:
            self.f &= ~flag

    def get_flag(self, flag):

        return bool(
            self.f & flag
        )

    def parity(self, value):

        return (
            bin(value & 0xFF).count("1") % 2
        ) == 0

    # ==================================================
    # 8-BIT ADD
    # ==================================================

    def add8(self, a, b, carry=0):

        result = a + b + carry

        value = result & 0xFF

        self.set_flag(
            self.FLAG_S,
            bool(value & 0x80)
        )

        self.set_flag(
            self.FLAG_Z,
            value == 0
        )

        self.set_flag(
            self.FLAG_H,
            (
                (a & 0x0F) +
                (b & 0x0F) +
                carry
            ) > 0x0F
        )

        self.set_flag(
            self.FLAG_PV,
            bool(
                (~(a ^ b) &
                 (a ^ value) &
                 0x80)
            )
        )

        self.set_flag(
            self.FLAG_N,
            False
        )

        self.set_flag(
            self.FLAG_C,
            result > 0xFF
        )

        return value

    # ==================================================
    # 8-BIT SUB
    # ==================================================

    def sub8(self, a, b, carry=0):

        result = a - b - carry

        value = result & 0xFF

        self.set_flag(
            self.FLAG_S,
            bool(value & 0x80)
        )

        self.set_flag(
            self.FLAG_Z,
            value == 0
        )

        self.set_flag(
            self.FLAG_H,
            (
                (a & 0x0F) -
                (b & 0x0F) -
                carry
            ) < 0
        )

        self.set_flag(
            self.FLAG_PV,
            bool(
                ((a ^ b) &
                 (a ^ value) &
                 0x80)
            )
        )

        self.set_flag(
            self.FLAG_N,
            True
        )

        self.set_flag(
            self.FLAG_C,
            result < 0
        )

        return value

    # ==================================================
    # INC
    # ==================================================

    def inc8(self, value):

        carry = self.get_flag(
            self.FLAG_C
        )

        result = (
            value + 1
        ) & 0xFF

        self.set_flag(
            self.FLAG_S,
            bool(result & 0x80)
        )

        self.set_flag(
            self.FLAG_Z,
            result == 0
        )

        self.set_flag(
            self.FLAG_H,
            (value & 0x0F) == 0x0F
        )

        self.set_flag(
            self.FLAG_PV,
            value == 0x7F
        )

        self.set_flag(
            self.FLAG_N,
            False
        )

        self.set_flag(
            self.FLAG_C,
            carry
        )

        return result

    # ==================================================
    # DEC
    # ==================================================

    def dec8(self, value):

        carry = self.get_flag(
            self.FLAG_C
        )

        result = (
            value - 1
        ) & 0xFF

        self.set_flag(
            self.FLAG_S,
            bool(result & 0x80)
        )

        self.set_flag(
            self.FLAG_Z,
            result == 0
        )

        self.set_flag(
            self.FLAG_H,
            (value & 0x0F) == 0
        )

        self.set_flag(
            self.FLAG_PV,
            value == 0x80
        )

        self.set_flag(
            self.FLAG_N,
            True
        )

        self.set_flag(
            self.FLAG_C,
            carry
        )

        return result

    # ==================================================
    # LOGICAL
    # ==================================================

    def and8(self, value):

        self.a &= value
        self.a &= 0xFF

        self.f = self.FLAG_H

        self.set_flag(
            self.FLAG_S,
            bool(self.a & 0x80)
        )

        self.set_flag(
            self.FLAG_Z,
            self.a == 0
        )

        self.set_flag(
            self.FLAG_PV,
            self.parity(self.a)
        )

    def or8(self, value):

        self.a |= value
        self.a &= 0xFF

        self.f = 0

        self.set_flag(
            self.FLAG_S,
            bool(self.a & 0x80)
        )

        self.set_flag(
            self.FLAG_Z,
            self.a == 0
        )

        self.set_flag(
            self.FLAG_PV,
            self.parity(self.a)
        )

    def xor8(self, value):

        self.a ^= value
        self.a &= 0xFF

        self.f = 0

        self.set_flag(
            self.FLAG_S,
            bool(self.a & 0x80)
        )

        self.set_flag(
            self.FLAG_Z,
            self.a == 0
        )

        self.set_flag(
            self.FLAG_PV,
            self.parity(self.a)
        )

    def cp(self, value):

        self.sub8(
            self.a,
            value
        )

    # ==================================================
    # REGISTER DECODER
    # ==================================================

    def read_r(self, code):

        code &= 7

        if code == 0:
            return self.b

        if code == 1:
            return self.c

        if code == 2:
            return self.d

        if code == 3:
            return self.e

        if code == 4:
            return self.h

        if code == 5:
            return self.l

        if code == 6:
            return self.read_byte(
                self.get_hl()
            )

        return self.a

    def write_r(self, code, value):

        code &= 7

        value &= 0xFF

        if code == 0:
            self.b = value

        elif code == 1:
            self.c = value

        elif code == 2:
            self.d = value

        elif code == 3:
            self.e = value

        elif code == 4:
            self.h = value

        elif code == 5:
            self.l = value

        elif code == 6:
            self.write_byte(
                self.get_hl(),
                value
            )

        else:
            self.a = value

    # ==================================================
    # AUTOMATIC LD DECODER
    # ==================================================

    def decode_ld_group(self, opcode):

        destination = (
            (opcode >> 3) & 7
        )

        source = opcode & 7

        value = self.read_r(
            source
        )

        self.write_r(
            destination,
            value
        )

    # ==================================================
    # AUTOMATIC ALU DECODER
    # ==================================================

    def decode_alu_group(self, opcode):

        operation = (
            (opcode >> 3) & 7
        )

        source = opcode & 7

        value = self.read_r(
            source
        )

        if operation == 0:

            self.a = self.add8(
                self.a,
                value
            )

        elif operation == 1:

            carry = int(
                self.get_flag(
                    self.FLAG_C
                )
            )

            self.a = self.add8(
                self.a,
                value,
                carry
            )

        elif operation == 2:

            self.a = self.sub8(
                self.a,
                value
            )

        elif operation == 3:

            carry = int(
                self.get_flag(
                    self.FLAG_C
                )
            )

            self.a = self.sub8(
                self.a,
                value,
                carry
            )

        elif operation == 4:
            self.and8(value)

        elif operation == 5:
            self.xor8(value)

        elif operation == 6:
            self.or8(value)

        elif operation == 7:
            self.cp(value)

    # ==================================================
    # INC / DEC DECODER
    # ==================================================

    def decode_inc_dec(self, opcode):

        register = (
            (opcode >> 3) & 7
        )

        is_dec = opcode & 1

        value = self.read_r(
            register
        )

        if is_dec:
            value = self.dec8(value)
        else:
            value = self.inc8(value)

        self.write_r(
            register,
            value
        )

    # ==================================================
    # OPCODE TABLE
    # ==================================================

    def build_opcode_table(self):

        self.opcodes[0x00] = self.op_nop
        self.opcodes[0x76] = self.op_halt

        # LD r,n

        self.opcodes[0x3E] = self.op_ld_a_n
        self.opcodes[0x06] = self.op_ld_b_n
        self.opcodes[0x0E] = self.op_ld_c_n
        self.opcodes[0x16] = self.op_ld_d_n
        self.opcodes[0x1E] = self.op_ld_e_n
        self.opcodes[0x26] = self.op_ld_h_n
        self.opcodes[0x2E] = self.op_ld_l_n

        # LD rr,nn

        self.opcodes[0x01] = self.op_ld_bc_nn
        self.opcodes[0x11] = self.op_ld_de_nn
        self.opcodes[0x21] = self.op_ld_hl_nn
        self.opcodes[0x31] = self.op_ld_sp_nn

        # Jumps

        self.opcodes[0xC3] = self.op_jp_nn
        self.opcodes[0x18] = self.op_jr
        self.opcodes[0x20] = self.op_jr_nz
        self.opcodes[0x28] = self.op_jr_z

        # CALL / RET

        self.opcodes[0xCD] = self.op_call
        self.opcodes[0xC9] = self.op_ret

        # PUSH / POP

        self.opcodes[0xC5] = self.op_push_bc
        self.opcodes[0xC1] = self.op_pop_bc

        self.opcodes[0xD5] = self.op_push_de
        self.opcodes[0xD1] = self.op_pop_de

        self.opcodes[0xE5] = self.op_push_hl
        self.opcodes[0xE1] = self.op_pop_hl

        self.opcodes[0xF5] = self.op_push_af
        self.opcodes[0xF1] = self.op_pop_af

        # Rotates

        self.opcodes[0x07] = self.op_rlca
        self.opcodes[0x0F] = self.op_rrca
        self.opcodes[0x17] = self.op_rla
        self.opcodes[0x1F] = self.op_rra

        # Interrupts

        self.opcodes[0xF3] = self.op_di
        self.opcodes[0xFB] = self.op_ei

    # ==================================================
    # BASIC INSTRUCTIONS
    # ==================================================

    def op_nop(self):
        pass

    def op_halt(self):
        self.halted = True

    def op_ld_a_n(self):
        self.a = self.fetch_byte()

    def op_ld_b_n(self):
        self.b = self.fetch_byte()

    def op_ld_c_n(self):
        self.c = self.fetch_byte()

    def op_ld_d_n(self):
        self.d = self.fetch_byte()

    def op_ld_e_n(self):
        self.e = self.fetch_byte()

    def op_ld_h_n(self):
        self.h = self.fetch_byte()

    def op_ld_l_n(self):
        self.l = self.fetch_byte()

    # ==================================================
    # 16-BIT LOADS
    # ==================================================

    def op_ld_bc_nn(self):
        self.set_bc(
            self.fetch_word()
        )

    def op_ld_de_nn(self):
        self.set_de(
            self.fetch_word()
        )

    def op_ld_hl_nn(self):
        self.set_hl(
            self.fetch_word()
        )

    def op_ld_sp_nn(self):
        self.sp = self.fetch_word()

    # ==================================================
    # JUMPS
    # ==================================================

    def op_jp_nn(self):

        self.pc = self.fetch_word()

    def op_jr(self):

        offset = self.fetch_byte()

        if offset & 0x80:
            offset -= 0x100

        self.pc = (
            self.pc + offset
        ) & 0xFFFF

    def op_jr_nz(self):

        offset = self.fetch_byte()

        if not self.get_flag(
            self.FLAG_Z
        ):

            if offset & 0x80:
                offset -= 0x100

            self.pc = (
                self.pc + offset
            ) & 0xFFFF

    def op_jr_z(self):

        offset = self.fetch_byte()

        if self.get_flag(
            self.FLAG_Z
        ):

            if offset & 0x80:
                offset -= 0x100

            self.pc = (
                self.pc + offset
            ) & 0xFFFF

    # ==================================================
    # CALL / RET
    # ==================================================

    def op_call(self):

        address = self.fetch_word()

        self.push(
            self.pc
        )

        self.pc = address

    def op_ret(self):

        self.pc = self.pop()

    # ==================================================
    # STACK
    # ==================================================

    def push(self, value):

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

    def pop(self):

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

        return low | (high << 8)

    def op_push_bc(self):
        self.push(self.get_bc())

    def op_pop_bc(self):
        self.set_bc(self.pop())

    def op_push_de(self):
        self.push(self.get_de())

    def op_pop_de(self):
        self.set_de(self.pop())

    def op_push_hl(self):
        self.push(self.get_hl())

    def op_pop_hl(self):
        self.set_hl(self.pop())

    def op_push_af(self):

        self.push(
            (self.a << 8) |
            self.f
        )

    def op_pop_af(self):

        value = self.pop()

        self.a = (
            value >> 8
        ) & 0xFF

        self.f = value & 0xFF

    # ==================================================
    # ROTATES
    # ==================================================

    def op_rlca(self):

        carry = (
            self.a >> 7
        ) & 1

        self.a = (
            (self.a << 1) |
            carry
        ) & 0xFF

        self.set_flag(
            self.FLAG_H,
            False
        )

        self.set_flag(
            self.FLAG_N,
            False
        )

        self.set_flag(
            self.FLAG_C,
            bool(carry)
        )

    def op_rrca(self):

        carry = self.a & 1

        self.a = (
            (self.a >> 1) |
            (carry << 7)
        ) & 0xFF

        self.set_flag(
            self.FLAG_H,
            False
        )

        self.set_flag(
            self.FLAG_N,
            False
        )

        self.set_flag(
            self.FLAG_C,
            bool(carry)
        )

    def op_rla(self):

        old_carry = int(
            self.get_flag(
                self.FLAG_C
            )
        )

        carry = (
            self.a >> 7
        ) & 1

        self.a = (
            (self.a << 1) |
            old_carry
        ) & 0xFF

        self.set_flag(
            self.FLAG_H,
            False
        )

        self.set_flag(
            self.FLAG_N,
            False
        )

        self.set_flag(
            self.FLAG_C,
            bool(carry)
        )

    def op_rra(self):

        old_carry = int(
            self.get_flag(
                self.FLAG_C
            )
        )

        carry = self.a & 1

        self.a = (
            (self.a >> 1) |
            (old_carry << 7)
        ) & 0xFF

        self.set_flag(
            self.FLAG_H,
            False
        )

        self.set_flag(
            self.FLAG_N,
            False
        )

        self.set_flag(
            self.FLAG_C,
            bool(carry)
        )

    # ==================================================
    # INTERRUPTS
    # ==================================================

    def op_di(self):

        self.iff1 = False
        self.iff2 = False

    def op_ei(self):

        self.iff1 = True
        self.iff2 = True

    # ==================================================
    # FULL CB DECODER
    # ==================================================

    def execute_cb(self, opcode):

        group = (
            opcode >> 6
        ) & 3

        operation = (
            opcode >> 3
        ) & 7

        register = opcode & 7

        # ------------------------------------------
        # ROTATE / SHIFT
        # ------------------------------------------

        if group == 0:

            value = self.read_r(
                register
            )

            carry = 0

            if operation == 0:

                # RLC

                carry = (
                    value >> 7
                ) & 1

                value = (
                    (value << 1) |
                    carry
                ) & 0xFF

            elif operation == 1:

                # RRC

                carry = value & 1

                value = (
                    (value >> 1) |
                    (carry << 7)
                ) & 0xFF

            elif operation == 2:

                # RL

                old_carry = int(
                    self.get_flag(
                        self.FLAG_C
                    )
                )

                carry = (
                    value >> 7
                ) & 1

                value = (
                    (value << 1) |
                    old_carry
                ) & 0xFF

            elif operation == 3:

                # RR

                old_carry = int(
                    self.get_flag(
                        self.FLAG_C
                    )
                )

                carry = value & 1

                value = (
                    (value >> 1) |
                    (old_carry << 7)
                ) & 0xFF

            elif operation == 4:

                # SLA

                carry = (
                    value >> 7
                ) & 1

                value = (
                    value << 1
                ) & 0xFF

            elif operation == 5:

                # SRA

                carry = value & 1

                value = (
                    (value >> 1) |
                    (value & 0x80)
                ) & 0xFF

            elif operation == 6:

                # SLL

                carry = (
                    value >> 7
                ) & 1

                value = (
                    (value << 1) |
                    1
                ) & 0xFF

            elif operation == 7:

                # SRL

                carry = value & 1

                value = (
                    value >> 1
                ) & 0xFF

            self.write_r(
                register,
                value
            )

            self.f = 0

            self.set_flag(
                self.FLAG_S,
                bool(value & 0x80)
            )

            self.set_flag(
                self.FLAG_Z,
                value == 0
            )

            self.set_flag(
                self.FLAG_PV,
                self.parity(value)
            )

            self.set_flag(
                self.FLAG_C,
                bool(carry)
            )

            return

        # ------------------------------------------
        # BIT
        # ------------------------------------------

        if group == 1:

            bit = operation

            value = self.read_r(
                register
            )

            tested = (
                value &
                (1 << bit)
            )

            self.set_flag(
                self.FLAG_Z,
                tested == 0
            )

            self.set_flag(
                self.FLAG_H,
                True
            )

            self.set_flag(
                self.FLAG_N,
                False
            )

            self.set_flag(
                self.FLAG_S,
                bit == 7 and tested != 0
            )

            self.set_flag(
                self.FLAG_PV,
                tested == 0
            )

            return

        # ------------------------------------------
        # RES
        # ------------------------------------------

        if group == 2:

            bit = operation

            value = self.read_r(
                register
            )

            value &= ~(
                1 << bit
            )

            self.write_r(
                register,
                value
            )

            return

        # ------------------------------------------
        # SET
        # ------------------------------------------

        if group == 3:

            bit = operation

            value = self.read_r(
                register
            )

            value |= (
                1 << bit
            )

            self.write_r(
                register,
                value
            )

            return

    # ==================================================
    # IX / IY
    # ==================================================

    def execute_indexed(self, prefix):

        use_ix = (
            prefix == 0xDD
        )

        index = (
            self.ix
            if use_ix
            else self.iy
        )

        opcode = self.fetch_byte()

        # LD IX/IY,nn

        if opcode == 0x21:

            value = self.fetch_word()

            if use_ix:
                self.ix = value
            else:
                self.iy = value

            return

        # INC IX/IY

        if opcode == 0x23:

            index = (
                index + 1
            ) & 0xFFFF

            if use_ix:
                self.ix = index
            else:
                self.iy = index

            return

        # DEC IX/IY

        if opcode == 0x2B:

            index = (
                index - 1
            ) & 0xFFFF

            if use_ix:
                self.ix = index
            else:
                self.iy = index

            return

        # LD (nn),IX/IY

        if opcode == 0x22:

            address = self.fetch_word()

            self.write_byte(
                address,
                index & 0xFF
            )

            self.write_byte(
                address + 1,
                (index >> 8) & 0xFF
            )

            return

        # LD IX/IY,(nn)

        if opcode == 0x2A:

            address = self.fetch_word()

            low = self.read_byte(address)
            high = self.read_byte(
                address + 1
            )

            value = (
                low |
                (high << 8)
            )

            if use_ix:
                self.ix = value
            else:
                self.iy = value

            return

        # Indexed memory instructions

        if opcode in (
            0x36,
            0x46,
            0x7E,
            0x77
        ):

            displacement = (
                self.fetch_byte()
            )

            if displacement & 0x80:
                displacement -= 0x100

            address = (
                index + displacement
            ) & 0xFFFF

            if opcode == 0x36:

                value = self.fetch_byte()

                self.write_byte(
                    address,
                    value
                )

            elif opcode == 0x46:

                self.b = self.read_byte(
                    address
                )

            elif opcode == 0x7E:

                self.a = self.read_byte(
                    address
                )

            elif opcode == 0x77:

                self.write_byte(
                    address,
                    self.a
                )

            return

        print(
            "Unimplemented "
            f"{'IX' if use_ix else 'IY'} "
            f"opcode "
            f"{opcode:02X}"
        )

        self.running = False

    # ==================================================
    # ED PREFIX
    # ==================================================

    def execute_ed(self, opcode):

        # RETN

        if opcode == 0x45:

            self.pc = self.pop()

            self.iff1 = self.iff2

            return

        # RETI

        if opcode == 0x4D:

            self.pc = self.pop()

            return

        # IM 0

        if opcode == 0x46:

            self.im = 0

            return

        # IM 1

        if opcode == 0x56:

            self.im = 1

            return

        # IM 2

        if opcode == 0x5E:

            self.im = 2

            return

        # IN A,(C)

        if opcode == 0x78:

            self.a = self.io_read(
                self.get_bc()
            )

            return

        # OUT (C),A

        if opcode == 0x79:

            self.io_write(
                self.get_bc(),
                self.a
            )

            return

        print(
            "Unimplemented ED opcode "
            f"{opcode:02X}"
        )

        self.running = False

    # ==================================================
    # UNKNOWN OPCODE
    # ==================================================

    def op_unimplemented(self):

        address = (
            self.pc - 1
        ) & 0xFFFF

        opcode = self.read_byte(
            address
        )

        print()
        print("=" * 40)
        print("UNIMPLEMENTED Z80 OPCODE")
        print("=" * 40)

        print(
            f"Opcode:  0x{opcode:02X}"
        )

        print(
            f"Address: 0x{address:04X}"
        )

        print(
            f"PC:      0x{self.pc:04X}"
        )

        print(
            f"A:       0x{self.a:02X}"
        )

        print(
            f"F:       0x{self.f:02X}"
        )

        print(
            f"BC:      0x{self.get_bc():04X}"
        )

        print(
            f"DE:      0x{self.get_de():04X}"
        )

        print(
            f"HL:      0x{self.get_hl():04X}"
        )

        print(
            f"IX:      0x{self.ix:04X}"
        )

        print(
            f"IY:      0x{self.iy:04X}"
        )

        print(
            f"SP:      0x{self.sp:04X}"
        )

        print("=" * 40)

        self.running = False

    # ==================================================
    # CPU STEP
    # ==================================================

    def step(self):

        if self.halted:
            return

        opcode = self.fetch_byte()

        # ED PREFIX

        if opcode == 0xED:

            self.execute_ed(
                self.fetch_byte()
            )

            return

        # CB PREFIX

        if opcode == 0xCB:

            self.execute_cb(
                self.fetch_byte()
            )

            return

        # DD PREFIX = IX

        if opcode == 0xDD:

            self.execute_indexed(
                0xDD
            )

            return

        # FD PREFIX = IY

        if opcode == 0xFD:

            self.execute_indexed(
                0xFD
            )

            return

        # LD r,r

        if 0x40 <= opcode <= 0x7F:

            if opcode != 0x76:

                self.decode_ld_group(
                    opcode
                )

                return

        # ALU

        if 0x80 <= opcode <= 0xBF:

            self.decode_alu_group(
                opcode
            )

            return

        # INC / DEC

        if opcode in (
            0x04, 0x05,
            0x0C, 0x0D,
            0x14, 0x15,
            0x1C, 0x1D,
            0x24, 0x25,
            0x2C, 0x2D,
            0x34, 0x35,
            0x3C, 0x3D
        ):

            self.decode_inc_dec(
                opcode
            )

            return

        # Normal opcode table

        handler = self.opcodes[
            opcode
        ]

        handler()

    # ==================================================
    # RUN
    # ==================================================

    def run(self, cycles=1000000):

        count = 0

        while (
            self.running
            and not self.halted
            and count < cycles
        ):

            self.step()

            count += 1

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        memory = self.memory

        self.__init__(
            memory
        )