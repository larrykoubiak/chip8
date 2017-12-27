import pygame
import os
from cpu import CPU

_image_library = {}


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image

#pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
screen = pygame.display.set_mode((400, 300))
#pygame.mixer.music.load('Creep.xm')
#pygame.mixer.music.play(-1)

done = False
is_blue = True
x = 30
y = 30

c = CPU()
print c
clock = pygame.time.Clock()

while not done:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
    # keys
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        y -= 3
    if pressed[pygame.K_DOWN]:
        y += 3
    if pressed[pygame.K_LEFT]:
        x -= 3
    if pressed[pygame.K_RIGHT]:
        x += 3
    # graphics
    screen.fill((0, 0, 0))
    screen.blit(get_image('ball_sprite.png'), (x, y))
    pygame.display.flip()
    clock.tick(60)
