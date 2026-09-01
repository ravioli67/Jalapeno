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


def execute_ed(cpu, opcode):

    # ==========================================
    # IN r,(C)
    # ==========================================

    if 0x40 <= opcode <= 0x78:

        if opcode & 0x07 == 0:

            register = (opcode >> 3) & 0x07

            value = cpu.io_read(
                cpu.get_bc()
            )

            if register != 6:

                cpu.write_r(
                    register,
                    value
                )

            cpu.f = (
                value
                & (
                    S_FLAG
                    | Y_FLAG
                    | X_FLAG
                )
            )

            if value == 0:
                cpu.f |= Z_FLAG

            return


    # ==========================================
    # OUT (C),r
    # ==========================================

    if 0x41 <= opcode <= 0x79:

        if opcode & 0x07 == 1:

            register = (
                opcode >> 3
            ) & 0x07

            if register == 6:
                value = 0

            else:
                value = cpu.read_r(
                    register
                )

            cpu.io_write(
                cpu.get_bc(),
                value
            )

            return


    # ==========================================
    # SBC HL,rr
    # ==========================================

    if opcode in (
        0x42,
        0x52,
        0x62,
        0x72,
    ):

        pair = (
            opcode >> 4
        ) & 3

        if pair == 0:
            value = cpu.get_bc()

        elif pair == 1:
            value = cpu.get_de()

        elif pair == 2:
            value = cpu.get_hl()

        else:
            value = cpu.sp

        hl = cpu.get_hl()

        carry = (
            cpu.f & C_FLAG
        )

        result = (
            hl
            - value
            - carry
        ) & 0xFFFF

        cpu.set_hl(result)

        cpu.f = N_FLAG

        if result & 0x8000:
            cpu.f |= S_FLAG

        if result == 0:
            cpu.f |= Z_FLAG

        if (
            ((hl ^ value ^ result)
             & 0x1000)
        ):
            cpu.f |= H_FLAG

        if (
            ((hl ^ value)
             & (hl ^ result)
             & 0x8000)
        ):
            cpu.f |= 0x04

        if (
            hl < value + carry
        ):
            cpu.f |= C_FLAG

        cpu.f |= (
            (result >> 8)
            & (
                Y_FLAG
                | X_FLAG
            )
        )

        return


    # ==========================================
    # ADC HL,rr
    # ==========================================

    if opcode in (
        0x4A,
        0x5A,
        0x6A,
        0x7A,
    ):

        pair = (
            opcode >> 4
        ) & 3

        if pair == 0:
            value = cpu.get_bc()

        elif pair == 1:
            value = cpu.get_de()

        elif pair == 2:
            value = cpu.get_hl()

        else:
            value = cpu.sp

        hl = cpu.get_hl()

        carry = (
            cpu.f & C_FLAG
        )

        result = (
            hl
            + value
            + carry
        ) & 0xFFFF

        cpu.set_hl(result)

        cpu.f = 0

        if result & 0x8000:
            cpu.f |= S_FLAG

        if result == 0:
            cpu.f |= Z_FLAG

        if (
            ((hl ^ value ^ result)
             & 0x1000)
        ):
            cpu.f |= H_FLAG

        if (
            (~(hl ^ value)
             & (hl ^ result)
             & 0x8000)
        ):
            cpu.f |= PV_FLAG

        if (
            hl + value + carry
            > 0xFFFF
        ):
            cpu.f |= C_FLAG

        cpu.f |= (
            (result >> 8)
            & (
                Y_FLAG
                | X_FLAG
            )
        )

        return


    # ==========================================
    # LD (nn),rr
    # ==========================================

    if opcode in (
        0x43,
        0x53,
        0x63,
        0x73,
    ):

        address = cpu.fetch_word()

        pair = (
            opcode >> 4
        ) & 3

        if pair == 0:
            value = cpu.get_bc()

        elif pair == 1:
            value = cpu.get_de()

        elif pair == 2:
            value = cpu.get_hl()

        else:
            value = cpu.sp

        cpu.write_byte(
            address,
            value & 0xFF
        )

        cpu.write_byte(
            address + 1,
            value >> 8
        )

        return


    # ==========================================
    # LD rr,(nn)
    # ==========================================

    if opcode in (
        0x4B,
        0x5B,
        0x6B,
        0x7B,
    ):

        address = cpu.fetch_word()

        low = cpu.read_byte(
            address
        )

        high = cpu.read_byte(
            address + 1
        )

        value = (
            low
            | (high << 8)
        )

        pair = (
            opcode >> 4
        ) & 3

        if pair == 0:
            cpu.set_bc(value)

        elif pair == 1:
            cpu.set_de(value)

        elif pair == 2:
            cpu.set_hl(value)

        else:
            cpu.sp = value

        return


    # ==========================================
    # NEG
    # ==========================================

    if opcode in (
        0x44,
        0x4C,
        0x54,
        0x5C,
        0x64,
        0x6C,
        0x74,
        0x7C,
    ):

        old_a = cpu.a

        cpu.a = (
            -old_a
        ) & 0xFF

        cpu.f = N_FLAG

        if cpu.a & 0x80:
            cpu.f |= S_FLAG

        if cpu.a == 0:
            cpu.f |= Z_FLAG

        if (
            old_a & 0x0F
        ):
            cpu.f |= H_FLAG

        if old_a == 0x80:
            cpu.f |= PV_FLAG

        if old_a != 0:
            cpu.f |= C_FLAG

        cpu.f |= (
            cpu.a
            & (
                Y_FLAG
                | X_FLAG
            )
        )

        return


    # ==========================================
    # RETN / RETI
    # ==========================================

    if opcode in (
        0x45,
        0x55,
        0x65,
        0x75,
    ):

        cpu.reg.iff1 = (
            cpu.reg.iff2
        )

        cpu.pc = cpu.pop_word()

        return


    if opcode in (
        0x4D,
        0x5D,
        0x6D,
        0x7D,
    ):

        cpu.pc = cpu.pop_word()

        return


    # ==========================================
    # IM 0
    # ==========================================

    if opcode in (
        0x46,
        0x4E,
        0x66,
        0x6E,
    ):

        cpu.im = 0
        return


    # ==========================================
    # IM 1
    # ==========================================

    if opcode in (
        0x56,
        0x76,
    ):

        cpu.im = 1
        return


    # ==========================================
    # IM 2
    # ==========================================

    if opcode in (
        0x5E,
        0x7E,
    ):

        cpu.im = 2
        return


    # ==========================================
    # LD I,A
    # ==========================================

    if opcode == 0x47:

        cpu.i = cpu.a

        return


    # ==========================================
    # LD A,I
    # ==========================================

    if opcode == 0x57:

        cpu.a = cpu.i

        cpu.f &= C_FLAG

        if cpu.a & 0x80:
            cpu.f |= S_FLAG

        if cpu.a == 0:
            cpu.f |= Z_FLAG

        if cpu.reg.iff2:
            cpu.f |= PV_FLAG

        cpu.f |= (
            cpu.a
            & (
                Y_FLAG
                | X_FLAG
            )
        )

        return


    # ==========================================
    # LD R,A
    # ==========================================

    if opcode == 0x4F:

        cpu.r = cpu.a

        return


    # ==========================================
    # LD A,R
    # ==========================================

    if opcode == 0x5F:

        cpu.a = cpu.r

        cpu.f &= C_FLAG

        if cpu.a & 0x80:
            cpu.f |= S_FLAG

        if cpu.a == 0:
            cpu.f |= Z_FLAG

        if cpu.reg.iff2:
            cpu.f |= PV_FLAG

        cpu.f |= (
            cpu.a
            & (
                Y_FLAG
                | X_FLAG
            )
        )

        return


    # ==========================================
    # LDI
    # ==========================================

    if opcode == 0xA0:

        _ldi(cpu, decrement=False)

        return


    # ==========================================
    # LDD
    # ==========================================

    if opcode == 0xA8:

        _ldi(cpu, decrement=True)

        return


    # ==========================================
    # LDIR
    # ==========================================

    if opcode == 0xB0:

        while cpu.get_bc() != 0:

            _ldi(
                cpu,
                decrement=False
            )

        return


    # ==========================================
    # LDDR
    # ==========================================

    if opcode == 0xB8:

        while cpu.get_bc() != 0:

            _ldi(
                cpu,
                decrement=True
            )

        return


    # ==========================================
    # CPI
    # ==========================================

    if opcode == 0xA1:

        _cpi(cpu, decrement=False)

        return


    # ==========================================
    # CPD
    # ==========================================

    if opcode == 0xA9:

        _cpi(cpu, decrement=True)

        return


    # ==========================================
    # CPIR
    # ==========================================

    if opcode == 0xB1:

        while cpu.get_bc() != 0:

            _cpi(
                cpu,
                decrement=False
            )

            if cpu.f & Z_FLAG:
                break

        return


    # ==========================================
    # CPDR
    # ==========================================

    if opcode == 0xB9:

        while cpu.get_bc() != 0:

            _cpi(
                cpu,
                decrement=True
            )

            if cpu.f & Z_FLAG:
                break

        return


    raise NotImplementedError(
        f"Unimplemented ED opcode "
        f"{opcode:02X}"
    )


