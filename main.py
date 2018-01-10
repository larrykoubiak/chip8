from emu import Emu

if __name__ == "__main__":
    emu = Emu(key_release=False,scale=8,debug=True)
    emu.mainloop('roms/test2.ch8')