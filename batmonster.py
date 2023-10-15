import pygame, sys
import random
pygame.init()
clock = pygame.time.Clock()
SCREEN_W = 800
SCREEN_H = 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))


#loadbat
batredr1 = pygame.image.load("mons/red1.png")
batredr1 = pygame.transform.scale(batredr1, (50, 50))
batredr2 = pygame.image.load("mons/red2.png")
batredr2 = pygame.transform.scale(batredr2, (50, 50))
batredr3 = pygame.image.load("mons/red3.png")
batredr3 = pygame.transform.scale(batredr3, (50, 50))
batredr4 = pygame.image.load("mons/red4.png")
batredr4 = pygame.transform.scale(batredr4, (50, 50))

sprite_batredr = [batredr1, batredr2, batredr3, batredr4]

batredl1 = pygame.transform.flip(batredr1, True, False)
batredl2 = pygame.transform.flip(batredr2, True, False)
batredl3 = pygame.transform.flip(batredr3, True, False)
batredl4 = pygame.transform.flip(batredr4, True, False)

sprites_batredl = [batredl1, batredl2, batredl3, batredl4]

#Setting Direction
current_batred = sprite_batredr

#monster animation setup
current_frame_batred = 0

#setup possition player
sprites_rect_red = sprite_batredr[0].get_rect()
sprites_rect_red.x = random.randint(0, 700)
sprites_rect_red.y = random.randint(0, 500)

batredx_speed = 5
batredy_speed = 4

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((30, 30, 30))
    
    current_frame_batred += 0.2
    
    sprites_rect_red.x += batredx_speed
    sprites_rect_red.y += batredy_speed
    
    
    if sprites_rect_red.right >= SCREEN_W  or sprites_rect_red.left <= 0:
        batredx_speed *= -1
    if sprites_rect_red.bottom >= SCREEN_H or sprites_rect_red.top <= 0:
        batredy_speed *= -1
    
    if batredx_speed > 0 and batredy_speed > 0:
        current_batred = sprite_batredr
    if batredx_speed < 0 and batredy_speed > 0:
        current_batred = sprites_batredl
    if batredx_speed > 0 and batredy_speed < 0:
        current_batred = sprite_batredr
    if batredx_speed < 0 and batredy_speed < 0:
        current_batred = sprites_batredl
    #Control Loop Sprite and Boss
    if current_frame_batred >= len(current_batred):
        current_frame_batred = 0
    
    screen.blit(current_batred[int(current_frame_batred)], sprites_rect_red)
    
    pygame.display.flip()
    clock.tick(60)