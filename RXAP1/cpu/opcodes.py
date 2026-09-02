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

def execute_opcode(cpu, opcode):

    # ==================================================
    # NOP
    # ==================================================

    if opcode == 0x00:
        return


    # ==================================================
    # HALT
    # ==================================================

    if opcode == 0x76:
        cpu.halted = True
        return


    # ==================================================
    # LD BC,nn
    # ==================================================

    if opcode == 0x01:
        cpu.set_bc(cpu.fetch_word())
        return


    # ==================================================
    # LD DE,nn
    # ==================================================

    if opcode == 0x11:
        cpu.set_de(cpu.fetch_word())
        return


    # ==================================================
    # LD HL,nn
    # ==================================================

    if opcode == 0x21:
        cpu.set_hl(cpu.fetch_word())
        return


    # ==================================================
    # LD SP,nn
    # ==================================================

    if opcode == 0x31:
        cpu.sp = cpu.fetch_word()
        return


    # ==================================================
    # LD (BC),A
    # ==================================================

    if opcode == 0x02:
        cpu.write_byte(cpu.get_bc(), cpu.a)
        return


    # ==================================================
    # LD A,(BC)
    # ==================================================

    if opcode == 0x0A:
        cpu.a = cpu.read_byte(cpu.get_bc())
        return


    # ==================================================
    # LD (DE),A
    # ==================================================

    if opcode == 0x12:
        cpu.write_byte(cpu.get_de(), cpu.a)
        return


    # ==================================================
    # LD A,(DE)
    # ==================================================

    if opcode == 0x1A:
        cpu.a = cpu.read_byte(cpu.get_de())
        return


    # ==================================================
    # LD (HL),n
    # ==================================================

    if opcode == 0x36:

        cpu.write_byte(
            cpu.get_hl(),
            cpu.fetch_byte()
        )

        return


    # ==================================================
    # LD r,n
    # ==================================================

    immediate_registers = {
        0x06: 0,  # B
        0x0E: 1,  # C
        0x16: 2,  # D
        0x1E: 3,  # E
        0x26: 4,  # H
        0x2E: 5,  # L
        0x3E: 7,  # A
    }

    if opcode in immediate_registers:

        register = immediate_registers[opcode]

        cpu.write_r(
            register,
            cpu.fetch_byte()
        )

        return

    # ==================================
    # OUT (n),A
    # ==================================

    if opcode == 0xD3:

        port = cpu.fetch_byte()

        cpu.io_write(
            port,
            cpu.reg.a
        )

        return

    # ==================================================
    # LD r,r'
    # ==================================================

    if 0x40 <= opcode <= 0x7F:

        destination = (opcode >> 3) & 7
        source = opcode & 7

        value = cpu.read_r(source)

        cpu.write_r(
            destination,
            value
        )

        return


    # ==================================================
    # LD A,(nn)
    # ==================================================

    if opcode == 0x3A:

        address = cpu.fetch_word()

        cpu.a = cpu.read_byte(address)

        return


    # ==================================================
    # LD (nn),A
    # ==================================================

    if opcode == 0x32:

        address = cpu.fetch_word()

        cpu.write_byte(
            address,
            cpu.a
        )

        return


    # ==================================================
    # LD (nn),BC
    # ==================================================

    if opcode == 0xED:
        pass


    # ==================================================
    # LD (nn),HL
    # ==================================================

    if opcode == 0x22:

        address = cpu.fetch_word()

        value = cpu.get_hl()

        cpu.write_byte(
            address,
            value & 0xFF
        )

        cpu.write_byte(
            (address + 1) & 0xFFFF,
            (value >> 8) & 0xFF
        )

        return


    # ==================================================
    # LD HL,(nn)
    # ==================================================

    if opcode == 0x2A:

        address = cpu.fetch_word()

        low = cpu.read_byte(address)

        high = cpu.read_byte(
            (address + 1) & 0xFFFF
        )

        cpu.set_hl(
            low | (high << 8)
        )

        return


    # ==================================================
    # LD (nn),BC
    # ==================================================

    if opcode == 0xED:

        return


    # ==================================================
    # INC r
    # ==================================================

    if opcode in (
        0x04,
        0x0C,
        0x14,
        0x1C,
        0x24,
        0x2C,
        0x3C,
    ):

        register = (opcode >> 3) & 7

        old = cpu.read_r(register)

        result = (old + 1) & 0xFF

        old_carry = cpu.f & C_FLAG

        cpu.f = old_carry

        if result & 0x80:
            cpu.f |= S_FLAG

        if result == 0:
            cpu.f |= Z_FLAG

        if (old & 0x0F) == 0x0F:
            cpu.f |= H_FLAG

        if old == 0x7F:
            cpu.f |= PV_FLAG

        cpu.f |= result & (Y_FLAG | X_FLAG)

        cpu.write_r(
            register,
            result
        )

        return


    # ==================================================
    # DEC r
    # ==================================================

    if opcode in (
        0x05,
        0x0D,
        0x15,
        0x1D,
        0x25,
        0x2D,
        0x3D,
    ):

        register = (opcode >> 3) & 7

        old = cpu.read_r(register)

        result = (old - 1) & 0xFF

        old_carry = cpu.f & C_FLAG

        cpu.f = old_carry | N_FLAG

        if result & 0x80:
            cpu.f |= S_FLAG

        if result == 0:
            cpu.f |= Z_FLAG

        if (old & 0x0F) == 0:
            cpu.f |= H_FLAG

        if old == 0x80:
            cpu.f |= PV_FLAG

        cpu.f |= result & (Y_FLAG | X_FLAG)

        cpu.write_r(
            register,
            result
        )

        return


    # ==================================================
    # INC (HL)
    # ==================================================

    if opcode == 0x34:

        address = cpu.get_hl()

        old = cpu.read_byte(address)

        result = (old + 1) & 0xFF

        old_carry = cpu.f & C_FLAG

        cpu.f = old_carry

        if result & 0x80:
            cpu.f |= S_FLAG

        if result == 0:
            cpu.f |= Z_FLAG

        if (old & 0x0F) == 0x0F:
            cpu.f |= H_FLAG

        if old == 0x7F:
            cpu.f |= PV_FLAG

        cpu.f |= result & (Y_FLAG | X_FLAG)

        cpu.write_byte(
            address,
            result
        )

        return


    # ==================================================
    # DEC (HL)
    # ==================================================

    if opcode == 0x35:

        address = cpu.get_hl()

        old = cpu.read_byte(address)

        result = (old - 1) & 0xFF

        old_carry = cpu.f & C_FLAG

        cpu.f = old_carry | N_FLAG

        if result & 0x80:
            cpu.f |= S_FLAG

        if result == 0:
            cpu.f |= Z_FLAG

        if (old & 0x0F) == 0:
            cpu.f |= H_FLAG

        if old == 0x80:
            cpu.f |= PV_FLAG

        cpu.f |= result & (Y_FLAG | X_FLAG)

        cpu.write_byte(
            address,
            result
        )

        return


    # ==================================================
    # INC / DEC 16-BIT
    # ==================================================

    if opcode == 0x03:
        cpu.set_bc(cpu.get_bc() + 1)
        return

    if opcode == 0x13:
        cpu.set_de(cpu.get_de() + 1)
        return

    if opcode == 0x23:
        cpu.set_hl(cpu.get_hl() + 1)
        return

    if opcode == 0x33:
        cpu.sp = (cpu.sp + 1) & 0xFFFF
        return

    if opcode == 0x0B:
        cpu.set_bc(cpu.get_bc() - 1)
        return

    if opcode == 0x1B:
        cpu.set_de(cpu.get_de() - 1)
        return

    if opcode == 0x2B:
        cpu.set_hl(cpu.get_hl() - 1)
        return

    if opcode == 0x3B:
        cpu.sp = (cpu.sp - 1) & 0xFFFF
        return


    # ==================================================
    # ADD HL,rr
    # ==================================================

    if opcode == 0x09:
        _add_hl(cpu, cpu.get_bc())
        return

    if opcode == 0x19:
        _add_hl(cpu, cpu.get_de())
        return

    if opcode == 0x29:
        _add_hl(cpu, cpu.get_hl())
        return

    if opcode == 0x39:
        _add_hl(cpu, cpu.sp)
        return


    # ==================================================
    # ADD A,r
    # ==================================================

    if 0x80 <= opcode <= 0x87:

        register = opcode & 7

        _add_a(
            cpu,
            cpu.read_r(register)
        )

        return


    # ==================================================
    # ADC A,r
    # ==================================================

    if 0x88 <= opcode <= 0x8F:

        register = opcode & 7

        _adc_a(
            cpu,
            cpu.read_r(register)
        )

        return


    # ==================================================
    # SUB r
    # ==================================================

    if 0x90 <= opcode <= 0x97:

        register = opcode & 7

        _sub_a(
            cpu,
            cpu.read_r(register)
        )

        return


    # ==================================================
    # SBC A,r
    # ==================================================

    if 0x98 <= opcode <= 0x9F:

        register = opcode & 7

        _sbc_a(
            cpu,
            cpu.read_r(register)
        )

        return


    # ==================================================
    # AND r
    # ==================================================

    if 0xA0 <= opcode <= 0xA7:

        register = opcode & 7

        _and_a(
            cpu,
            cpu.read_r(register)
        )

        return


    # ==================================================
    # XOR r
    # ==================================================

    if 0xA8 <= opcode <= 0xAF:

        register = opcode & 7

        _xor_a(
            cpu,
            cpu.read_r(register)
        )

        return


    # ==================================================
    # OR r
    # ==================================================

    if 0xB0 <= opcode <= 0xB7:

        register = opcode & 7

        _or_a(
            cpu,
            cpu.read_r(register)
        )

        return


    # ==================================================
    # CP r
    # ==================================================

    if 0xB8 <= opcode <= 0xBF:

        register = opcode & 7

        _cp(
            cpu,
            cpu.read_r(register)
        )

        return


    # ==================================================
    # IMMEDIATE ALU
    # ==================================================

    if opcode == 0xC6:
        _add_a(cpu, cpu.fetch_byte())
        return

    if opcode == 0xCE:
        _adc_a(cpu, cpu.fetch_byte())
        return

    if opcode == 0xD6:
        _sub_a(cpu, cpu.fetch_byte())
        return

    if opcode == 0xDE:
        _sbc_a(cpu, cpu.fetch_byte())
        return

    if opcode == 0xE6:
        _and_a(cpu, cpu.fetch_byte())
        return

    if opcode == 0xEE:
        _xor_a(cpu, cpu.fetch_byte())
        return

    if opcode == 0xF6:
        _or_a(cpu, cpu.fetch_byte())
        return

    if opcode == 0xFE:
        _cp(cpu, cpu.fetch_byte())
        return


    # ==================================================
    # JP nn
    # ==================================================

    if opcode == 0xC3:

        cpu.pc = cpu.fetch_word()

        return


    # ==================================================
    # CONDITIONAL JP
    # ==================================================

    if opcode in (
        0xC2,
        0xCA,
        0xD2,
        0xDA,
        0xE2,
        0xEA,
        0xF2,
        0xFA,
    ):

        address = cpu.fetch_word()

        if _condition_true(cpu, opcode):
            cpu.pc = address

        return


    # ==================================================
    # JR
    # ==================================================

    if opcode == 0x18:

        _jr(cpu)

        return


    # ==================================================
    # CONDITIONAL JR
    # ==================================================

    if opcode in (
        0x20,
        0x28,
        0x30,
        0x38,
    ):

        displacement = cpu.fetch_byte()

        if displacement & 0x80:
            displacement -= 0x100

        if _condition_true(cpu, opcode):

            cpu.pc = (
                cpu.pc + displacement
            ) & 0xFFFF

        return


    # ==================================================
    # CALL nn
    # ==================================================

    if opcode == 0xCD:

        address = cpu.fetch_word()

        cpu.push_word(cpu.pc)

        cpu.pc = address

        return


    # ==================================================
    # CONDITIONAL CALL
    # ==================================================

    if opcode in (
        0xC4,
        0xCC,
        0xD4,
        0xDC,
        0xE4,
        0xEC,
        0xF4,
        0xFC,
    ):

        address = cpu.fetch_word()

        if _condition_true(cpu, opcode):

            cpu.push_word(cpu.pc)

            cpu.pc = address

        return


    # ==================================================
    # RET
    # ==================================================

    if opcode == 0xC9:

        cpu.pc = cpu.pop_word()

        return


    # ==================================================
    # CONDITIONAL RET
    # ==================================================

    if opcode in (
        0xC0,
        0xC8,
        0xD0,
        0xD8,
        0xE0,
        0xE8,
        0xF0,
        0xF8,
    ):

        if _condition_true(cpu, opcode):

            cpu.pc = cpu.pop_word()

        return


    # ==================================================
    # RST
    # ==================================================

    rst_vectors = {
        0xC7: 0x00,
        0xCF: 0x08,
        0xD7: 0x10,
        0xDF: 0x18,
        0xE7: 0x20,
        0xEF: 0x28,
        0xF7: 0x30,
        0xFF: 0x38,
    }

    if opcode in rst_vectors:

        cpu.push_word(cpu.pc)

        cpu.pc = rst_vectors[opcode]

        return


    # ==================================================
    # PUSH
    # ==================================================

    if opcode == 0xC5:
        cpu.push_word(cpu.get_bc())
        return

    if opcode == 0xD5:
        cpu.push_word(cpu.get_de())
        return

    if opcode == 0xE5:
        cpu.push_word(cpu.get_hl())
        return

    if opcode == 0xF5:

        cpu.push_word(
            (cpu.a << 8) | cpu.f
        )

        return


    # ==================================================
    # POP
    # ==================================================

    if opcode == 0xC1:
        cpu.set_bc(cpu.pop_word())
        return

    if opcode == 0xD1:
        cpu.set_de(cpu.pop_word())
        return

    if opcode == 0xE1:
        cpu.set_hl(cpu.pop_word())
        return

    if opcode == 0xF1:

        value = cpu.pop_word()

        cpu.f = value & 0xFF
        cpu.a = (value >> 8) & 0xFF

        return


    # ==================================================
    # EX DE,HL
    # ==================================================

    if opcode == 0xEB:

        de = cpu.get_de()
        hl = cpu.get_hl()

        cpu.set_de(hl)
        cpu.set_hl(de)

        return


    # ==================================================
    # EX AF,AF'
    # ==================================================

    if opcode == 0x08:

        (
            cpu.reg.a,
            cpu.reg.a_alt
        ) = (
            cpu.reg.a_alt,
            cpu.reg.a
        )

        (
            cpu.reg.f,
            cpu.reg.f_alt
        ) = (
            cpu.reg.f_alt,
            cpu.reg.f
        )

        return


    # ==================================================
    # EXX
    # ==================================================

    if opcode == 0xD9:

        (
            cpu.reg.b,
            cpu.reg.b_alt
        ) = (
            cpu.reg.b_alt,
            cpu.reg.b
        )

        (
            cpu.reg.c,
            cpu.reg.c_alt
        ) = (
            cpu.reg.c_alt,
            cpu.reg.c
        )

        (
            cpu.reg.d,
            cpu.reg.d_alt
        ) = (
            cpu.reg.d_alt,
            cpu.reg.d
        )

        (
            cpu.reg.e,
            cpu.reg.e_alt
        ) = (
            cpu.reg.e_alt,
            cpu.reg.e
        )

        (
            cpu.reg.h,
            cpu.reg.h_alt
        ) = (
            cpu.reg.h_alt,
            cpu.reg.h
        )

        (
            cpu.reg.l,
            cpu.reg.l_alt
        ) = (
            cpu.reg.l_alt,
            cpu.reg.l
        )

        return


    # ==================================================
    # EX (SP),HL
    # ==================================================

    if opcode == 0xE3:

        low = cpu.read_byte(cpu.sp)

        high = cpu.read_byte(
            (cpu.sp + 1) & 0xFFFF
        )

        memory_value = (
            low | (high << 8)
        )

        hl = cpu.get_hl()

        cpu.write_byte(
            cpu.sp,
            hl & 0xFF
        )

        cpu.write_byte(
            (cpu.sp + 1) & 0xFFFF,
            (hl >> 8) & 0xFF
        )

        cpu.set_hl(
            memory_value
        )

        return


    # ==================================================
    # JP (HL)
    # ==================================================

    if opcode == 0xE9:

        cpu.pc = cpu.get_hl()

        return


    # ==================================================
    # LD SP,HL
    # ==================================================

    if opcode == 0xF9:

        cpu.sp = cpu.get_hl()

        return


    # ==================================================
    # RLCA
    # ==================================================

    if opcode == 0x07:

        old = cpu.a

        carry = (old >> 7) & 1

        cpu.a = (
            (old << 1) | carry
        ) & 0xFF

        cpu.f &= (
            S_FLAG |
            Z_FLAG |
            PV_FLAG
        )

        cpu.f &= ~H_FLAG
        cpu.f &= ~N_FLAG

        cpu.f |= cpu.a & (
            Y_FLAG | X_FLAG
        )

        if carry:
            cpu.f |= C_FLAG

        return


    # ==================================================
    # RRCA
    # ==================================================

    if opcode == 0x0F:

        old = cpu.a

        carry = old & 1

        cpu.a = (
            (old >> 1) |
            (carry << 7)
        )

        cpu.f &= (
            S_FLAG |
            Z_FLAG |
            PV_FLAG
        )

        cpu.f &= ~H_FLAG
        cpu.f &= ~N_FLAG

        cpu.f |= cpu.a & (
            Y_FLAG | X_FLAG
        )

        if carry:
            cpu.f |= C_FLAG

        return


    # ==================================================
    # RLA
    # ==================================================

    if opcode == 0x17:

        old = cpu.a

        old_carry = cpu.f & C_FLAG

        carry = (old >> 7) & 1

        cpu.a = (
            (old << 1) |
            old_carry
        ) & 0xFF

        cpu.f &= (
            S_FLAG |
            Z_FLAG |
            PV_FLAG
        )

        cpu.f &= ~H_FLAG
        cpu.f &= ~N_FLAG

        cpu.f |= cpu.a & (
            Y_FLAG | X_FLAG
        )

        if carry:
            cpu.f |= C_FLAG

        return


    # ==================================================
    # RRA
    # ==================================================

    if opcode == 0x1F:

        old = cpu.a

        old_carry = cpu.f & C_FLAG

        carry = old & 1

        cpu.a = (
            (old >> 1) |
            (old_carry << 7)
        )

        cpu.f &= (
            S_FLAG |
            Z_FLAG |
            PV_FLAG
        )

        cpu.f &= ~H_FLAG
        cpu.f &= ~N_FLAG

        cpu.f |= cpu.a & (
            Y_FLAG | X_FLAG
        )

        if carry:
            cpu.f |= C_FLAG

        return


    # ==================================================
    # DAA
    # ==================================================

    if opcode == 0x27:

        old_a = cpu.a

        correction = 0

        carry = bool(
            cpu.f & C_FLAG
        )

        if (
            cpu.f & H_FLAG
            or (
                not (cpu.f & N_FLAG)
                and (old_a & 0x0F) > 9
            )
        ):
            correction |= 0x06

        if (
            carry
            or (
                not (cpu.f & N_FLAG)
                and old_a > 0x99
            )
        ):
            correction |= 0x60
            carry = True

        if cpu.f & N_FLAG:
            result = (
                old_a - correction
            ) & 0xFF
        else:
            result = (
                old_a + correction
            ) & 0xFF

        cpu.a = result

        old_n = cpu.f & N_FLAG

        cpu.f = old_n

        if result & 0x80:
            cpu.f |= S_FLAG

        if result == 0:
            cpu.f |= Z_FLAG

        if bin(result).count("1") % 2 == 0:
            cpu.f |= PV_FLAG

        cpu.f |= result & (
            Y_FLAG | X_FLAG
        )

        if carry:
            cpu.f |= C_FLAG

        return


    # ==================================================
    # CPL
    # ==================================================

    if opcode == 0x2F:

        cpu.a ^= 0xFF

        cpu.f |= (
            H_FLAG |
            N_FLAG
        )

        cpu.f &= ~(
            S_FLAG |
            Z_FLAG |
            PV_FLAG |
            C_FLAG
        )

        cpu.f |= cpu.a & (
            Y_FLAG | X_FLAG
        )

        return


    # ==================================================
    # SCF
    # ==================================================

    if opcode == 0x37:

        cpu.f &= ~(
            H_FLAG |
            N_FLAG
        )

        cpu.f |= C_FLAG

        cpu.f |= cpu.a & (
            Y_FLAG | X_FLAG
        )

        return


    # ==================================================
    # CCF
    # ==================================================

    if opcode == 0x3F:

        old_carry = cpu.f & C_FLAG

        cpu.f &= ~N_FLAG

        if old_carry:
            cpu.f |= H_FLAG
            cpu.f &= ~C_FLAG
        else:
            cpu.f &= ~H_FLAG
            cpu.f |= C_FLAG

        cpu.f |= cpu.a & (
            Y_FLAG | X_FLAG
        )

        return


    # ==================================================
    # DI
    # ==================================================

    if opcode == 0xF3:

        cpu.reg.iff1 = False
        cpu.reg.iff2 = False

        return


    # ==================================================
    # EI
    # ==================================================

    if opcode == 0xFB:

        cpu.reg.iff1 = True
        cpu.reg.iff2 = True

        return


    # ==================================================
    # UNKNOWN
    # ==================================================

    raise NotImplementedError(
        f"Opcode {opcode:02X} "
        f"not implemented at "
        f"{(cpu.pc - 1) & 0xFFFF:04X}"
    )


