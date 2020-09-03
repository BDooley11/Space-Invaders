import random
import math

import pygame
from pygame import mixer

# initialise pygame
pygame.init()

# create game display width X height
screen = pygame.display.set_mode((800,600))

# Background 800 X 600
background = pygame.image.load('Images/background.png')

# Background sound -1 value means play on loop
mixer.music.load('Music/background.wav')
mixer.music.play(-1)

# Title and Icon 32px
pygame.display.set_caption('Space-Invaders')
icon = pygame.image.load('Images/ufo.png')
pygame.display.set_icon(icon)

# Player 64px
playerImg = pygame.image.load('Images/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy 64px - create lists as multiple enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for x in range(num_of_enemies): 
    enemyImg.append(pygame.image.load('Images/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet 32px
# Ready state means cant see bullet
# Fire state means bullet is moving 
bulletImg = pygame.image.load('Images/bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0 
# parameters is font type and size
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200,250))

# blit means draw, two parameters,image and coordinates.
def player(x,y):
    screen.blit(playerImg, (x, y))

# blit means draw, two parameters,image and coordinates.
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    # 16 and 10 to make sure bullet is always fired from centre of ship
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    # formula to get distance between two coordinates
    distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

#Game Loop
running = True
while running:

    # three values of RGB(red,green,blue) for screen colour
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke check if right or left arrow key. Set speed of ships movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                # add if condition as if don't when press space bar the bullet would change x coordinate mid flight
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('Music/laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        # check if key pressed has been released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    #set restrictions to stop player ship going outside borders. 736 as ship is 64px
    playerX += playerX_change
    
    if playerX <= 0:
        playerX = 0
    elif playerX >=736: 
        playerX = 736

    #Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            # this moves all enemies off the screen.
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i] 
        elif enemyX[i] >=736: 
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]    

        # Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound('Music/explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i],enemyY[i],i)

    #Bullet movement
    # if bullet goes off screen reset to 480 and change state to ready so we can fire again.
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()
