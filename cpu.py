import bitfield
from bitfield import uint16tobytes, bytestouint16
import binascii

class CPU:
    def __init__(self):
        self.V = bytearray(16)
        self.I = 0
        self.stack = bytearray(64)
        self.SP = 0x3F
        self.PC = 0x200
        self.RAM = bytearray(4112)
    def __str__(self):
        val = "-" * 25 + "\n"
        val += "I: %02X\nSP: %02X\nPC: %04X\n" % (self.I, self.SP,self.PC)
        for i in range(0,16):
            val += "V%X: %02X\n" % (i, self.V[i])
        val += "Stack: " + binascii.hexlify(self.stack[self.SP:0x40]) + "\n"
        val += "-" * 25
        return val

    def read_opcode(self):
        opcode = bitfield.Opcode()
        b = self.RAM[self.PC:self.PC+2]
        opcode.from_bytes(b)
        self.PC += 2
        return opcode
    def run_opcode(self,opcode):
        if(opcode.Opcode2.op1 == 0x00):
            if(opcode.Opcode2.op2 == 0xE0):
                ## CLS (00E0)
                print "CLS " + str(opcode)
                return
            elif(opcode.Opcode2.op2 == 0xEE):
            ## RET (00EE)
                print "RET " + str(opcode)
                self.PC = bytestouint16(self.stack[self.SP+1:self.SP+3])
                self.SP += 2
                return
        elif(opcode.Opcode4.op1 == 0x1):
            ## JP (1nnn)
            print "JP " + str(opcode)
            addr = opcode.asuint16 & 0xFFF
            self.PC = addr
            return
        elif(opcode.Opcode4.op1 == 0x2):
            ## CALL (2nnn)
            print "CALL " + str(opcode)
            addr = opcode.asuint16 & 0xFFF
            self.stack[self.SP - 1:self.SP + 1] = uint16tobytes(self.PC)
            self.SP -= 2
            self.PC = addr
            return
        else:
            print "NOP"
            return
    def print_ram(self):
        for r in xrange(0,256):
            print "%03X : " % (r*16) + binascii.hexlify(c.RAM[r*16:(r*16)+16]).upper()

if __name__ == '__main__':
    c = CPU()
    c.RAM[0x0200:0x0206] = b'\xFE\x1F\xE0\x00\xEE\x2E'
    c.RAM[0x0EEE:0x0F00] = b'\xEE\x00'
    c.RAM[0x0FFE:0X1000] = b'\x02\x12'
    print len(c.RAM)
    print c
    o = c.read_opcode()
    while o.asuint16 != 0:
        c.run_opcode(o)
        print c
        o = c.read_opcode()