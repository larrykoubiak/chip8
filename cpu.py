import bitfield
import binascii
from random import randint
import math

class CPU:

    def __init__(self):
        self.reset()

    def __str__(self):
        val =  "+------+------+--++" + "--+" * 16 + "\n"
        val += "|  PC  |  I   |SP||"
        for i in range(0,16):
            val +="V%X|" % i
        val += "\n|0x%04X|0x%04X|%02X||" % (self.PC,self.I, self.SP)
        for i in range(0,16):
            val += "%02X|" % (self.V[i])
        val += "\n" + "+------+------+--++" + "--+" * 16
        return val

    def reset(self):
        self.V = bytearray(0x10)        #REGISTERS
        self.I = 0x0000                 #ADDRESS REGISTER
        self.SP = 0x000                 #STACK POINTER
        self.PC = 0x0200                #PROGRAM COUNTER
        self.KB = 0x0000                #KEYBOARD STATUS
        self.DT = 0x00                  #DELAY TIMER
        self.ST = 0x00                  #SOUND TIMER
        self.stack = bytearray(0x40)    #STACK
        self.RAM = bytearray(0x1000)    #RAM
        self.VRAM = bytearray(0x800)    #VRAM

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
                self.VRAM = bytearray(0x800)
                return
            elif(op.byt.b2 == 0xEE):
                self.SP -=1
                self.PC = self.stack[self.SP] << 8
                self.SP -= 1
                self.PC += self.stack[self.SP]
                return
            else:
                return
        elif(op.nib.n1 == 0x1):
            addr = op.int & 0xFFF
            self.PC = addr
            return
        elif(op.nib.n1 == 0x2):
            addr = op.int & 0xFFF
            self.stack[self.SP] =self.PC & 0xFF
            self.SP += 1
            self.stack[self.SP] =self.PC >> 0x8
            self.SP += 1
            self.PC = addr
            return
        elif(op.nib.n1 == 0x3):
            if self.V[op.nib.n2] == op.byt.b2:
                self.PC += 2
            return
        elif(op.nib.n1 == 0x4):
            if self.V[op.nib.n2] != op.byt.b2:
                self.PC += 2
            return
        elif(op.nib.n1 == 0x5 and op.nib.n4 == 0x0):
            if self.V[op.nib.n2] == self.V[op.nib.n3]:
                self.PC += 2
            return
        elif(op.nib.n1 == 0x6):
            self.V[op.nib.n2] = op.byt.b2
            return
        elif(op.nib.n1 == 0x7):
            val = self.V[op.nib.n2] + op.byt.b2
            self.V[op.nib.n2] = val & 0xFF
            return
        elif(op.nib.n1 == 0x8):
            if(op.nib.n4 == 0x0):
                self.V[op.nib.n2] = self.V[op.nib.n3]
                return
            elif(op.nib.n4 == 0x1):
                self.V[op.nib.n2] |= self.V[op.nib.n3]
                return
            elif(op.nib.n4 == 0x2):
                self.V[op.nib.n2] &= self.V[op.nib.n3]
                return
            elif(op.nib.n4 == 0x3):
                self.V[op.nib.n2] ^= self.V[op.nib.n3]
                return
            elif(op.nib.n4 == 0x4):
                val = self.V[op.nib.n2] + self.V[op.nib.n3]
                self.V[0xF] = val >> 8
                self.V[op.nib.n2] = val & 0xFF
                return
            elif(op.nib.n4 == 0x5):
                val = self.V[op.nib.n2] - self.V[op.nib.n3]
                self.V[0xF] = 1 if val >= 0 else 0
                self.V[op.nib.n2] = val & 0xFF
                return
            elif(op.nib.n4 == 0x6):
                self.V[0xF] = self.V[op.nib.n2] & 0x01
                self.V[op.nib.n2] = self.V[op.nib.n2] >> 1
                return
            elif(op.nib.n4 == 0x7):
                val = self.V[op.nib.n3] - self.V[op.nib.n2]
                self.V[0xF] = 1 if val >= 0 else 0
                self.V[op.nib.n2] = val & 0xFF
                return
            elif(op.nib.n4 == 0xE):
                self.V[0xF] = self.V[op.nib.n2] >> 7
                self.V[op.nib.n2] = (self.V[op.nib.n2] << 1) & 0xFF
                return
            else:
                return
        elif(op.nib.n1 == 0x9 and op.nib.n4 == 0x0):
            if(self.V[op.nib.n2] != self.V[op.nib.n3]):
                self.PC += 2
            return
        elif(op.nib.n1 == 0xA):
            addr = op.int & 0xFFF
            self.I = addr
            return
        elif(op.nib.n1 == 0xB):
            addr = op.int & 0xFFF
            self.PC = addr + self.V[0]
            return
        elif(op.nib.n1 == 0xC):
            rnd = randint(0,255)
            self.V[op.nib.n2] = rnd & op.byt.b2
            return
        elif(op.nib.n1 == 0xD):
            x = self.V[op.nib.n2]
            y = self.V[op.nib.n3]
            n = op.nib.n4
            self.draw_sprite(x,y,n)
            return
        elif(op.nib.n1 == 0xE):
            if(op.byt.b2 == 0x9E):
                k = self.V[op.nib.n2]
                m = 1 << k
                ks = (self.KB & m) >> k
                if(ks == 1):
                    self.PC += 2
                return
            elif(op.byt.b2 == 0xA1):
                k = self.V[op.nib.n2]
                m = 1 << k
                ks = (self.KB & m) >> k
                if(ks == 0):
                    self.PC += 2
                return
            else:
                return
        elif(op.nib.n1 == 0xF):
            if(op.byt.b2 == 0x07):
                self.V[op.nib.n2] = self.DT
                return
            elif(op.byt.b2 == 0x0A):
                if(self.KB == 0x00):
                    self.PC -= 2
                else:
                    self.V[op.nib.n2] = int(math.log(self.KB, 2))
                return
            elif(op.byt.b2 == 0x15):
                self.DT = self.V[op.nib.n2]
                return
            elif(op.byt.b2 == 0x18):
                self.ST = self.V[op.nib.n2]
                return
            elif(op.byt.b2 == 0x1E):
                val = self.I + self.V[op.nib.n2]
                self.I = val & 0xFFF
            elif(op.byt.b2 == 0x29):
                self.I = self.V[op.nib.n2] * 5
            elif(op.byt.b2 == 0x33):
                s = "%03d" % self.V[op.nib.n2]
                for i in xrange(0,3):
                    self.RAM[self.I+i] = int(s[i])
                return
            elif(op.byt.b2 == 0x55):
                for i in xrange(0,op.nib.n2 + 1):
                    self.RAM[self.I+i] = self.V[i]
                #self.I+=1
                return
            elif(op.byt.b2 == 0x65):
                for i in xrange(0,op.nib.n2 + 1):
                    self.V[i] = self.RAM[self.I+i]
                #self.I+=1
                return
        else:
            return

    def draw_sprite(self,x,y,n):
        self.V[0xF] = 0
        for i in xrange (0,n):
            s = self.RAM[self.I + i]
            org = ((y + i) * 64) + x
            for b in xrange(0,8):
                pos = (org + b) & 0x7FF
                pix = (s & (0x80 >> b)) >> (7-b)
                if pix == 1 and self.VRAM[pos] == 1:
                    self.V[0xF] = 1
                self.VRAM[pos] ^= pix
        return