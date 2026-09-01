from .flags import (
    S_FLAG,
    Z_FLAG,
    Y_FLAG,
    H_FLAG,
    X_FLAG,
    PV_FLAG,
    N_FLAG,
    C_FLAG,
    parity,
)


def execute_indexed(cpu, prefix):

    # prefix:
    # 0xDD = IX
    # 0xFD = IY

    use_ix = prefix == 0xDD

    # ==========================================
    # INDEX REGISTER
    # ==========================================

    def get_index():

        if use_ix:
            return cpu.ix

        return cpu.iy


    def set_index(value):

        value &= 0xFFFF

        if use_ix:
            cpu.ix = value

        else:
            cpu.iy = value


    # ==========================================
    # FETCH OPCODE
    # ==========================================

    opcode = cpu.fetch_byte()


    # ==========================================
    # DD CB / FD CB
    # ==========================================

    if opcode == 0xCB:

        displacement = cpu.fetch_byte()

        if displacement & 0x80:
            displacement -= 0x100

        cb_opcode = cpu.fetch_byte()

        address = (
            get_index()
            + displacement
        ) & 0xFFFF

        return execute_indexed_cb(
            cpu,
            address,
            cb_opcode
        )


    # ==========================================
    # LD IX/IY,nn
    # ==========================================

    if opcode == 0x21:

        set_index(
            cpu.fetch_word()
        )

        return


    # ==========================================
    # LD (nn),IX/IY
    # ==========================================

    if opcode == 0x22:

        address = cpu.fetch_word()

        value = get_index()

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
    # LD IX/IY,(nn)
    # ==========================================

    if opcode == 0x2A:

        address = cpu.fetch_word()

        low = cpu.read_byte(
            address
        )

        high = cpu.read_byte(
            address + 1
        )

        set_index(
            low | (high << 8)
        )

        return


    # ==========================================
    # INC IX/IY
    # ==========================================

    if opcode == 0x23:

        set_index(
            get_index() + 1
        )

        return


    # ==========================================
    # DEC IX/IY
    # ==========================================

    if opcode == 0x2B:

        set_index(
            get_index() - 1
        )

        return


    # ==========================================
    # ADD IX/IY,BC
    # ==========================================

    if opcode == 0x09:

        _add_index(
            cpu,
            get_index(),
            cpu.get_bc(),
            set_index
        )

        return


    # ==========================================
    # ADD IX/IY,DE
    # ==========================================

    if opcode == 0x19:

        _add_index(
            cpu,
            get_index(),
            cpu.get_de(),
            set_index
        )

        return


    # ==========================================
    # ADD IX/IY,IX/IY
    # ==========================================

    if opcode == 0x29:

        _add_index(
            cpu,
            get_index(),
            get_index(),
            set_index
        )

        return


    # ==========================================
    # ADD IX/IY,SP
    # ==========================================

    if opcode == 0x39:

        _add_index(
            cpu,
            get_index(),
            cpu.sp,
            set_index
        )

        return


    # ==========================================
    # LD r,(IX/IY+d)
    # ==========================================

    if opcode in (
        0x46,
        0x4E,
        0x56,
        0x5E,
        0x66,
        0x6E,
        0x7E,
    ):

        displacement = cpu.fetch_byte()

        if displacement & 0x80:
            displacement -= 0x100

        address = (
            get_index()
            + displacement
        ) & 0xFFFF

        value = cpu.read_byte(
            address
        )

        register = (
            opcode >> 3
        ) & 7

        cpu.write_r(
            register,
            value
        )

        return


    # ==========================================
    # LD (IX/IY+d),r
    # ==========================================

    if opcode in (
        0x70,
        0x71,
        0x72,
        0x73,
        0x74,
        0x75,
        0x77,
    ):

        displacement = cpu.fetch_byte()

        if displacement & 0x80:
            displacement -= 0x100

        address = (
            get_index()
            + displacement
        ) & 0xFFFF

        register = opcode & 7

        value = cpu.read_r(
            register
        )

        cpu.write_byte(
            address,
            value
        )

        return


    # ==========================================
    # LD (IX/IY+d),n
    # ==========================================

    if opcode == 0x36:

        displacement = cpu.fetch_byte()

        if displacement & 0x80:
            displacement -= 0x100

        value = cpu.fetch_byte()

        address = (
            get_index()
            + displacement
        ) & 0xFFFF

        cpu.write_byte(
            address,
            value
        )

        return


    # ==========================================
    # INC (IX/IY+d)
    # ==========================================

    if opcode == 0x34:

        displacement = cpu.fetch_byte()

        if displacement & 0x80:
            displacement -= 0x100

        address = (
            get_index()
            + displacement
        ) & 0xFFFF

        value = cpu.read_byte(
            address
        )

        result = (
            value + 1
        ) & 0xFF

        old_carry = (
            cpu.f & C_FLAG
        )

        cpu.f = old_carry

        if result & 0x80:
            cpu.f |= S_FLAG

        if result == 0:
            cpu.f |= Z_FLAG

        if (
            (value & 0x0F) == 0x0F
        ):
            cpu.f |= H_FLAG

        if value == 0x7F:
            cpu.f |= PV_FLAG

        cpu.f |= (
            result
            & (Y_FLAG | X_FLAG)
        )

        cpu.write_byte(
            address,
            result
        )

        return


    # ==========================================
    # DEC (IX/IY+d)
    # ==========================================

    if opcode == 0x35:

        displacement = cpu.fetch_byte()

        if displacement & 0x80:
            displacement -= 0x100

        address = (
            get_index()
            + displacement
        ) & 0xFFFF

        value = cpu.read_byte(
            address
        )

        result = (
            value - 1
        ) & 0xFF

        old_carry = (
            cpu.f & C_FLAG
        )

        cpu.f = (
            old_carry
            | N_FLAG
        )

        if result & 0x80:
            cpu.f |= S_FLAG

        if result == 0:
            cpu.f |= Z_FLAG

        if (
            (value & 0x0F) == 0
        ):
            cpu.f |= H_FLAG

        if value == 0x80:
            cpu.f |= PV_FLAG

        cpu.f |= (
            result
            & (Y_FLAG | X_FLAG)
        )

        cpu.write_byte(
            address,
            result
        )

        return


    raise NotImplementedError(
        f"Indexed opcode "
        f"{opcode:02X}"
    )


