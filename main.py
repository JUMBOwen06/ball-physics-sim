import pygame
import math

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

pygame.init()
font = pygame.font.SysFont("Arial", 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

gravity = 0.5
class Ball:
    def __init__(self, position_x, position_y, radius, velocity_x, velocity_y, density=1):
        self.position_x = position_x
        self.position_y = position_y

        self.radius = radius
        self.density = density

        self.mass = density * math.pi * radius ** 2

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
        if self.position_x - self.radius < 0:
            self.position_x = self.radius
            
            if self.velocity_x < 0:
                self.velocity_x *= -0.8

        # Right Wall
        if (self.position_x + self.radius >= SCREEN_WIDTH):
            self.position_x = SCREEN_WIDTH - self.radius

            if self.velocity_x > 0:
                self.velocity_x *= -0.8

        # Roof
        if self.position_y - self.radius < 0:
            self.position_y = self.radius
            
            if self.velocity_y < 0:
                self.velocity_y *= -0.8

        # Floor
        if (self.position_y + self.radius >= SCREEN_HEIGHT):
            self.position_y = SCREEN_HEIGHT - self.radius

            if self.velocity_y > 0:
                self.velocity_y *= -0.8



ball1 = Ball((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2), 40, 10, 3)
ball2 = Ball(SCREEN_WIDTH/4, (SCREEN_HEIGHT/4), 20, 3, 1)
ball3 = Ball(SCREEN_WIDTH/3, (SCREEN_HEIGHT/9), 35, 10, -2)
ball4 = Ball(SCREEN_WIDTH/2.5, (SCREEN_HEIGHT/1.2), 15, 12, -5)

balls = [ball1, ball2, ball3, ball4]
amount = len(balls)

def check_ball_collision(balls, restitution=0.9):
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            a, b = balls[i], balls[j]

            dx = b.position_x - a.position_x
            dy = b.position_y - a.position_y
            dist = math.hypot(dx, dy)
            min_dist = a.radius + b.radius

            if dist == 0 or dist >= min_dist:
                continue

            nx, ny = dx / dist, dy / dist

            # Push apart
            overlap = min_dist - dist
            total_mass = a.mass + b.mass
            a.position_x -= nx * overlap * (b.mass / total_mass)
            a.position_y -= ny * overlap * (b.mass / total_mass)
            b.position_x += nx * overlap * (a.mass / total_mass)
            b.position_y += ny * overlap * (a.mass / total_mass)

            # Relative velocity along the normal
            rel = (b.velocity_x - a.velocity_x) * nx + (b.velocity_y - a.velocity_y) * ny
            if rel >= 0:
                continue  # already separating

            impulse = -(1 + restitution) * rel / (1 / a.mass + 1 / b.mass)
            a.velocity_x -= impulse / a.mass * nx
            a.velocity_y -= impulse / a.mass * ny
            b.velocity_x += impulse / b.mass * nx
            b.velocity_y += impulse / b.mass * ny

                



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

    for ball in balls:
        ball.gravity()
        ball.move()
        ball.check_boundary_collision()

    check_ball_collision(balls)

    for ball in balls:
        ball.draw(screen)
    
    pygame.draw.rect(
        screen,
        (0, 0, 0),
        (0, 0, 1280, 720),
        1
    )

    pygame.display.flip()
    clock.tick(FPS)