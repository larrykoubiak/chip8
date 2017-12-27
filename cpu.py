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
        val =  "+------+--+--++" + "--+" * 16 + "\n"
        val += "|  PC  |I |SP||"
        for i in range(0,16):
            val +="V%X|" % i
        val += "\n|0x%04X|%02X|%02X||" % (self.PC,self.I, self.SP)
        for i in range(0,16):
            val += "%02X|" % (self.V[i])
        val += "\n" + "+------+--+--++" + "--+" * 16
        return val

    def read_opcode(self):
        opcode = bitfield.Opcode()
        if(self.PC < 0x1000):
            b = self.RAM[self.PC:self.PC+2]
            opcode.from_bytes(b)
            self.PC += 2
        return opcode
    def run_opcode(self,op):
        if(op.byt.b1 == 0x00):
            if(op.byt.b2 == 0xE0):
                print "CLS"
                return
            elif(op.byt.b2 == 0xEE):
                print "RET"
                self.SP -=1
                self.PC = self.stack[self.SP] << 8
                self.SP -= 1
                self.PC += self.stack[self.SP]
                return
        elif(op.nib.n1 == 0x1):
            addr = op.int & 0xFFF
            print "JP 0x%04X" % addr
            self.PC = addr
            return
        elif(op.nib.n1 == 0x2):
            addr = op.int & 0xFFF
            print "CALL 0x%04X" % addr 
            self.stack[self.SP] =self.PC & 0xFF
            self.SP += 1
            self.stack[self.SP] =self.PC >> 0x8
            self.SP += 1
            self.PC = addr
            return
        elif(op.nib.n1 == 0x3):
            print "SE V%X, 0x%02X" % (op.nib.n2,op.byt.b2)
            if self.V[op.nib.n2] == op.byt.b2:
                self.PC += 2
            return
        elif(op.nib.n1 == 0x4):
            print "SNE V%X, 0x%02X" % (op.nib.n2,op.byt.b2)
            if self.V[op.nib.n2] != op.byt.b2:
                self.PC += 2
            return
        elif(op.nib.n1 == 0x5):
            print "SE V%X, V%X" % (op.nib.n2,op.nib.n3)
            if self.V[op.nib.n2] == self.V[op.nib.n3]:
                self.PC += 2
            return
        elif(op.nib.n1 == 0x6):
            print "LD V%X, 0x%02X" % (op.nib.n2,op.byt.b2)
            self.V[op.nib.n2] = op.byt.b2
            return
        elif(op.nib.n1 == 0x7):
            print "ADD V%X, 0x%02X" % (op.nib.n2,op.byt.b2)
            val = self.V[op.nib.n2] + op.byt.b2
            self.V[op.nib.n2] = val & 0xFF
            return
        elif(op.nib.n1 == 0x8):
            if(op.nib.n4 == 0x0):
                print "LD V%X, V%X " % (op.nib.n2,op.nib.n3)
                self.V[op.nib.n2] = self.V[op.nib.n3]
                return
            elif(op.nib.n4 == 0x1):
                print "OR V%X, V%X " % (op.nib.n2,op.nib.n3)
                self.V[op.nib.n2] |= self.V[op.nib.n3]
                return
            elif(op.nib.n4 == 0x2):
                print "AND V%X, V%X " % (op.nib.n2,op.nib.n3)
                self.V[op.nib.n2] &= self.V[op.nib.n3]
                return
            elif(op.nib.n4 == 0x3):
                print "XOR V%X, V%X " % (op.nib.n2,op.nib.n3)
                self.V[op.nib.n2] ^= self.V[op.nib.n3]
                return
            elif(op.nib.n4 == 0x4):
                print "ADD V%X, V%X " % (op.nib.n2,op.nib.n3)
                val = self.V[op.nib.n2] + self.V[op.nib.n3]
                self.V[0xF] = val >> 8
                self.V[op.nib.n2] = val & 0xFF
                return
            elif(op.nib.n4 == 0x5):
                print "SUB V%X, V%X " % (op.nib.n2,op.nib.n3)
                val = self.V[op.nib.n2] - self.V[op.nib.n3]
                self.V[0xF] = 1 if val >= 0 else 0
                self.V[op.nib.n2] = val & 0xFF
                return
            elif(op.nib.n4 == 0x6):
                print "SHR V%X " % (op.nib.n2)
                self.V[0xF] = self.V[op.nib.n2] & 0x01
                self.V[op.nib.n2] = self.V[op.nib.n2] >> 1
                return
            elif(op.nib.n4 == 0x7):
                print "SUBN V%X, V%X " % (op.nib.n2,op.nib.n3)
                val = self.V[op.nib.n3] - self.V[op.nib.n2]
                self.V[0xF] = 1 if val >= 0 else 0
                self.V[op.nib.n2] = val & 0xFF
                return
            elif(op.nib.n4 == 0xE):
                print "SHL V%X " % (op.nib.n2)
                self.V[0xF] = self.V[op.nib.n2] >> 7
                self.V[op.nib.n2] = self.V[op.nib.n2] << 1
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
    c.RAM[0x0212:0x0218] = b'\xFE\x63\x13\x83\x14\x83' ## LD 3,FE - XOR 3,1 - ADD 3,1
    c.RAM[0x0218:0x021E] = b'\x05\x83\x06\x83\x0E\x83' ## LD 3,FE - XOR 3,1 - ADD 3,0    
    c.RAM[0x0EEE:0x0EF4] = b'\x01\x61\x02\x71\xEE\x00' ## LD 1, 01 - ADD 1, 02 - RET
    c.RAM[0x0FFA:0X1000] = b'\x02\x60\x20\x50\x02\x12' ## LD 0, 02 - SE 0,2 - JP 202
    print "START"
    print c
    o = c.read_opcode()
    while o.int != 0:
        c.run_opcode(o)
        #print c
        o = c.read_opcode()
    print c
    print "END"