# ==================================================
# BLOCK MEMORY TRANSFER
# ==================================================

def _ldi(cpu, decrement=False):

    value = cpu.read_byte(
        cpu.get_hl()
    )

    cpu.write_byte(
        cpu.get_de(),
        value
    )

    if decrement:

        cpu.set_hl(
            cpu.get_hl() - 1
        )

        cpu.set_de(
            cpu.get_de() - 1
        )

    else:

        cpu.set_hl(
            cpu.get_hl() + 1
        )

        cpu.set_de(
            cpu.get_de() + 1
        )

    cpu.set_bc(
        cpu.get_bc() - 1
    )

    cpu.f &= (
        S_FLAG
        | Z_FLAG
        | C_FLAG
    )

    if cpu.get_bc() != 0:

        cpu.f |= PV_FLAG


# ==================================================
# BLOCK COMPARE
# ==================================================

def _cpi(cpu, decrement=False):

    value = cpu.read_byte(
        cpu.get_hl()
    )

    old_carry = (
        cpu.f & C_FLAG
    )

    old_a = cpu.a

    result = (
        old_a - value
    ) & 0xFF

    cpu.f = (
        N_FLAG
        | old_carry
    )

    if result & 0x80:
        cpu.f |= S_FLAG

    if result == 0:
        cpu.f |= Z_FLAG

    if (
        (old_a & 0x0F)
        < (value & 0x0F)
    ):
        cpu.f |= H_FLAG

    if cpu.get_bc() - 1 != 0:

        cpu.f |= PV_FLAG

    cpu.f |= (
        result
        & (
            Y_FLAG
            | X_FLAG
        )
    )

    if decrement:

        cpu.set_hl(
            cpu.get_hl() - 1
        )

    else:

        cpu.set_hl(
            cpu.get_hl() + 1
        )

    cpu.set_bc(
        cpu.get_bc() - 1
    )