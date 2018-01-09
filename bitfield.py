import ctypes
import struct
c_uint8 = ctypes.c_uint8
c_uint16 = ctypes.c_uint16

def uint16tobytes(val):
    return struct.pack('>H',val)

def bytestouint16(b):
    return struct.unpack_from(">H",b)[0]

class Nibbles(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
            ("n3", c_uint8, 4),
            ("n4", c_uint8, 4),
            ("n1", c_uint8, 4),
            ("n2", c_uint8, 4),
        ]

class Bytes(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
            ("b2", c_uint8, 8),
            ("b1", c_uint8, 8),
        ]

class Opcode(ctypes.Union):
    _fields_ = [("nib", Nibbles),
                ("byt", Bytes),
                ("int", c_uint16)]
    def __init__(self):
        self.asuint16 = 0
    def __str__(self):
        fmtOp4 = "n1: %X n2: %X n3: %X n4: %X"
        fmtOp2 = "b1: %02X b2 : %02X"
    	result = fmtOp4 % (self.nib.n1, self.nib.n2, self.nib.n3, self.nib.n4)
        result += " " + fmtOp2 % (self.byt.b1,self.byt.b2) + " Op: %04X" % self.int
        #result = "%04X" % self.int
        return result
    def from_bytes(self,b):
        self.int = struct.unpack_from(">H",b)[0]
    def to_bytes(self):
        return struct.pack('>H',self.int)
    def from_b2(self,byts):
        self.byt.b1 = byts[0]
        self.byt.b2 = byts[1]
    def from_n4(self,nibs):
        self.nib.n1 = nibs[0]
        self.nib.n2 = nibs[1]
        self.nib.n3 = nibs[2]
        self.nib.n4 = nibs[3]
    def from_n2b(self,n2b):
        self.nib.n1 = n2b[0]
        self.nib.n2 = n2b[1]
        self.byt.b2 = n2b[2]
    def from_n3n(self,n3n):
        self.int = (n3n[0] << 12) + n3n[1]