# ======================================================
# CONDITIONS
# ======================================================

def _condition_true(cpu, opcode):

    condition = (
        opcode >> 3
    ) & 7

    if condition == 0:
        return not (cpu.f & Z_FLAG)

    if condition == 1:
        return bool(cpu.f & Z_FLAG)

    if condition == 2:
        return not (cpu.f & C_FLAG)

    if condition == 3:
        return bool(cpu.f & C_FLAG)

    if condition == 4:
        return not (cpu.f & PV_FLAG)

    if condition == 5:
        return bool(cpu.f & PV_FLAG)

    if condition == 6:
        return not (cpu.f & S_FLAG)

    if condition == 7:
        return bool(cpu.f & S_FLAG)

    return False


# ======================================================
# JR
# ======================================================

def _jr(cpu):

    displacement = cpu.fetch_byte()

    if displacement & 0x80:
        displacement -= 0x100

    cpu.pc = (
        cpu.pc + displacement
    ) & 0xFFFF


# ======================================================
# ADD HL
# ======================================================

def _add_hl(cpu, value):

    hl = cpu.get_hl()

    result = (
        hl + value
    ) & 0xFFFF

    cpu.f &= (
        S_FLAG |
        Z_FLAG |
        PV_FLAG
    )

    if hl + value > 0xFFFF:
        cpu.f |= C_FLAG

    if (
        (hl ^ value ^ result)
        & 0x1000
    ):
        cpu.f |= H_FLAG

    cpu.f |= (
        result >> 8
    ) & (
        Y_FLAG | X_FLAG
    )

    cpu.set_hl(result)


