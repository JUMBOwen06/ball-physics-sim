import math
import random
import pygame

# Screen dimensions and fps are hardcoded initially, but can be changed
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

# Easy settings to change
##########################
START_BALLS = 5                     # The amount of starting balls
MIN_RADIUS, MAX_RADIUS = 10, 40     # Ball radius in pixels
RESTITUTION = 0.9                   # Ball-to-ball bounciness
WALL_BOUNCE = 0.8                   # Wall bounciness
THROW_STRENGTH = 0.15               # How hard drag-to-throw launches
STRESS_TEST_AMOUNT = 100            # Balls added when pressing S
CELL_SIZE = MAX_RADIUS * 2          # Grid cell must be at least the biggest ball's diameter
##########################

# Pygame setup
##########################
pygame.init()
font = pygame.font.Font(None, 28)                                   # Built-in font, loads faster than SysFont
small_font = pygame.font.Font(None, 22)                             # Smaller font for the controls bar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Physics Sim")
clock = pygame.time.Clock()                                         # Keeps the sim at a steady FPS
##########################

# Colours
##########################
BACKGROUND = (18, 18, 28)           # Dark navy so the blue balls stand out
WHITE = (255, 255, 255)             # HUD text and aim line
GREY = (150, 150, 160)              # Controls bar text
##########################


def speed_colour(speed, max_speed=25):  # Blends from blue (slow) to red (fast) based on speed
    t = min(speed / max_speed, 1)       # How fast the ball is from 0 to 1, capped at max_speed
    slow = (60, 120, 255)
    fast = (255, 60, 60)
    return tuple(int(s + (f - s) * t) for s, f in zip(slow, fast))


class Ball:
    def __init__(self, position_x, position_y, radius, velocity_x, velocity_y, density=1):
        self.position_x = position_x
        self.position_y = position_y

        self.radius = radius
        self.density = density
        self.mass = density * math.pi * radius**2   # Mass comes from the ball's area so bigger balls are heavier

        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    @property
    def speed(self):    # Total speed of the ball, used for the colour
        return math.hypot(self.velocity_x, self.velocity_y)

    def draw(self, screen): # Gives pygame the location and size of each ball
        pygame.draw.circle(
            screen,
            speed_colour(self.speed),
            (self.position_x, self.position_y),
            self.radius,
        )

    def apply_gravity(self, gravity):   # Applies gravity to each ball individually
        self.velocity_y += gravity

    def move(self): # Moves the ball by its velocity each frame
        self.position_x += self.velocity_x
        self.position_y += self.velocity_y

    def check_boundary_collision(self): # Keeps the ball inside the screen and bounces it off the walls
        # Left Wall
        if self.position_x - self.radius < 0:
            self.position_x = self.radius
            if self.velocity_x < 0:
                self.velocity_x *= -WALL_BOUNCE

        # Right Wall
        if self.position_x + self.radius > SCREEN_WIDTH:
            self.position_x = SCREEN_WIDTH - self.radius
            if self.velocity_x > 0:
                self.velocity_x *= -WALL_BOUNCE

        # Roof
        if self.position_y - self.radius < 0:
            self.position_y = self.radius
            if self.velocity_y < 0:
                self.velocity_y *= -WALL_BOUNCE

        # Floor
        if self.position_y + self.radius > SCREEN_HEIGHT:
            self.position_y = SCREEN_HEIGHT - self.radius
            if self.velocity_y > 0:
                self.velocity_y *= -WALL_BOUNCE
                if abs(self.velocity_y) < 1:  # Stops tiny endless hops
                    self.velocity_y = 0


