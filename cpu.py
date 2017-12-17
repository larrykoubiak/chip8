import bitfield

class CPU:
    def __init__(self):
        self.V = bytearray(16)
        self.I = 0
        self.stack = bytearray(64)
        self.SP = 0x3F
        self.PC = 0x200
        self.RAM = bytearray(4096)
        self.RAM[0x200:0x204] = b'\x3F\x40\xFF\xE0'
    def __str__(self):
        val = "I: %02X\nSP: %02X\nPC: %04X\n" % (self.I, self.SP,self.PC)
        for i in range(0,16):
            val += "V%X: %02X\n" % (i, self.V[i])
        return val
    def read_opcode(self):
        opcode = bitfield.Opcode()
        opcode.from_bytes(self.RAM[self.PC:self.PC+2])
        self.PC += 2
        return opcode

if __name__ == '__main__':
    c = CPU()
    o = c.read_opcode()
    print o
    o = c.read_opcode()
    print o