import pygame
from pygame.locals import *
import os
from cpu import CPU

#pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
screen = pygame.display.set_mode((320, 200),HWSURFACE|DOUBLEBUF)
chip8bb = pygame.surface.Surface((64,32))
#pygame.mixer.music.load('Creep.xm')
#pygame.mixer.music.play(-1)
running = False
done = False

c = CPU()
c.load_file('test.ch8',0x200)
clock = pygame.time.Clock()
running = True
start = pygame.time.get_ticks()
while not done:
    # events
    e = pygame.time.get_ticks() - start
    while(e < 16 and done == False) :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True
        # keys
        pressed = pygame.key.get_pressed()
        c.KB = 0
        if pressed[pygame.K_1]: 
            c.KB |= 0x1
        if pressed[pygame.K_2]:
            c.KB |= 0x2
        if pressed[pygame.K_3]:
            c.KB |= 0x4
        if(running):
            o = c.read_opcode()
            if o.int == 0x00:
                running = False
            else:
                c.run_opcode(o)
        e = pygame.time.get_ticks() - start
    # graphics
    screen.fill((0, 0, 0))
    chip8bb.fill((0,0,0))
    for y in xrange(0,32):
        for x in xrange(0,64):
            pos = (y * 64) + x
            if c.VRAM[pos] == 1:
                chip8bb.set_at((x,y),(255,255,255))
    screen.blit(pygame.transform.scale(chip8bb,(320,200)),(0,0))
    pygame.display.flip()
    start = pygame.time.get_ticks()