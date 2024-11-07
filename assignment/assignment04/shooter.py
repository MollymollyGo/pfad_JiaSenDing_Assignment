import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# Player settings
player_img = pygame.Surface((50, 50))
player_img.fill(GREEN)
player_x = SCREEN_WIDTH // 2 - 25
player_y = SCREEN_HEIGHT - 70
player_speed = 7
player_lives = 3

# Bullet settings
bullet_img = pygame.Surface((10, 30))
bullet_img.fill(RED)
bullet_speed = -10
bullet_state = "ready"
bullet_x = 0
bullet_y = player_y

# Target settings
TARGET_COUNT = 15
target_img = pygame.Surface((50, 50))
target_img.fill(WHITE)
targets = []
for _ in range(TARGET_COUNT):
    targets.append([random.randint(0, SCREEN_WIDTH - 50), random.randint(50, 300), random.choice([3, 4, 5])])

# Boss settings
boss_img = pygame.Surface((100, 100))
boss_img.fill(BLACK)
boss_x = SCREEN_WIDTH - 100
boss_y = 50
boss_speed = -5
boss_active = False

# Game state
score = 0
time_remaining = 30
game_state = "playable"


def display_text(text, x, y):
    screen_text = font.render(text, True, WHITE)
    SCREEN.blit(screen_text, [x, y])


def reset_game():
    global player_lives, bullet_state, bullet_x, bullet_y, targets, boss_active, boss_x, game_state, score, time_remaining
    player_lives = 3
    bullet_state = "ready"
    bullet_x = 0
    bullet_y = player_y
    targets = []
    for _ in range(TARGET_COUNT):
        targets.append([random.randint(0, SCREEN_WIDTH - 50), random.randint(50, 300), random.choice([3, 4, 5])])
    boss_active = False
    boss_x = SCREEN_WIDTH - 100
    game_state = "playable"
    score = 0
    time_remaining = 30


# Main game loop
while True:
    SCREEN.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x + 20
                bullet_state = "fired"

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 50:
        player_x += player_speed

    # Bullet movement
    if bullet_state == "fired":
        bullet_y += bullet_speed
        if bullet_y < 0:
            bullet_state = "ready"
            bullet_y = player_y
    else:
        bullet_x = player_x + 20
        bullet_y = player_y

    # Target movement
    for target in targets:
        target[0] += target[2]
        if target[0] > SCREEN_WIDTH or target[0] < 0:
            target[2] *= -1

    # Boss movement
    if boss_active:
        boss_x += boss_speed
        if boss_x < 0 or boss_x > SCREEN_WIDTH - 100:
            boss_speed *= -1

    # Bullet collision with targets
    for target in targets:
        if target[1] < bullet_y < target[1] + 50 and target[0] < bullet_x < target[0] + 50:
            targets.remove(target)
            bullet_state = "ready"
            bullet_y = player_y
            score += 1
            if score == TARGET_COUNT:
                boss_active = True

    # Bullet collision with boss
    if boss_active and boss_y < bullet_y < boss_y + 100 and boss_x < bullet_x < boss_x + 100:
        if score == TARGET_COUNT:
            game_state = "win"
        else:
            game_state = "lose"

    # Draw player, bullet, targets, and boss
    SCREEN.blit(player_img, (player_x, player_y))
    if bullet_state == "fired":
        SCREEN.blit(bullet_img, (bullet_x, bullet_y))
    for target in targets:
        SCREEN.blit(target_img, (target[0], target[1]))
    if boss_active:
        SCREEN.blit(boss_img, (boss_x, boss_y))

    # Draw lives and timer
    for i in range(player_lives):
        pygame.draw.rect(SCREEN, YELLOW, (10 + i * 30, 10, 20, 20))
    display_text(f"Time: {time_remaining}", SCREEN_WIDTH - 200, 10)

    # Update game state
    if time_remaining <= 0 or player_lives <= 0:
        game_state = "lose"

    if game_state != "playable":
        display_text("You Win!" if game_state == "win" else "Game Over", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        pygame.display.update()
        pygame.time.delay(2000)
        reset_game()

    # Timer countdown
    if pygame.time.get_ticks() % 1000 == 0:
        time_remaining -= 1

    # Update display
    pygame.display.update()
    clock.tick(60)