# ======================================================
# ADD A
# ======================================================

def _add_a(cpu, value):

    a = cpu.a

    result = (
        a + value
    ) & 0xFF

    cpu.f = 0

    if result & 0x80:
        cpu.f |= S_FLAG

    if result == 0:
        cpu.f |= Z_FLAG

    if (
        (a ^ value ^ result)
        & 0x10
    ):
        cpu.f |= H_FLAG

    if (
        (~(a ^ value)
        & (a ^ result)
        & 0x80)
    ):
        cpu.f |= PV_FLAG

    if a + value > 0xFF:
        cpu.f |= C_FLAG

    cpu.f |= result & (
        Y_FLAG | X_FLAG
    )

    cpu.a = result


# ======================================================
# ADC A
# ======================================================

def _adc_a(cpu, value):

    a = cpu.a

    carry = 1 if (
        cpu.f & C_FLAG
    ) else 0

    total = (
        a + value + carry
    )

    result = total & 0xFF

    cpu.f = 0

    if result & 0x80:
        cpu.f |= S_FLAG

    if result == 0:
        cpu.f |= Z_FLAG

    if (
        (a ^ value ^ result)
        & 0x10
    ):
        cpu.f |= H_FLAG

    if (
        (~(a ^ value)
        & (a ^ result)
        & 0x80)
    ):
        cpu.f |= PV_FLAG

    if total > 0xFF:
        cpu.f |= C_FLAG

    cpu.f |= result & (
        Y_FLAG | X_FLAG
    )

    cpu.a = result


