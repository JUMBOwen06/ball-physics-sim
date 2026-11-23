import pygame
import math

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

pygame.init()
font = pygame.font.SysFont("Arial", 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

gravity = 1
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
ball4 = Ball(SCREEN_WIDTH/2.5, (SCREEN_HEIGHT/1.2), 15, 100, 12, -5)

balls = [ball1, ball2, ball3, ball4]
amount = len(balls)

def check_ball_collision(ball1, ball2):
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            ball1 = balls[i]
            ball2 = balls[j]

            horizontal_distance = abs(ball2.position_x - ball1.position_x)
            vertical_distance = abs(ball2.position_y - ball1.position_y)
            total_distance = math.sqrt((horizontal_distance**2) + (vertical_distance**2))

            if ball1.radius + ball2.radius >= total_distance:
                overlap = (ball1.radius + ball2.radius) - total_distance

                dx = ball2.position_x - ball1.position_x
                dy = ball2.position_y - ball1.position_y

                nx = dx / total_distance
                ny = dy / total_distance

                correction = overlap / 2

                ball1.position_x -= nx * correction
                ball1.position_y -= ny * correction

                ball2.position_x -= nx * correction
                ball2.position_y -= ny * correction

                relative_velocity = ((ball2.velocity_x - ball1.velocity_x) * nx + (ball2.velocity_y - ball1.velocity_y) * ny)

                if relative_velocity < 0:
                    print("Collision")
                    m1 = ball1.mass
                    m2 = ball2.mass
                    v1 = ball1.velocity_x
                    v2 = ball2.velocity_x

                    tmp1 = ((m1 - m2)*v1 + 2*m2*v2) / (m1 + m2)
                    tmp2 = ((m2 - m1)*v2 + 2*m1*v1) / (m2 + m1)

                    ball1.velocity_x = tmp1
                    ball2.velocity_x = tmp2

                



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

    check_ball_collision(ball1, ball2)

    pygame.display.flip()
    clock.tick(FPS)