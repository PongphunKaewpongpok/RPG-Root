import pygame
import random
pygame.init()

#ชื่อเกม
pygame.display.set_caption("ProjectbeginTest")
#LOGO Game
icon = pygame.image.load("testlearn/logo.png")
pygame.display.set_icon(icon)
#Set ขนาดหน้าจอ
SCREEN_W = 800
SCREEN_H = 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

#Colour Setting
RED = (255, 0, 0)
GREEN = (0, 255, 0)
#Damage Object
damage = pygame.image.load("testlearn/metreo.png")
damage = pygame.transform.scale(damage, (100, 100))
#ค่าพื้นฐาน Object Damage
damage_rect = damage.get_rect()
damage_rect.x = random.randint(0, SCREEN_W - 32)
damage_rect.y = 0
#Damage Object2
damage2 = pygame.image.load("testlearn/metreo.png")
damage2 = pygame.transform.scale(damage2, (100, 100))
#ค่าพื้นฐาน Object damage2
damage2_rect = damage2.get_rect()
damage2_rect.x = random.randint(0, SCREEN_W - 32)
damage2_rect.y = 0

#BOSS
#Up load Boss image
phase1_1 = pygame.image.load("boss/form1.png")
phase1_1 = pygame.transform.scale(phase1_1, (250, 250))
phase1_2 = pygame.image.load("boss/form2.png")
phase1_2 = pygame.transform.scale(phase1_2, (250, 250))
phase1_3 = pygame.image.load("boss/form3.png")
phase1_3 = pygame.transform.scale(phase1_3, (250, 250))
phase2_1 = pygame.image.load("boss/2form1.png")
phase2_1 = pygame.transform.scale(phase2_1, (250, 250))
phase2_2 = pygame.image.load("boss/2form2.png")
phase2_2 = pygame.transform.scale(phase2_2, (250, 250))
phase2_3 = pygame.image.load("boss/2form3.png")
phase2_3 = pygame.transform.scale(phase2_3, (250, 250))
phase3_1 = pygame.image.load("boss/1form1.png")
phase3_1 = pygame.transform.scale(phase3_1, (250, 250))
phase3_2 = pygame.image.load("boss/1form2.png")
phase3_2 = pygame.transform.scale(phase3_2, (250, 250))
phase3_3 = pygame.image.load("boss/1form3.png")
phase3_3 = pygame.transform.scale(phase3_3, (250, 250))
#Phase ของ Boss
boss_phase1 = [phase1_1, phase1_2, phase1_3]
boss_phase2 = [phase2_1, phase2_2, phase2_3]
boss_phase3 = [phase3_1, phase3_2, phase3_3]

#Direction
right1 = pygame.image.load("4d/r1.png")
right1 = pygame.transform.scale(right1, (100, 100))
right2 = pygame.image.load("4d/r2.png")
right2 = pygame.transform.scale(right2, (100, 100))
right3 = pygame.image.load("4d/r3.png")
right3 = pygame.transform.scale(right3, (100, 100))
right4 = pygame.image.load("4d/r4.png")
right4 = pygame.transform.scale(right4, (100, 100))
right5 = pygame.image.load("4d/r5.png")
right5 = pygame.transform.scale(right5, (100, 100))
right6 = pygame.image.load("4d/r6.png")
right6 = pygame.transform.scale(right1, (100, 100))

sprites_right = [right1, right2, right3, right4, right5, right6]

left1 = pygame.transform.flip(right1, True, False)
left2 = pygame.transform.flip(right2, True, False)
left3 = pygame.transform.flip(right3, True, False)
left4 = pygame.transform.flip(right4, True, False)
left5 = pygame.transform.flip(right5, True, False)
left6 = pygame.transform.flip(right6, True, False)

sprites_left = [left1, left2, left3, left4, left5, left6]

up1 = pygame.image.load("4d/u1.png")
up1 = pygame.transform.scale(up1, (100, 100))
up2 = pygame.image.load("4d/u2.png")
up2 = pygame.transform.scale(up2, (100, 100))
up3 = pygame.image.load("4d/u3.png")
up3 = pygame.transform.scale(up3, (100, 100))
up4 = pygame.image.load("4d/u4.png")
up4 = pygame.transform.scale(up4, (100, 100))
up5 = pygame.image.load("4d/u5.png")
up5 = pygame.transform.scale(up5, (100, 100))
up6 = pygame.image.load("4d/u6.png")
up6 = pygame.transform.scale(up6, (100, 100))

