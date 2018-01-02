import pygame
from pygame.locals import *
from cpu import CPU

class Emu:
    def __init__(self,key_release=False):
        pygame.init()
        pygame.display.set_caption("Chip8 Emulator")
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        self.screen = pygame.display.set_mode((320, 160),HWSURFACE|DOUBLEBUF)
        self.chip8bb = pygame.surface.Surface((64,32))
        self.done = False        
        self.c = CPU()
        self.clock = pygame.time.Clock()
        self.instructions = {}
        self.prev_presses = {}
        self.auto_key_release = key_release
        self.keymap = [
            pygame.K_x, #0x0
            pygame.K_1, #0x1
            pygame.K_2, #0x2
            pygame.K_3, #0x3
            pygame.K_q, #0x4
            pygame.K_w, #0x5
            pygame.K_e, #0x6
            pygame.K_a, #0x7
            pygame.K_s, #0x8
            pygame.K_d, #0x9
            pygame.K_z, #0xA
            pygame.K_c, #0xB
            pygame.K_4, #0xC
            pygame.K_r, #0xD
            pygame.K_f, #0xE
            pygame.K_v  #0xF
            ]

    def run_instruction(self):
        #check if opcode is disassembled already
        if self.c.PC not in self.instructions:
            self.instructions[self.c.PC] =  self.c.disassemble_addr(self.c.PC)
        o = self.c.read_opcode()
        self.c.run_opcode(o)

    def check_input(self):
        pressed = pygame.key.get_pressed()
        self.c.KB = 0x00
        #process input
        for k in xrange(0,16):
            if pressed[self.keymap[k]]:
                if not self.auto_key_release or \
                (self.auto_key_release and \
                not self.prev_presses[self.keymap[k]]):
                    self.c.KB |= (1 << k)
            else:
                self.c.KB &= ~(1 << k)
        self.prev_presses = pressed

    def draw(self):
        self.screen.fill((0,0,0))
        self.chip8bb.fill((0,0,0))
        for y in xrange(0,32):
            for x in xrange(0,64):
                pos = (y * 64) + x
                if self.c.VRAM[pos] == 1:
                    self.chip8bb.set_at((x,y),(255,255,255))
        self.screen.blit(pygame.transform.scale(self.chip8bb,(320,160)),(0,0))
        pygame.display.flip()

    def update_timers(self):
        if self.c.DT > 0:
            self.c.DT -= 1
        if self.c.ST > 0: 
            self.c.ST -= 1

    def mainloop(self,path):
        self.c.load_file(path,0x200)
        framecounter = 0
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.done = True
            self.check_input()
            for tickcounter in xrange(0,12):
                self.run_instruction()
            self.draw()
            self.update_timers()
            self.clock.tick(60)