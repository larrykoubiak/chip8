import bitfield
class Disassembler:

    def disassemble_addr(self,bytes,addr):
        str = "0x%04X: " % addr
        op = bitfield.Opcode()
        op.from_bytes(bytes[addr:addr+2])
        if(op.byt.b1 == 0x00):
            if(op.byt.b2 == 0xE0):
                return str + "CLS"
            elif(op.byt.b2 == 0xEE):
                return str + "RET"
            else:
                return str +  "NOP 0x%04X" % op.int
        elif(op.nib.n1 == 0x1):
            addr = op.int & 0xFFF
            return str + "JP 0x%04X" % addr
        elif(op.nib.n1 == 0x2):
            addr = op.int & 0xFFF
            return str + "CALL 0x%04X" % addr 
        elif(op.nib.n1 == 0x3):
            return str + "SE V%X, 0x%02X" % (op.nib.n2,op.byt.b2)
        elif(op.nib.n1 == 0x4):
            return str + "SNE V%X, 0x%02X" % (op.nib.n2,op.byt.b2)
        elif(op.nib.n1 == 0x5 and op.nib.n4 == 0x0):
            return str + "SE V%X, V%X" % (op.nib.n2,op.nib.n3)
        elif(op.nib.n1 == 0x6):
            return str + "LD V%X, 0x%02X" % (op.nib.n2,op.byt.b2)
        elif(op.nib.n1 == 0x7):
            return str + "ADD V%X, 0x%02X" % (op.nib.n2,op.byt.b2)
        elif(op.nib.n1 == 0x8):
            if(op.nib.n4 == 0x0):
                return str + "LD V%X, V%X " % (op.nib.n2,op.nib.n3)
            elif(op.nib.n4 == 0x1):
                return str + "OR V%X, V%X " % (op.nib.n2,op.nib.n3)
            elif(op.nib.n4 == 0x2):
                return str + "AND V%X, V%X " % (op.nib.n2,op.nib.n3)
            elif(op.nib.n4 == 0x3):
                return str + "XOR V%X, V%X " % (op.nib.n2,op.nib.n3)
            elif(op.nib.n4 == 0x4):
                return str + "ADD V%X, V%X " % (op.nib.n2,op.nib.n3)
            elif(op.nib.n4 == 0x5):
                return str + "SUB V%X, V%X " % (op.nib.n2,op.nib.n3)
            elif(op.nib.n4 == 0x6):
                return str + "SHR V%X " % (op.nib.n2)
            elif(op.nib.n4 == 0x7):
                return str + "SUBN V%X, V%X " % (op.nib.n2,op.nib.n3)
            elif(op.nib.n4 == 0xE):
                return str + "SHL V%X " % (op.nib.n2)
            else:
                return str + "NOP 0x%04X" % op.int
        elif(op.nib.n1 == 0x9 and op.nib.n4 == 0x0):
            return str + "SNE V%X, V%X" % (op.nib.n2, op.nib.n3)
        elif(op.nib.n1 == 0xA):
            addr = op.int & 0xFFF
            return str + "LD I,0x%03X" % addr
        elif(op.nib.n1 == 0xB):
            addr = op.int & 0xFFF
            return str + "JP V0,0x%03X" % addr
        elif(op.nib.n1 == 0xC):
            return str + "RND V%X,0x%02X" % (op.nib.n2, op.byt.b2)
        elif(op.nib.n1 == 0xD):
            return str + "DRW V%X,V%X,0x%X" % (op.nib.n2, op.nib.n3,op.nib.n4)
        elif(op.nib.n1 == 0xE):
            if(op.byt.b2 == 0x9E):
                return str + "SKP V%X" % op.nib.n2
            elif(op.byt.b2 == 0xA1):
                return str + "SKNP V%X" % op.nib.n2
            else:
                return str + "NOP 0x%04X" % op.int
        elif(op.nib.n1 == 0xF):
            if(op.byt.b2 == 0x07):
                return str + "LD V%X,DT" % op.nib.n2
            elif(op.byt.b2 == 0x0A):
                return str + "LD V%X,K" % op.nib.n2
            elif(op.byt.b2 == 0x15):
                return str + "LD DT,V%X" % op.nib.n2
            elif(op.byt.b2 == 0x18):
                return str + "LD ST,V%X" % op.nib.n2
            elif(op.byt.b2 == 0x1E):
                return str + "ADD I,V%X" % op.nib.n2
            elif(op.byt.b2 == 0x29):
                return str + "LD F,V%X" % op.nib.n2
            elif(op.byt.b2 == 0x33):
                return str + "LD B,V%X" % op.nib.n2
            elif(op.byt.b2 == 0x55):
                return str + "LD [I],V%X" % op.nib.n2
            elif(op.byt.b2 == 0x65):
                return str + "LD V%X,[I]" % op.nib.n2
            else:
                return str + "NOP 0x%04X" % op.int
        else:
            return str + "NOP 0x%04X" % op.int

    def disassemble_range(self,bytes,start,end):
        for i in xrange(start,end+2,2):
            print self.disassemble_addr(bytes,i)

    def disassemble_file(self,path,start=0x0,end=0xE00):
        f = open(path,"rb")
        b = bytearray(f.read())
        if(end>(len(b)-2)):
            end = len(b) -2
        f.close()
        self.disassemble_range(b,start,end)

if __name__ == "__main__":
    d = Disassembler()
    d.disassemble_file("roms/Tetris (19xx)(-).bin")