import regex as re
import bitfield
import os

class Assembler:
    def __init__(self):
        self.strreg = "^(?:(?P<label>[^\s\:]*):?)?" + \
              "\s*(?P<instr>[A-Zdbwinc]*) " + \
              "(?:(?P<op1>[^, ]*),\s*)?" + \
              "(?:(?P<reg2>[^, ]*),\s*)?" + \
              "(?:(?P<op2>[^, \\n]*))?\s*" + \
              "(?:; (?P<comment>.*))?$"
        self.r_line = re.compile(self.strreg)
        self.labels = {}
        self.buffer = bytearray(0xE00)
        self.position = 0
        self.cwd = ""

    def loadfilebytes(self,path):
        f = open(path,'rb')
        b = bytearray(f.read())
        f.close()
        return b
    def assemble_tokens(self,tokendict):
        ins = tokendict["instr"]
        op1 = tokendict["op1"]
        op2 = tokendict["op2"]
        reg2 = tokendict["reg2"]
        label = tokendict["label"]
        if label and label !="":
            self.labels[label] = self.position
        opcode = bitfield.Opcode()
        if(ins == "CLS"):
            opcode.from_b2((0x00,0xE0))
        elif(ins == "RET"):
            opcode.from_b2((0x00,0xEE))
        elif(ins == "JP"):
            if(op1 and op1 == "V0"):
                opcode.from_n3n((0xB,int(op2,16)))
            elif(op2.startswith("0x")):
                opcode.from_n3n((0x1,int(op2,16)))
        elif(ins == "CALL"):
            opcode.from_n3n((0x2,int(op2,16)))
        elif(ins == "SE"):
            if(op2.startswith("0x")):
                opcode.from_n2b((0x3,int(op1[1:],16),int(op2,16)))
            elif(op2.startswith("V")):
                opcode.from_n4((0x5,int(op1[1:],16),int(op2[1:],0x0)))
        elif(ins == "SNE"):
            if(op2.startswith("0x")):
                opcode.from_n2b((0x4,int(op1[1:],16),int(op2,16)))
            elif(op2.startswith("V")):
                opcode.from_n4((0x9,int(op1[1:],16),int(op2[1:],16),0x0))
        elif(ins == "LD"):
            if(op1.startswith("V")):
                if(op2.startswith("0x")):
                    opcode.from_n2b((0x6,int(op1[1:],16),int(op2,16)))
                elif(op2.startswith("V")):
                    opcode.from_n4((0x8,int(op1[1:],16),int(op2[1:],16),0x0))
                elif(op2 == "DT"):
                    opcode.from_n2b((0xF,int(op1[1:],16),0x07))
                elif(op2 == "K"):
                    opcode.from_n2b((0xF,int(op1[1:],16),0x0A))
                elif(op2 == "[I]"):
                    opcode.from_n2b((0xF,int(op1[1:],16),0x65))
            elif(op1 == "I"):
                opcode.from_n3n((0xA,int(op2,16)))
            elif(op1 == "DT"):
                opcode.from_n2b((0xF,int(op2[1:],16),0x15))
            elif(op1 == "ST"):
                opcode.from_n2b((0xF,int(op2[1:],16),0x18))
            elif(op1 == "F"):
                opcode.from_n2b((0xF,int(op2[1:],16),0x29))
            elif(op1 == "B"):
                opcode.from_n2b((0xF,int(op2[1:],16),0x33))
            elif(op1 == "[I]"):
                opcode.from_n2b((0xF,int(op2[1:],16),0x55))
        elif(ins == "ADD"):
            if(op1.startswith("V")):
                if(op2.startswith("0x")):
                    opcode.from_n2b((0x7,int(op1[1:],16),int(op2,16)))
                elif(op2.startswith("V")):
                    opcode.from_n4((0x8,int(op1[1:],16),int(op2[1:],16),0x4))
            elif(op1 == "I"):
                if(op2.startswith("V")):
                    opcode.from_n2b((0xF,int(op2[1:],16),0x1E))
        elif(ins == "OR"):
            opcode.from_n4((0x8,int(op1[1:],16),int(op2[1:],16),0x1))
        elif(ins == "AND"):
            opcode.from_n4((0x8,int(op1[1:],16),int(op2[1:],16),0x2))
        elif(ins == "XOR"):
            opcode.from_n4((0x8,int(op1[1:],16),int(op2[1:],16),0x3))
        elif(ins == "SUB"):
            opcode.from_n4((0x8,int(op1[1:],16),int(op2[1:],16),0x5))
        elif(ins == "SHR"):
            opcode.from_n4((0x8,int(op1[1:],16),0x0,0x6))
        elif(ins == "SUBN"):
            opcode.from_n4((0x8,int(op1[1:],16),int(op2[1:],16),0x7))
        elif(ins == "SHL"):
            opcode.from_n4((0x8,int(op1[1:],16),0x0,0xE))
        elif(ins == "RND"):
            opcode.from_n2b((0xC,int(op1[1:],16),int(op2,16)))
        elif(ins == "DRW"):
            opcode.from_n4((0xD,int(op1[1:],16),int(reg2[1:],16),int(op2,16)))
        elif(ins == "SKP"):
            opcode.from_n2b((0xE,int(op2[1:],16),0x9E))
        elif(ins == "SKNP"):
            opcode.from_n2b((0xE,int(op2[1:],16),0xA1))
        else:
            opcode.int = 0x00
        if(opcode.int != 0x0): # check non-opcodes
            self.buffer[self.position:self.position+2] = opcode.to_bytes()
            self.position +=2
        else:
            if(ins == "dw"):
                self.buffer[self.position:self.position+1] =int(op2,16)
                self.position +=1
            elif(ins == "db"):
                self.buffer[self.position:self.position+2] = bitfield.uint16tobytes(int(op2,16))
                self.position +=2
            elif(ins == "inc"):
                print "%04X" % self.position
                b = self.loadfilebytes(os.path.join(self.cwd,op2))
                self.buffer[self.position:self.position+len(b)] = b
                self.position += len(b)

    def parseline(self,strline):
        m = self.r_line.search(strline)
        strresult=""
        o = None
        if m is not None:
            self.assemble_tokens(m.groupdict())
            print "0x%04X: %s" % (self.position,strline) 

    def assemble_file(self,srcpath,destpath=""):
        self.position = 0
        self.cwd = os.path.dirname(srcpath)
        if destpath=="":
            destpath = srcpath.replace(".s",".bin")
        f = open(srcpath, "r")
        for line in f:
            o =a.parseline(line)
        f.close()
        self.buffer = self.buffer[0:self.position]
        o = open(destpath, "wb")
        o.write(self.buffer)
        o.close()
        return

if __name__ == "__main__":
    a = Assembler()
    a.assemble_file("src/tetris.s","roms/tetris.ch8")