import pygame
import math

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

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

    def gravity(self):
        self.velocity_y += 1

    def move(self):
        self.position_x += self.velocity_x
        self.position_y += self.velocity_y

    def check_boundary_collision(self):
        # Left Wall
        if (self.position_x - self.radius <= 0):
            self.velocity_x *= -.8

        # Right Wall
        if (self.position_x + self.radius >= SCREEN_WIDTH):
            self.position_x = SCREEN_WIDTH - self.radius

            if self.velocity_x > 0:
                self.velocity_x *= -0.8

        # Roof
        if self.position_y - self.radius <= 0:
            self.velocity_y *= -0.8

        # Floor
        if (self.position_y + self.radius >= SCREEN_HEIGHT):
            self.position_y = SCREEN_HEIGHT - self.radius

            if self.velocity_y > 0:
                self.velocity_y *= -0.8

        


mainBall = Ball((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2), 40, 5, 10, 3)
secondball = Ball(SCREEN_WIDTH/4, (SCREEN_HEIGHT/4), 20, 5, 3, 1)
balls = [mainBall, secondball]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("blue")



    for circle in balls:
        circle.check_boundary_collision()
        circle.gravity()
        circle.move()
        circle.draw(screen)

    pygame.draw.rect(
        screen,
        (255, 0, 0),
        (0, 0, 1280, 720),
        5
    )

    pygame.display.flip()
    clock.tick(FPS)