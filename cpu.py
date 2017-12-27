import bitfield
from bitfield import uint16tobytes, bytestouint16
import binascii

class CPU:
    def __init__(self):
        self.V = bytearray(0x10)
        self.I = 0x00
        self.stack = bytearray(0x40)
        self.SP = 0x00
        self.PC = 0x200
        self.RAM = bytearray(0x1000)
    def __str__(self):
        val = "-" * 63 + "\n"
        val += "|  PC  |I |SP||"
        for i in range(0,16):
            val +="V%X|" % i
        #val += "\n" + ("-" * 60)
        val += "\n|0x%04X|%02X|%02X||" % (self.PC,self.I, self.SP)
        for i in range(0,16):
            val += "%02X|" % (self.V[i])
        #val += "\n|Stack|" + binascii.hexlify(self.stack[0:0x1A]) + "|"
        val += "\n" + ("-" * 63)
        return val

    def read_opcode(self):
        opcode = bitfield.Opcode()
        if(self.PC < 0x1000):
            b = self.RAM[self.PC:self.PC+2]
            opcode.from_bytes(b)
            self.PC += 2
        return opcode
    def run_opcode(self,opcode):
        if(opcode.Opcode2.op1 == 0x00):
            if(opcode.Opcode2.op2 == 0xE0):
                ## CLS (00E0)
                print "CLS"
                return
            elif(opcode.Opcode2.op2 == 0xEE):
            ## RET (00EE)
                print "RET"
                self.SP -=1
                self.PC = self.stack[self.SP] << 8
                self.SP -= 1
                self.PC += self.stack[self.SP]
                return
        elif(opcode.Opcode4.op1 == 0x1):
            ## JP (1nnn)
            addr = opcode.asuint16 & 0xFFF
            print "JP 0x%04X" % addr
            self.PC = addr
            return
        elif(opcode.Opcode4.op1 == 0x2):
            ## CALL (2nnn)
            addr = opcode.asuint16 & 0xFFF
            print "CALL 0x%04X" % addr 
            self.stack[self.SP] =self.PC & 0xFF
            self.SP += 1
            self.stack[self.SP] =self.PC >> 0x8
            self.SP += 1
            self.PC = addr
            return
        elif(opcode.Opcode4.op1 == 0x3):
            ## SE (3xkk)
            print "SE V%X, 0x%02X" % (opcode.Opcode4.op2,opcode.Opcode2.op2)
            if self.V[opcode.Opcode4.op2] == opcode.Opcode2.op2:
                self.PC += 2
            return
        elif(opcode.Opcode4.op1 == 0x4):
            ## SNE (4xkk)
            print "SNE V%X, 0x%02X" % (opcode.Opcode4.op2,opcode.Opcode2.op2)
            if self.V[opcode.Opcode4.op2] != opcode.Opcode2.op2:
                self.PC += 2
            return
        elif(opcode.Opcode4.op1 == 0x5):
            ## SE (5xy0)
            print "SE V%X, V%X" % (opcode.Opcode4.op2,opcode.Opcode4.op3)
            if self.V[opcode.Opcode4.op2] == self.V[opcode.Opcode4.op3]:
                self.PC += 2
            return
        elif(opcode.Opcode4.op1 == 0x6):
            ## LD (6xkk)
            print "LD V%X, 0x%02X" % (opcode.Opcode4.op2,opcode.Opcode2.op2)
            self.V[opcode.Opcode4.op2] = opcode.Opcode2.op2
            return
        elif(opcode.Opcode4.op1 == 0x7):
            ## ADD (7xkk)
            print "ADD V%X, 0x%02X" % (opcode.Opcode4.op2,opcode.Opcode2.op2)
            val = self.V[opcode.Opcode4.op2] + opcode.Opcode2.op2
            self.V[opcode.Opcode4.op2] = val & 0xFF
            return
        elif(opcode.Opcode4.op1 == 0x8):
            if(opcode.Opcode4.op4 == 0x0):
                ## LD (8xy0)
                print "LD V%X, V%X " % (opcode.Opcode4.op2,opcode.Opcode4.op3)
                self.V[opcode.Opcode4.op2] = self.V[opcode.Opcode4.op3]
                return
            elif(opcode.Opcode4.op4 == 0x1):
                ## OR (8xy1)
                print "OR V%X, V%X " % (opcode.Opcode4.op2,opcode.Opcode4.op3)
                self.V[opcode.Opcode4.op2] |= self.V[opcode.Opcode4.op3]
                return
            elif(opcode.Opcode4.op4 == 0x2):
                ## AND (8xy2)
                print "AND V%X, V%X " % (opcode.Opcode4.op2,opcode.Opcode4.op3)
                self.V[opcode.Opcode4.op2] &= self.V[opcode.Opcode4.op3]
                return
        else:
            print "NOP"
            return
    def print_ram(self):
        for r in xrange(0,256):
            print "%03X : " % (r*16) + binascii.hexlify(c.RAM[r*16:(r*16)+16]).upper()

if __name__ == '__main__':
    c = CPU()
    c.RAM[0x0200:0x0206] = b'\xFA\x1F\xE0\x00\xEE\x2E' ## JP FFA - CLS - CALL EEE
    c.RAM[0x0206:0x020C] = b'\x03\x31\xFF\xFF\x03\x41' ## SE 1, 03 - NOP - SNE 1, 03
    c.RAM[0x020C:0x0212] = b'\x00\x82\x11\x82\x02\x82' ## LD 2,0 - OR 2,1 - AND 2,0
    c.RAM[0x0EEE:0x0EF4] = b'\x01\x61\x02\x71\xEE\x00' ## LD 1, 01 - ADD 1, 02 - RET
    c.RAM[0x0FFA:0X1000] = b'\x02\x60\x20\x50\x02\x12' ## LD 0, 02 - SE 0,2 - JP 202
    print "START"
    print c
    o = c.read_opcode()
    while o.asuint16 != 0:
        c.run_opcode(o)
        #print c
        o = c.read_opcode()
    print c
    print "END"