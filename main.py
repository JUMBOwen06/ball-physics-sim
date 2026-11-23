import pygame
import math

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


def gravity():
    gravity = -9.8
class Ball:
    def __init__(self, position_x, position_y, radius, mass, velocity_x, velocity_y, ):
        self.position_x = position_x
        self.position_y = position_y

        self.radius = radius

        self.mass = mass

        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (self.position_x, self.position_y),
            self.radius
        )


mainBall = Ball((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2), 40, 5, 0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("blue")

    mainBall.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)