# ======================================================
# SUB A
# ======================================================

def _sub_a(cpu, value):

    a = cpu.a

    result = (
        a - value
    ) & 0xFF

    cpu.f = N_FLAG

    if result & 0x80:
        cpu.f |= S_FLAG

    if result == 0:
        cpu.f |= Z_FLAG

    if (
        (a ^ value ^ result)
        & 0x10
    ):
        cpu.f |= H_FLAG

    if (
        ((a ^ value)
        & (a ^ result)
        & 0x80)
    ):
        cpu.f |= PV_FLAG

    if a < value:
        cpu.f |= C_FLAG

    cpu.f |= result & (
        Y_FLAG | X_FLAG
    )

    cpu.a = result


# ======================================================
# SBC A
# ======================================================

def _sbc_a(cpu, value):

    a = cpu.a

    carry = 1 if (
        cpu.f & C_FLAG
    ) else 0

    total = (
        a - value - carry
    )

    result = total & 0xFF

    cpu.f = N_FLAG

    if result & 0x80:
        cpu.f |= S_FLAG

    if result == 0:
        cpu.f |= Z_FLAG

    if (
        (a ^ value ^ result)
        & 0x10
    ):
        cpu.f |= H_FLAG

    if (
        ((a ^ value)
        & (a ^ result)
        & 0x80)
    ):
        cpu.f |= PV_FLAG

    if total < 0:
        cpu.f |= C_FLAG

    cpu.f |= result & (
        Y_FLAG | X_FLAG
    )

    cpu.a = result


