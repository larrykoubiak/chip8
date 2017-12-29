import pygame
from pygame.locals import *
import os
from cpu import CPU

class Emu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chip8 Emulator")
        self.screen = pygame.display.set_mode((320, 160),HWSURFACE|DOUBLEBUF)
        self.chip8bb = pygame.surface.Surface((64,32))
        self.done = False        
        self.c = CPU()
        self.clock = pygame.time.Clock()
        self.instructions = {}

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

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.done = True
        # keys
        pressed = pygame.key.get_pressed()
        self.c.KB = 0x00
        if pressed[pygame.K_x]:
            self.c.KB = (1 << 0x0)
        elif pressed[pygame.K_1]: 
            self.c.KB = (1 << 0x1)
        elif pressed[pygame.K_2]:
            self.c.KB = (1 << 0x2)
        elif pressed[pygame.K_3]:
            self.c.KB = (1 << 0x3)
        elif pressed[pygame.K_q]:
            self.c.KB = (1 << 0x4)
        elif pressed[pygame.K_w]:
            self.c.KB = (1 << 0x5)
        elif pressed[pygame.K_e]:
            self.c.KB = (1 << 0x6)
        elif pressed[pygame.K_a]:
            self.c.KB = (1 << 0x7)
        elif pressed[pygame.K_s]:
            self.c.KB = (1 << 0x8)
        elif pressed[pygame.K_d]:
            self.c.KB = (1 << 0x9)
        elif pressed[pygame.K_z]:
            self.c.KB = (1 << 0xA)
        elif pressed[pygame.K_c]:
            self.c.KB = (1 << 0xB)
        elif pressed[pygame.K_4]:
            self.c.KB = (1 << 0xC)
        elif pressed[pygame.K_r]:
            self.c.KB = (1 << 0xD)
        elif pressed[pygame.K_f]:
            self.c.KB = (1 << 0xE)
        elif pressed[pygame.K_v]:
            self.c.KB = (1 << 0xF)
        if self.c.PC not in self.instructions:
            self.instructions[self.c.PC] =  self.c.disassemble_addr(self.c.PC)
        o = self.c.read_opcode()
        self.c.run_opcode(o)        
    def mainloop(self,path):
        self.c.load_file(path,0x200)
        framecounter = 0
        tickcounter = 0
        while not self.done:
            self.update()
            tickcounter += 1
            if (tickcounter >= 16):
                tickcounter = 0
                self.clock.tick(60)
                self.draw()
                if self.c.DT > 0:
                    self.c.DT -= 1
                if self.c.ST > 0: 
                    self.c.ST -= 1
                framecounter += 1
            if framecounter >= 60:
                framecounter = 0

if __name__ == "__main__":
    emu = Emu()
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.music.load('Creep.xm')
    pygame.mixer.music.play(-1)
    emu.mainloop('test.ch8')
    keylist = emu.instructions.keys()
    keylist.sort()
    for k in keylist:
        print "%s" % emu.instructions[k]