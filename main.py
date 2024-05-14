import random
import pygame
from pygame import mixer
import time  # Import the time module to handle shooting cooldown

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.set_volume(0.05)  # Set background music volume to 5%
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

new_width = 80
new_height = 80

for i in range(num_of_enemies):
    img = pygame.image.load('enemy.png')
    img = pygame.transform.scale(img, (new_width, new_height))
    enemyImg.append(img)
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"
last_shot_time = time.time()  # Track the last shot time
shot_cooldown = 0.5  # Half a second cooldown between shots

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
score_textX = 10
score_textY = 10

# Sound Effects
bulletSound = mixer.Sound("laser.wav")
explosionSound = mixer.Sound("explosion.wav")
bulletSound.set_volume(0.03)
explosionSound.set_volume(0.03)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    hitbox_width = new_width - 10
    hitbox_height = new_height - 10
    enemy_rect = pygame.Rect(enemyX + 5, enemyY + 5, hitbox_width, hitbox_height)
    bullet_rect = pygame.Rect(bulletX, bulletY, bulletImg.get_width(), bulletImg.get_height())
    return enemy_rect.colliderect(bullet_rect)

def game_over_text():
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Game Loop
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready" and time.time() - last_shot_time >= shot_cooldown:
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    last_shot_time = time.time()
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    playerX += playerX_change
    playerX = max(0, min(playerX, 736))

    if not game_over:
        for i in range(num_of_enemies):
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0 or enemyX[i] >= 736:
                enemyX_change[i] = -enemyX_change[i]
                enemyY[i] += enemyY_change[i]

            if pygame.Rect(enemyX[i], enemyY[i], new_width, new_height).colliderect(pygame.Rect(playerX, playerY, playerImg.get_width(), playerImg.get_height())):
                game_over = True  # Set game over if an enemy touches the player

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                if score_value % 25 == 0:
                    for j in range(num_of_enemies):
                        enemyX_change[j] *= 1.2

                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(score_textX, score_textY)
    else:
        game_over_text()  # Show game over text only

    pygame.display.update()