sprites_up = [up1, up2, up3, up4, up5, up6]

down1 = pygame.image.load("4d/d1.png")
down1 = pygame.transform.scale(down1, (100, 100))
down2 = pygame.image.load("4d/d2.png")
down2 = pygame.transform.scale(down2, (100, 100))
down3 = pygame.image.load("4d/d3.png")
down3 = pygame.transform.scale(down3, (100, 100))
down4 = pygame.image.load("4d/d4.png")
down4 = pygame.transform.scale(down4, (100, 100))
down5 = pygame.image.load("4d/d5.png")
down5 = pygame.transform.scale(down5, (100, 100))
down6 = pygame.image.load("4d/d6.png")
down6 = pygame.transform.scale(down6, (100, 100))

sprites_down = [down1, down2, down3, down4, down5, down6]

#Setting Direction
current_direction  = "right"
current_sprites = sprites_right

background_image = pygame.image.load("testlearn/map.png")
background_rec = background_image.get_rect(center = (SCREEN_W//2,SCREEN_H//2))

sprites_rect = sprites_right[0].get_rect()

#Boss set up
current_boss = boss_phase1

boss1_rect = boss_phase1[0].get_rect()
boss1_rect.x = 275
boss1_rect.y = 10
#Player Hp
playerHp = 200
current_playerHP = 200
#Boss Hp
bossHP = 300
current_bossHp = 300

sprites_rect.x = 250
sprites_rect.y = 250

FALL1 = random.randint(7, 12)
FALL2 = random.randint(7, 12)
speed = 3

frame_rate = 10

background_x = 0
background_y = 0

current_frameboss = 0

current_frame = 0

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
    current_frameboss += 0.1
    if current_bossHp > 200:
        current_boss = boss_phase1
    if  100 < current_bossHp < 200:
        current_boss = boss_phase2
    if current_bossHp < 100:
        current_boss = boss_phase3
    
    #attack damage
    if keys[pygame.K_SPACE]:
        current_bossHp -= 1
    if keys[pygame.K_RIGHT]:
        current_direction = "right"
        current_sprites = sprites_right
        current_frame += 0.2
        sprites_rect.x += speed
    if keys[pygame.K_LEFT]:
        current_direction = "left"
        current_sprites = sprites_left
        current_frame += 0.2
        sprites_rect.x -= speed
    if keys[pygame.K_UP]:
        current_direction = "up"
        current_sprites = sprites_up
        current_frame += 0.2
        sprites_rect.y -= speed
    if keys[pygame.K_DOWN]:
        current_direction = "down"
        current_sprites = sprites_down
        current_frame += 0.2
        sprites_rect.y += speed
            
    screen.fill((0,0,0))
        
    if current_frame >= len(current_sprites):
        current_frame = 0
    if current_frame == 6:
        current_frame = 0

    if current_frameboss >= len(boss_phase1):
        current_frameboss = 0
    if current_frameboss == 4:
        current_frameboss = 0
        
    #Ball Object
    if damage_rect.y < SCREEN_H:
        damage_rect.y += FALL1
    else:
        damage_rect.x = random.randint(0, SCREEN_W-32)
        damage_rect.y = 0
    #Ball Object2
    if damage2_rect.y < SCREEN_H:
        damage2_rect.y += FALL2
    else:
        damage2_rect.x = random.randint(0, SCREEN_W-32)
        damage2_rect.y = 0
    
    #healthbarSystem
    #BosshealthBar
    pygame.draw.rect(background_image, RED, (250, 20, bossHP, 15))
    pygame.draw.rect(background_image, GREEN, (250, 20, current_bossHp, 15))
    
    #playerHealthbar
    pygame.draw.rect(background_image, RED, (300, 580, playerHp, 15))
    pygame.draw.rect(background_image, GREEN, (300, 580, current_playerHP, 15))
            
    screen.blit(background_image, (background_x, background_y))
    screen.blit(current_sprites[int(current_frame)], sprites_rect)
    screen.blit(current_boss[int(current_frameboss)], boss1_rect)
    screen.blit(damage, damage_rect)
    screen.blit(damage2, damage2_rect)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