# ==================================================
# INDEXED CB
# ==================================================

def execute_indexed_cb(
    cpu,
    address,
    opcode
):

    group = opcode >> 6

    bit = (
        opcode >> 3
    ) & 7

    # The register field

    register = opcode & 7

    value = cpu.read_byte(
        address
    )


    # ==========================================
    # ROTATE / SHIFT
    # ==========================================

    if group == 0:

        if bit == 0:

            result = (
                (value << 1)
                | (value >> 7)
            ) & 0xFF

            carry = value >> 7

        elif bit == 1:

            result = (
                (value >> 1)
                | ((value & 1) << 7)
            )

            carry = value & 1

        elif bit == 2:

            old_carry = (
                cpu.f & C_FLAG
            )

            result = (
                (value << 1)
                | old_carry
            ) & 0xFF

            carry = value >> 7

        elif bit == 3:

            old_carry = (
                cpu.f & C_FLAG
            )

            result = (
                (value >> 1)
                | (old_carry << 7)
            )

            carry = value & 1

        elif bit == 4:

            result = (
                value << 1
            ) & 0xFF

            carry = value >> 7

        elif bit == 5:

            result = (
                (value >> 1)
                | (value & 0x80)
            )

            carry = value & 1

        elif bit == 6:

            result = (
                (value << 1)
                | 1
            ) & 0xFF

            carry = value >> 7

        else:

            result = value >> 1

            carry = value & 1


        cpu.f = 0

        if result & 0x80:
            cpu.f |= S_FLAG

        if result == 0:
            cpu.f |= Z_FLAG

        if parity(result):
            cpu.f |= PV_FLAG

        cpu.f |= (
            result
            & (Y_FLAG | X_FLAG)
        )

        if carry:
            cpu.f |= C_FLAG


        cpu.write_byte(
            address,
            result
        )

        return


    # ==========================================
    # BIT
    # ==========================================

    if group == 1:

        mask = 1 << bit

        cpu.f &= C_FLAG

        cpu.f |= H_FLAG

        if not (
            value & mask
        ):

            cpu.f |= (
                Z_FLAG
                | PV_FLAG
            )

        if bit == 7 and (
            value & mask
        ):

            cpu.f |= S_FLAG

        cpu.f |= (
            value
            & (Y_FLAG | X_FLAG)
        )

        return


    # ==========================================
    # RES
    # ==========================================

    if group == 2:

        value &= ~(
            1 << bit
        )

        cpu.write_byte(
            address,
            value
        )

        return


    # ==========================================
    # SET
    # ==========================================

    if group == 3:

        value |= (
            1 << bit
        )

        cpu.write_byte(
            address,
            value
        )

        return


    raise NotImplementedError(
        f"Indexed CB opcode "
        f"{opcode:02X}"
    )


# ==================================================
# ADD IX/IY,rr
# ==================================================

def _add_index(
    cpu,
    index_value,
    value,
    setter
):

    result = (
        index_value
        + value
    ) & 0xFFFF

    old_carry = (
        cpu.f & C_FLAG
    )

    cpu.f = old_carry

    if (
        index_value + value
        > 0xFFFF
    ):

        cpu.f |= C_FLAG

    if (
        (index_value ^ value ^ result)
        & 0x1000
    ):

        cpu.f |= H_FLAG

    cpu.f |= (
        (result >> 8)
        & (
            Y_FLAG
            | X_FLAG
        )
    )

    setter(result)