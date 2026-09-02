class Console:

    def __init__(self):

        self.output = ""
        self.input_buffer = []


    # ==================================
    # OUTPUT
    # ==================================

    def write_char(self, value):

        value &= 0xFF

        char = chr(value)

        self.output += char

        print(char, end="", flush=True)


    # ==================================
    # INPUT
    # ==================================

    def push_input(self, text):

        for char in text:

            self.input_buffer.append(
                ord(char) & 0xFF
            )


    # ==================================
    # READ INPUT
    # ==================================

    def read_char(self):

        if not self.input_buffer:

            return 0x00

        return self.input_buffer.pop(0)


    # ==================================
    # GET OUTPUT
    # ==================================

    def get_output(self):

        return self.output


    # ==================================
    # CLEAR
    # ==================================

    def clear(self):

        self.output = ""
        self.input_buffer.clear()