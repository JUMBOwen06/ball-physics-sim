import pygame
import math

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

pygame.init()
font = pygame.font.SysFont("Arial", 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

gravity = 1.0
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
        self.velocity_y += gravity

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



ball1 = Ball((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2), 40, 5, 10, 3)
ball2 = Ball(SCREEN_WIDTH/4, (SCREEN_HEIGHT/4), 20, 2, 3, 1)
ball3 = Ball(SCREEN_WIDTH/3, (SCREEN_HEIGHT/9), 35, 10, 8, -2)
ball4 = Ball(SCREEN_WIDTH/2.5, (SCREEN_HEIGHT/1.2), 15, 7, 12, -5)

balls = [ball1, ball2, ball3, ball4]
amount = len(balls)

def check_ball_collision(mainBall, secondball):
    pass
# Horizontal distance
    
# Vertical Distance
# Total distance
# Sum of radius

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("blue")
    text1 = font.render(f"Gravity: {gravity}", True, (255, 255, 255))
    text2 = font.render(f"Amount of balls: {amount}", True, (255, 255, 255))
    
    screen.blit(text1, (10,10))
    screen.blit(text2, (10, 34))

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