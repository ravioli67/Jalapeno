class Registers:

    def __init__(self):

        # Main registers

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


    # ==========================================
    # BC
    # ==========================================

    def get_bc(self):

        return (
            (self.b << 8)
            | self.c
        )


    def set_bc(self, value):

        value &= 0xFFFF

        self.b = (
            value >> 8
        ) & 0xFF

        self.c = value & 0xFF


    # ==========================================
    # DE
    # ==========================================

    def get_de(self):

        return (
            (self.d << 8)
            | self.e
        )


    def set_de(self, value):

        value &= 0xFFFF

        self.d = (
            value >> 8
        ) & 0xFF

        self.e = value & 0xFF


    # ==========================================
    # HL
    # ==========================================

    def get_hl(self):

        return (
            (self.h << 8)
            | self.l
        )


    def set_hl(self, value):

        value &= 0xFFFF

        self.h = (
            value >> 8
        ) & 0xFF

        self.l = value & 0xFF


    # ==========================================
    # RESET
    # ==========================================

    def reset(self):

        self.a = 0
        self.f = 0

        self.b = 0
        self.c = 0

        self.d = 0
        self.e = 0

        self.h = 0
        self.l = 0

        self.a_alt = 0
        self.f_alt = 0

        self.b_alt = 0
        self.c_alt = 0

        self.d_alt = 0
        self.e_alt = 0

        self.h_alt = 0
        self.l_alt = 0

        self.ix = 0
        self.iy = 0

        self.sp = 0xFFFF
        self.pc = 0

        self.i = 0
        self.r = 0

        self.iff1 = False
        self.iff2 = False

        self.im = 0