# ======================================================
# AND
# ======================================================

def _and_a(cpu, value):

    result = cpu.a & value

    cpu.a = result

    cpu.f = H_FLAG

    if result & 0x80:
        cpu.f |= S_FLAG

    if result == 0:
        cpu.f |= Z_FLAG

    if bin(result).count("1") % 2 == 0:
        cpu.f |= PV_FLAG

    cpu.f |= result & (
        Y_FLAG | X_FLAG
    )


# ======================================================
# XOR
# ======================================================

def _xor_a(cpu, value):

    result = cpu.a ^ value

    cpu.a = result

    cpu.f = 0

    if result & 0x80:
        cpu.f |= S_FLAG

    if result == 0:
        cpu.f |= Z_FLAG

    if bin(result).count("1") % 2 == 0:
        cpu.f |= PV_FLAG

    cpu.f |= result & (
        Y_FLAG | X_FLAG
    )


# ======================================================
# OR
# ======================================================

def _or_a(cpu, value):

    result = cpu.a | value

    cpu.a = result

    cpu.f = 0

    if result & 0x80:
        cpu.f |= S_FLAG

    if result == 0:
        cpu.f |= Z_FLAG

    if bin(result).count("1") % 2 == 0:
        cpu.f |= PV_FLAG

    cpu.f |= result & (
        Y_FLAG | X_FLAG
    )


# ======================================================
# CP
# ======================================================

def _cp(cpu, value):

    a = cpu.a

    result = (
        a - value
    ) & 0xFF

    cpu.f = N_FLAG

    if result & 0x80:
        cpu.f |= S_FLAG

    if result == 0:
        cpu.f |= Z_FLAG

    if (
        (a ^ value ^ result)
        & 0x10
    ):
        cpu.f |= H_FLAG

    if (
        ((a ^ value)
        & (a ^ result)
        & 0x80)
    ):
        cpu.f |= PV_FLAG

    if a < value:
        cpu.f |= C_FLAG

    cpu.f |= value & (
        Y_FLAG | X_FLAG
    )