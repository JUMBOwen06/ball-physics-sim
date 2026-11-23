import pygame
import math

"""
class balls:
    xpos = float
    ypos = float
"""

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("blue")

    pygame.display.flip()

    clock.tick(FPS)