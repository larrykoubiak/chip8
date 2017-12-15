class CPU:
    def __init__(self):
        self.V = bytearray(16)
        self.I = 0
        self.stack = bytearray(64)
        self.SP = 0x3F
        self.PC = 0x200
    def __str__(self):
        val = "I: %02X\nSP: %02X\nPC: %04X\n" % (self.I, self.SP,self.PC)
        for i in range(0,16):
            val += "V%X: %02X\n" % (i, self.V[i])
        return val