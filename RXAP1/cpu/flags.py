S_FLAG = 0x80
Z_FLAG = 0x40
Y_FLAG = 0x20
H_FLAG = 0x10
X_FLAG = 0x08
PV_FLAG = 0x04
N_FLAG = 0x02
C_FLAG = 0x01


def parity(value):

    value &= 0xFF

    return (
        bin(value).count("1") % 2
    ) == 0


def sz_flags(value):

    value &= 0xFF

    flags = value & (
        S_FLAG
        | Y_FLAG
        | X_FLAG
    )

    if value == 0:
        flags |= Z_FLAG

    return flags