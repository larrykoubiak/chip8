from emu import Emu

if __name__ == "__main__":
    emu = Emu(key_release=False,scale=8,debug=False)
    emu.mainloop('roms/tetris.ch8')