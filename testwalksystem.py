import pygame
import random
pygame.init()

#ชื่อเกม
pygame.display.set_caption("ProjectbeginTest")
#LOGO Game
icon = pygame.image.load("testlearn/logo.png")
pygame.display.set_icon(icon)
#Set ขนาดหน้าจอ
SCREEN_W = 640
SCREEN_H = 480
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
# #Set พื้นหลัง
# bg = pygame.image.load("testlearn/mapbg.png")
# #player setting (Object)
# player = pygame.image.load("testlearn/char.png")
# player = pygame.transform.scale(player, (50, 50))
# #ค่าพื้นฐาน Player
# player_rect = player.get_rect()
# player_rect.centerx = SCREEN_W // 2
# player_rect.centery = SCREEN_H // 2

#BOSS
#boss = pygame.image.load("testlearn/boss.png")
#boss = pygame.transform.scale(boss, (225, 225))
#ค่าพื้นฐานBoss
#boss_rect = boss.get_rect()
#boss_rect.centerx = SCREEN_W // 2
#boss_rect.centery = 100

#Direction
right1 = pygame.image.load("char/moveright1.png")
right1 = pygame.transform.scale(right1, (100, 100))
right2 = pygame.image.load("char/moveright2.png")
right2 = pygame.transform.scale(right2, (100, 100))
right3 = pygame.image.load("char/moveright3.png")
right3 = pygame.transform.scale(right3, (100, 100))
right4 = pygame.image.load("char/moveright4.png")
right4 = pygame.transform.scale(right4, (100, 100))
right5 = pygame.image.load("char/moveright5.png")
right5 = pygame.transform.scale(right5, (100, 100))

sprites_right = [right1, right2, right3, right4, right5]

left1 = pygame.image.load("char/moveleft1.png")
left1 = pygame.transform.scale(left1, (100, 100))
left2 = pygame.image.load("char/moveleft2.png")
left2 = pygame.transform.scale(left2, (100, 100))
left3 = pygame.image.load("char/moveleft3.png")
left3 = pygame.transform.scale(left3, (100, 100))
left4 = pygame.image.load("char/moveleft4.png")
left4 = pygame.transform.scale(left4, (100, 100))
left5 = pygame.image.load("char/moveleft5.png")
left5 = pygame.transform.scale(left5, (100, 100))

sprites_left = [left1, left2, left3, left4, left5]

current_direction  = "right"
current_sprites = sprites_right

background_image = pygame.image.load("testlearn/mapbg.png")
background_rec = background_image.get_rect(center = (SCREEN_W//2,SCREEN_H//2))

sprites_rect = sprites_right[0].get_rect()

sprites_rect.x = 250
sprites_rect.y = 250

speed = 3

frame_rate = 10

background_x = 0
background_y = 0

current_frame = 0

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
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
            
    screen.fill((0,0,0))
        
    if current_frame >= len(current_sprites):
        current_frame = 0
    if current_frame == 4:
        current_frame = 0
            
    screen.blit(background_image, (background_x, background_y))
    screen.blit(current_sprites[int(current_frame)], sprites_rect)
        
    pygame.display.flip()
    clock.tick(60)