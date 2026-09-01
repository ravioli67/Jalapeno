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


def execute_cb(cpu, opcode):

    group = opcode >> 6
    bit = (opcode >> 3) & 0x07
    reg = opcode & 0x07

    value = cpu.read_r(reg)

    # ==========================================
    # ROTATE / SHIFT
    # ==========================================

    if group == 0:

        if bit == 0:
            # RLC
            result = (
                (value << 1)
                | (value >> 7)
            ) & 0xFF

            carry = value >> 7

        elif bit == 1:
            # RRC
            result = (
                (value >> 1)
                | ((value & 1) << 7)
            )

            carry = value & 1

        elif bit == 2:
            # RL
            old_carry = (
                cpu.f & C_FLAG
            )

            result = (
                (value << 1)
                | old_carry
            ) & 0xFF

            carry = value >> 7

        elif bit == 3:
            # RR
            old_carry = (
                cpu.f & C_FLAG
            )

            result = (
                (value >> 1)
                | (old_carry << 7)
            )

            carry = value & 1

        elif bit == 4:
            # SLA
            result = (
                value << 1
            ) & 0xFF

            carry = value >> 7

        elif bit == 5:
            # SRA
            result = (
                (value >> 1)
                | (value & 0x80)
            )

            carry = value & 1

        elif bit == 6:
            # SLL
            result = (
                (value << 1)
                | 1
            ) & 0xFF

            carry = value >> 7

        else:
            # SRL
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

        cpu.write_r(
            reg,
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

        if not (value & mask):

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

        cpu.write_r(
            reg,
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

        cpu.write_r(
            reg,
            value
        )

        return


    raise NotImplementedError(
        f"CB opcode {opcode:02X}"
    )