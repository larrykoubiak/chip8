from emu import Emu
from gooey import Gooey, GooeyParser

@Gooey
def main():
    parser = GooeyParser(description='Chip-8 Emulator')
    parser.add_argument("rom",\
                        help="ROM file to be executed",\
                        action="store",\
                        widget="FileChooser")
    parser.add_argument("--key_release",\
                        help="Auto-release keys (needed for some games)",\
                        action="store_true")
    parser.add_argument("--debug",\
                        help="Debug Mode (disassemble rom code)",
                        action="store_true")
    parser.add_argument("--scale",\
                        help="Scale multiplier of window size",
                        nargs='?',\
                        default=8,\
                        type=int)
    args = parser.parse_args()
    emu = Emu(args.key_release,args.scale,args.debug)
    emu.mainloop(args.rom)
if __name__ == "__main__":
    main()