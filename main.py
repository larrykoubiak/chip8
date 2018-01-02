from emu import Emu

if __name__ == "__main__":
    emu = Emu()
    emu.mainloop('tetris.rom')
    keylist = emu.instructions.keys()
    keylist.sort()
    for k in keylist:
        print "%s" % emu.instructions[k]