def make_random_ball(): # Will give a ball random attributes so I no longer need to hard code
    radius = random.randint(MIN_RADIUS, MAX_RADIUS)
    return Ball(
        random.randint(radius, SCREEN_WIDTH - radius),
        random.randint(radius, SCREEN_HEIGHT // 2),
        radius,
        random.uniform(-8, 8),
        random.uniform(-5, 5),
    )


def resolve_collision(a, b):    # Checks one pair of balls and bounces them if they overlap
    dx = b.position_x - a.position_x
    dy = b.position_y - a.position_y
    dist = math.hypot(dx, dy)
    min_dist = a.radius + b.radius

    if dist == 0 or dist >= min_dist:   # Not touching, or exactly on top of each other
        return

    nx, ny = dx / dist, dy / dist   # Collision normal, the direction from ball a to ball b

    # Push apart, heavier ball moves less
    overlap = min_dist - dist
    total_mass = a.mass + b.mass
    a.position_x -= nx * overlap * (b.mass / total_mass)
    a.position_y -= ny * overlap * (b.mass / total_mass)
    b.position_x += nx * overlap * (a.mass / total_mass)
    b.position_y += ny * overlap * (a.mass / total_mass)

    # Relative velocity along the normal
    rel = (b.velocity_x - a.velocity_x) * nx + (b.velocity_y - a.velocity_y) * ny
    if rel >= 0:
        return  # Already separating

    # Equal and opposite impulse, scaled by mass and bounciness
    impulse = -(1 + RESTITUTION) * rel / (1 / a.mass + 1 / b.mass)
    a.velocity_x -= impulse / a.mass * nx
    a.velocity_y -= impulse / a.mass * ny
    b.velocity_x += impulse / b.mass * nx
    b.velocity_y += impulse / b.mass * ny


def check_collisions_brute(balls):  # Compares every pair of balls, O(n^2), returns how many pairs were checked
    checks = 0
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            checks += 1
            resolve_collision(balls[i], balls[j])
    return checks


def check_collisions_grid(balls):   # Spatial grid, only compares balls in the same or neighbouring cells
    grid = {}
    for i, ball in enumerate(balls):    # Puts each ball into a grid cell
        cell = (int(ball.position_x // CELL_SIZE), int(ball.position_y // CELL_SIZE))
        grid.setdefault(cell, []).append(i)

    checks = 0
    for (cx, cy), indices in grid.items():
        for ox in (-1, 0, 1):           # Looks at the 3x3 block of cells around this one
            for oy in (-1, 0, 1):
                neighbours = grid.get((cx + ox, cy + oy))
                if not neighbours:
                    continue
                for i in indices:
                    for j in neighbours:
                        if j > i:  # Each pair only once
                            checks += 1
                            resolve_collision(balls[i], balls[j])
    return checks


def ball_at(pos):   # Returns the index of the ball under the mouse, or None
    mx, my = pos
    for i in range(len(balls) - 1, -1, -1):  # Topmost (last drawn) first
        b = balls[i]
        if math.hypot(b.position_x - mx, b.position_y - my) <= b.radius:
            return i
    return None


def draw_hud(): # Draws the stats in the top left and the controls along the bottom
    lines = [
        f"FPS: {clock.get_fps():.0f}",
        f"Balls: {len(balls)}",
        f"Gravity: {gravity:.2f}",
        f"Collision: {'Spatial grid' if use_grid else 'Brute force'}",
        f"Pair checks / frame: {checks_this_frame}",
    ]
    if paused:
        lines.append("PAUSED")
    for n, line in enumerate(lines):
        screen.blit(font.render(line, True, WHITE), (10, 10 + n * 24))

    controls = (
        "Drag: throw   Right-click: delete   Space: pause   Up/Down: gravity   "
        "G: grid on/off   S: +100 balls   C: clear   R: reset"
    )
    screen.blit(small_font.render(controls, True, GREY), (10, SCREEN_HEIGHT - 24))


# Starting state
##########################
gravity = 1.0                                               # Gravity added to each ball's velocity every frame
balls = [make_random_ball() for _ in range(START_BALLS)]    # List of every ball in the sim
paused = False                                              # Space toggles this
use_grid = True                                             # G switches between spatial grid and brute force
checks_this_frame = 0                                       # Pair checks shown in the HUD

drag_start = None                                           # Where the left mouse button went down
pending_radius = 0                                          # Size of the ball being aimed
##########################

running = True
while running:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click starts aiming a throw
                drag_start = event.pos
                pending_radius = random.randint(MIN_RADIUS, MAX_RADIUS)
            elif event.button == 3:  # Right click deletes the ball under the cursor
                hit = ball_at(event.pos)
                if hit is not None:
                    balls.pop(hit)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drag_start:
            sx, sy = drag_start
            ex, ey = event.pos
            # Slingshot, pull back and the ball launches the opposite way
            vx = (sx - ex) * THROW_STRENGTH
            vy = (sy - ey) * THROW_STRENGTH
            balls.append(Ball(sx, sy, pending_radius, vx, vy))
            drag_start = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:     # Pause
                paused = not paused
            elif event.key == pygame.K_UP:      # Raise gravity
                gravity += 0.25
            elif event.key == pygame.K_DOWN:    # Lower gravity, never below 0
                gravity = max(0, gravity - 0.25)
            elif event.key == pygame.K_g:       # Toggle spatial grid
                use_grid = not use_grid
            elif event.key == pygame.K_s:       # Stress test
                balls.extend(make_random_ball() for _ in range(STRESS_TEST_AMOUNT))
            elif event.key == pygame.K_c:       # Clear all balls
                balls.clear()
            elif event.key == pygame.K_r:       # Reset
                gravity = 1.0
                balls = [make_random_ball() for _ in range(START_BALLS)]

    # Update
    if not paused:
        for ball in balls:
            ball.apply_gravity(gravity)
            ball.move()
            ball.check_boundary_collision()

        if use_grid:
            checks_this_frame = check_collisions_grid(balls)
        else:
            checks_this_frame = check_collisions_brute(balls)

    # Draw
    screen.fill(BACKGROUND)

    for ball in balls:
        ball.draw(screen)

    if drag_start:
        sx, sy = drag_start
        mx, my = pygame.mouse.get_pos()
        # Line shows the direction the ball will launch
        pygame.draw.line(screen, WHITE, drag_start, (sx + (sx - mx), sy + (sy - my)), 2)
        pygame.draw.circle(screen, WHITE, drag_start, pending_radius, 2)

    pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 1)    # Screen border
    draw_hud()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()