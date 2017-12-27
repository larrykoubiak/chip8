import ctypes
import struct
c_uint8 = ctypes.c_uint8
c_uint16 = ctypes.c_uint16

def uint16tobytes(val):
    return struct.pack('H',val)

def bytestouint16(b):
    return struct.unpack_from("H",b)[0]

class Opcode4(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
            ("op4", c_uint8, 4),
            ("op3", c_uint8, 4),
            ("op2", c_uint8, 4),
            ("op1", c_uint8, 4),
        ]

class Opcode2(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
            ("op2", c_uint8, 8),
            ("op1", c_uint8, 8),
        ]

class Opcode(ctypes.Union):
    _fields_ = [("Opcode4", Opcode4),
                ("Opcode2", Opcode2),
                ("asuint16", c_uint16)]
    def __init__(self):
        self.asuint16 = 0
    def __str__(self):
        #fmtOp4 = "Op4_1: %X Op4_2: %X Op4_3: %X Op_4: %X"
        #fmtOp2 = "Op2_1: %02X Op2_2 : %02X"
    	#result = fmtOp4 % (self.Opcode4.op1, self.Opcode4.op2, self.Opcode4.op3, self.Opcode4.op4)
        #result += " " + fmtOp2 % (self.Opcode2.op1,self.Opcode2.op2) + " Op: %04X" % self.asuint16
        result = "%04X" % self.asuint16
        return result
    def from_bytes(self,b):
        self.asuint16 = struct.unpack_from("H",b)[0]
