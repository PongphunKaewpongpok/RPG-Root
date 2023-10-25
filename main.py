###mport Libraries
import pygame, sys, math, json, random

###Game Starting
pygame.init()
SCREEN_WEIGHT = 1380
SCREEN_HEIGHT = 720
game_screen = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))
pygame.display.set_caption("RPG ตี Root")
clock = pygame.time.Clock()
playing = True
first_time = True
spawn_tile_time = 0

###Wand
wand_image = pygame.image.load('Texture/Wand/original_form.png').convert_alpha()

###Player Data
#Creating idle_animate
num0121 = [0, 1, 2, 1]
idle_animate = []
for i in num0121:
    player_idle = pygame.image.load(f'Texture/Player/idle_{i}.png').convert_alpha()
    idle_animate.append(player_idle)
player_frame = 0

###Map Assets
map_bg = pygame.image.load('Texture/Map/City_1.png').convert_alpha()
map_bg = pygame.transform.scale(map_bg, (1280,720))

#Hydra Asset
hydra_animation = pygame.image.load('Texture/Entitys/Hydra/3_heads_form_3.png').convert_alpha()
hydra_hitbox = pygame.Rect(100, 100, 50, 50)

###Load Datas
with open("Data/game_data.txt") as game_data:
    UPGRADE_DATA_DICT = json.loads(game_data.read())

###Tiles Inventory
inventory_list = []

###Ground Tile Asset
tile_image_list = []
tile_name_list_tem1 = list(range(0, 10))
tile_name_list_tem2 = ["plus", "minus", "times", "obelus", "equal", "power"]
for i in tile_name_list_tem1:
    tile_image = pygame.image.load(f'Texture/Tiles/Ground/Numbers/{i}.png').convert_alpha()
    tile_image_list.append(tile_image)
for i in tile_name_list_tem2:
    tile_image = pygame.image.load(f'Texture/Tiles/Ground/Operators/{i}.png').convert_alpha()
    tile_image_list.append(tile_image)
tile_image = pygame.image.load('Texture/Tiles/Ground/flame_tile.png').convert_alpha()
tile_image_list.append(tile_image)
###For random choice in future
tile_name_list = list(range(0, 10))
tile_name_list.extend(tile_name_list_tem2)
tile_name_list.append("flame_tile")

###Shoot Tile Asset
shoot_tile_image_list = []
for i in tile_name_list_tem1:
    tile_image = pygame.image.load(f'Texture/Tiles/Shooting/Numbers/{i}.png').convert_alpha()
    shoot_tile_image_list.append(tile_image)
for i in tile_name_list_tem2:
    tile_image = pygame.image.load(f'Texture/Tiles/Shooting/Operators/{i}.png').convert_alpha()
    shoot_tile_image_list.append(tile_image)

###Shoot Flame Tile Asset
shoot_flame_tile_image_list = []
for i in tile_name_list_tem1:
    tile_image = pygame.image.load(f'Texture/Tiles/Flame/Numbers/{i}.png').convert_alpha()
    shoot_flame_tile_image_list.append(tile_image)
for i in tile_name_list_tem2:
    tile_image = pygame.image.load(f'Texture/Tiles/Flame/Operators/{i}.png').convert_alpha()
    shoot_flame_tile_image_list.append(tile_image)

#Fire Chamber Asset
fire_chamber_animate = []
FIRE_CHAM_POS = []
FIRE_CHAM_TIME = []
for i in num0121:
    tem_fire_chamber_image = pygame.image.load(f'Texture/Others/Fire/{i}.png').convert_alpha()
    tem_fire_chamber_image = pygame.transform.scale(tem_fire_chamber_image, (60,80))
    fire_chamber_animate.append(tem_fire_chamber_image)
fire_chamber_frame = 0

###Enemy
#Enemy Lists
ENEMY_TYPE = []
ENEMY_POS = []
ENEMY_EQUATION = []
small_root_animation = []
#Enemy Asset
for i in range(0, 6):
    smallroot_animate = pygame.image.load(f'Texture/Entitys/Small_Root/{i}.png').convert_alpha()
    small_root_animation.append(smallroot_animate)
smallroot_frame = 0
enemy_spawn_time = 60

###Tiles On Ground
TILE_TYPE = []
TILE_POS = []
TILE_COUNT = 0
LIMIT_TILE_GROUND = 20

###Shooting Tile
#Tile Lists
SHOOT_TILE_TYPE = []
SHOOT_TILE_POS = []
SHOOT_TILE_FIRE = []
#Shooting tile velocity
SHOOT_TILE_VEL = []
#Shooting Delay Time
SHOOT_DELAY_TIME = 0

###Select Tile
#0 = No Tile
SELECT_TILE = 0

#Health Asset
red_heart = pygame.image.load('Texture/Others/Heart/Red_Heart.png').convert_alpha()
black_heart = pygame.image.load('Texture/Others/Heart/Black_Heart.png').convert_alpha()
HEALTH_LEFT = []
for _ in range(UPGRADE_DATA_DICT["Max Health"]):
    HEALTH_LEFT.append(red_heart)
hit_delay_time = 0

#Inventory Background Asset
inventory_bg_image = pygame.image.load('Texture/Others/Inventory_BG.png').convert_alpha()

#Select Tile Asset
select_tile_image_list = []
for i in range(0, 2):
    TEM_IMAGE = pygame.image.load(f'Texture/Tiles/Select/{i}.png').convert_alpha()
    select_tile_image_list.append(TEM_IMAGE)
select_inven_frame = 0



#Function Code Zone#

def enemy_movement():
    #Enemy Movement
    for i in range(0, len(ENEMY_TYPE)):
        if ENEMY_TYPE[i] == "smallroot" and int(smallroot_frame) < 4:
            TEM_X_DIST = player_hitbox.x - ENEMY_POS[i].x
            TEM_Y_DIST = -(player_hitbox.y - ENEMY_POS[i].y)
            TEM_RADIAN = math.atan2(TEM_Y_DIST, TEM_X_DIST)
            ENEMY_POS[i].x += math.cos(TEM_RADIAN)
            ENEMY_POS[i].y += -(math.sin(TEM_RADIAN))

def display_enemy():
    global hit_delay_time
    for i in range(0, len(ENEMY_TYPE)):
        TEM_HITBOX = ENEMY_POS[i]
        if ENEMY_TYPE[i] == "smallroot":
            TEM_ENEMY_IMAGE = smallroot_sprite
        if TEM_HITBOX.colliderect(player_hitbox) and hit_delay_time == 0:
            hit_delay_time = 60
            for j in range(len(HEALTH_LEFT)-1, -1, -1):
                if HEALTH_LEFT[j] == red_heart:
                    HEALTH_LEFT[j] = black_heart
                    break
        game_screen.blit(TEM_ENEMY_IMAGE, ENEMY_POS[i])

def creating_enemy(types, count):
    for _ in range(count):
        ENEMY_TYPE.append(types)
        ENEMY_EQUATION.append("")
        if types == "smallroot":
            TEM_HITBOX = smallroot_sprite.get_rect()
        TEM_HITBOX.x = random.randint(100, SCREEN_WEIGHT-200)
        TEM_HITBOX.y = random.randint(100, SCREEN_WEIGHT-200)
        ENEMY_POS.append(TEM_HITBOX)

def display_select_inven_tile():
    #Display Selecting Inventory Tiles
    game_screen.blit(select_tile_image_list[int(select_inven_frame)], (1305, 60*(SELECT_TILE-1)))

def display_inventory_tiles():
    #Display Inventory Tiles
    for i in range(0, len(inventory_list)):
        TEM_VAR = inventory_list[i]
        if isinstance(TEM_VAR, int):
            TEM_INVEN_TILE = shoot_tile_image_list[TEM_VAR]
        elif TEM_VAR == "plus":
            TEM_INVEN_TILE = shoot_tile_image_list[10]
        elif TEM_VAR == "minus":
            TEM_INVEN_TILE = shoot_tile_image_list[11]
        elif TEM_VAR == "times":
            TEM_INVEN_TILE = shoot_tile_image_list[12]
        elif TEM_VAR == "obelus":
            TEM_INVEN_TILE = shoot_tile_image_list[13]
        elif TEM_VAR == "equal":
            TEM_INVEN_TILE = shoot_tile_image_list[14]
        elif TEM_VAR == "power":
            TEM_INVEN_TILE = shoot_tile_image_list[15]
        game_screen.blit(TEM_INVEN_TILE, (1305, 60*i))

def display_health():
    #Display Health Bar
    for i in range(0, len(HEALTH_LEFT)):
        game_screen.blit(HEALTH_LEFT[i], (10+(50*i), 10))

def fire_chamber_time(start_from=0):
    for i in range(start_from, len(FIRE_CHAM_TIME)):
        if FIRE_CHAM_TIME[i] == 0:
            FIRE_CHAM_TIME.pop(i)
            FIRE_CHAM_POS.pop(i)
            fire_chamber_time(i)
            break
        else:
            FIRE_CHAM_TIME[i] -= 1

def make_flame_tile(num):
    TEM_GET_RECT = SHOOT_TILE_POS[num]
    for i in range(0, len(FIRE_CHAM_TIME)):
        if TEM_GET_RECT.colliderect(FIRE_CHAM_POS[i]):
            SHOOT_TILE_FIRE[num] = True

def summon_fire(num):
    #Spawning A Fire Chamber
    FIRE_CHAM_TIME.append(600)
    TEM_POS = fire_chamber_sprite.get_rect()
    TEM_POS.x = TILE_POS[num].x
    TEM_POS.y = TILE_POS[num].y
    FIRE_CHAM_POS.append(TEM_POS)

def display_fire():
    #Display A Fire Chamber
    for i in range(0, len(FIRE_CHAM_TIME)):
        game_screen.blit(fire_chamber_sprite, FIRE_CHAM_POS[i])

def display_shoot_tile(num):
    #Display A Display Shooting Tile
    TEM_VAR = SHOOT_TILE_TYPE[num]
    TEM_TILE_HITBOX = SHOOT_TILE_POS[num]
    if isinstance(TEM_VAR, int):
        TEM_TILE_IMAGE = shoot_tile_image_list[TEM_VAR]
    elif TEM_VAR == "plus":
        TEM_TILE_IMAGE = shoot_tile_image_list[10]
    elif TEM_VAR == "minus":
        TEM_TILE_IMAGE = shoot_tile_image_list[11]
    elif TEM_VAR == "times":
        TEM_TILE_IMAGE = shoot_tile_image_list[12]
    elif TEM_VAR == "obelus":
        TEM_TILE_IMAGE = shoot_tile_image_list[13]
    elif TEM_VAR == "equal":
        TEM_TILE_IMAGE = shoot_tile_image_list[14]
    elif TEM_VAR == "power":
        TEM_TILE_IMAGE = shoot_tile_image_list[15]
    game_screen.blit(TEM_TILE_IMAGE, SHOOT_TILE_POS[num])

def display_shoot_flame_tile(num):
    #Display A Display Shooting Flame Tile
    TEM_VAR = SHOOT_TILE_TYPE[num]
    TEM_TILE_HITBOX = SHOOT_TILE_POS[num]
    if isinstance(TEM_VAR, int):
        TEM_TILE_IMAGE = shoot_flame_tile_image_list[TEM_VAR]
    elif TEM_VAR == "plus":
        TEM_TILE_IMAGE = shoot_flame_tile_image_list[10]
    elif TEM_VAR == "minus":
        TEM_TILE_IMAGE = shoot_flame_tile_image_list[11]
    elif TEM_VAR == "times":
        TEM_TILE_IMAGE = shoot_flame_tile_image_list[12]
    elif TEM_VAR == "obelus":
        TEM_TILE_IMAGE = shoot_flame_tile_image_list[13]
    elif TEM_VAR == "equal":
        TEM_TILE_IMAGE = shoot_flame_tile_image_list[14]
    elif TEM_VAR == "power":
        TEM_TILE_IMAGE = shoot_flame_tile_image_list[15]
    game_screen.blit(TEM_TILE_IMAGE, SHOOT_TILE_POS[num])

def moving_shoot_tile():
    for i in range(0, len(SHOOT_TILE_TYPE)):
        SHOOT_TILE_POS[i].x += SHOOT_TILE_VEL[i][0]
        SHOOT_TILE_POS[i].y += SHOOT_TILE_VEL[i][1]

def shoot_tile():
    #Detect Shooting Tile
    global SELECT_TILE, SHOOT_DELAY_TIME
    if keys[pygame.K_e] and SELECT_TILE > 0 and SHOOT_DELAY_TIME == 0 and len(inventory_list) > 0:
        SHOOT_DELAY_TIME = 15
        types = inventory_list[SELECT_TILE-1]
        inventory_list.pop(SELECT_TILE-1)
        if SELECT_TILE > 1 and SELECT_TILE > len(inventory_list)-1:
            SELECT_TILE -= 1
        elif SELECT_TILE == 1:
            SELECT_TILE = 1
        if isinstance(types, int):
            TEM_TILE_IMAGE = shoot_tile_image_list[types]
        elif types == "plus":
            TEM_TILE_IMAGE = shoot_tile_image_list[10]
        elif types == "minus":
            TEM_TILE_IMAGE = shoot_tile_image_list[11]
        elif types == "times":
            TEM_TILE_IMAGE = shoot_tile_image_list[12]
        elif types == "obelus":
            TEM_TILE_IMAGE = shoot_tile_image_list[13]
        elif types == "equal":
            TEM_TILE_IMAGE = shoot_tile_image_list[14]
        elif types == "power":
            TEM_TILE_IMAGE = shoot_tile_image_list[15]
        SHOOT_TILE_TYPE.append(types)
        TEM_POS = TEM_TILE_IMAGE.get_rect()
        TEM_POS.x = player_hitbox.x
        TEM_POS.y = player_hitbox.y
        SHOOT_TILE_POS.append(TEM_POS)
        SHOOT_TILE_FIRE.append(False)
        TEM_MOVE_TUPLE = (math.cos(wand_radian)*10, -(math.sin(wand_radian)*10))
        SHOOT_TILE_VEL.append(TEM_MOVE_TUPLE)

def spawn_tiles():
    global TILE_COUNT
    TEM_RANDOM_NUM = random.choice(tile_name_list)
    TILE_TYPE.append(TEM_RANDOM_NUM)
    if isinstance(TEM_RANDOM_NUM, int):
        TEM_GET_RECT = tile_image_list[TEM_RANDOM_NUM].get_rect()
    elif TEM_RANDOM_NUM == "plus":
        TEM_GET_RECT = tile_image_list[10].get_rect()
    elif TEM_RANDOM_NUM == "minus":
        TEM_GET_RECT = tile_image_list[11].get_rect()
    elif TEM_RANDOM_NUM == "times":
        TEM_GET_RECT = tile_image_list[12].get_rect()
    elif TEM_RANDOM_NUM == "obelus":
        TEM_GET_RECT = tile_image_list[13].get_rect()
    elif TEM_RANDOM_NUM == "equal":
        TEM_GET_RECT = tile_image_list[14].get_rect()
    elif TEM_RANDOM_NUM == "power":
        TEM_GET_RECT = tile_image_list[15].get_rect()
    elif TEM_RANDOM_NUM == "flame_tile":
        TEM_GET_RECT = tile_image_list[16].get_rect()
    TEM_GET_RECT.x = random.randint(100, SCREEN_WEIGHT-200)
    TEM_GET_RECT.y = random.randint(100, SCREEN_HEIGHT-100)
    TILE_POS.append(TEM_GET_RECT)
    TILE_COUNT += 1
        
def display_tiles_ground(start_from=0):
    #Blit and Detect Touching
    global TILE_COUNT, SELECT_TILE
    for i in range(start_from, len(TILE_TYPE)):
        TEM_VAR = TILE_TYPE[i]
        TEM_TILE_HITBOX = TILE_POS[i]
        if isinstance(TEM_VAR, int):
            TEM_TILE_IMAGE = tile_image_list[TEM_VAR]
        elif TEM_VAR == "plus":
            TEM_TILE_IMAGE = tile_image_list[10]
        elif TEM_VAR == "minus":
            TEM_TILE_IMAGE = tile_image_list[11]
        elif TEM_VAR == "times":
            TEM_TILE_IMAGE = tile_image_list[12]
        elif TEM_VAR == "obelus":
            TEM_TILE_IMAGE = tile_image_list[13]
        elif TEM_VAR == "equal":
            TEM_TILE_IMAGE = tile_image_list[14]
        elif TEM_VAR == "power":
            TEM_TILE_IMAGE = tile_image_list[15]
        elif TEM_VAR == "flame_tile":
            TEM_TILE_IMAGE = tile_image_list[16]
        game_screen.blit(TEM_TILE_IMAGE, TILE_POS[i])
        if TEM_TILE_HITBOX.colliderect(player_hitbox) and len(inventory_list) < UPGRADE_DATA_DICT["Inventory Slot"]:
            if TEM_VAR != "flame_tile":
                inventory_list.append(TEM_VAR)
                TILE_TYPE.pop(i)
                TILE_POS.pop(i)
                TILE_COUNT -= 1
                print(inventory_list)
                display_tiles_ground(i)
                break
            else:
                summon_fire(i)
                TILE_TYPE.pop(i)
                TILE_POS.pop(i)
                TILE_COUNT -= 1
                display_tiles_ground(i)
                break

def wand_pos():
    global wand_x, wand_y
    wand_x = player_hitbox.center[0]
    wand_y = player_hitbox.center[1]

def move_speed_set():
    #Move Speed Set
    global MOVEMENT_SPEED
    if keys[pygame.K_w] or keys[pygame.K_s]:
        if keys[pygame.K_a] or keys[pygame.K_d]:
            MOVEMENT_SPEED = (50**0.5)/2
        else:
            MOVEMENT_SPEED = 5
    else:
        MOVEMENT_SPEED = 5

def mouse_detect_func():
    #Mouse Position
    global mouse_pos
    mouse_pos = pygame.mouse.get_pos()

def player_frame_animate():
    #Player Animation Frame
    global player_frame
    if player_frame >= 3.9:
        player_frame = 0
    else:
        player_frame += 0.1

def fire_cham_frame_animate():
    #Player Animation Frame
    global fire_chamber_frame
    if fire_chamber_frame >= 3.9:
        fire_chamber_frame = 0
    else:
        fire_chamber_frame += 0.1

def smallroot_frame_animate():
    #Smail Root Animation Frame
    global smallroot_frame
    if smallroot_frame >= 5.9:
        smallroot_frame = 0
    else:
        smallroot_frame += 0.1

def select_inven_animate():
    global select_inven_frame
    if select_inven_frame >= 1.9:
        select_inven_frame = 0
    else:
        select_inven_frame += 0.1

def shoot_delay_func():
    global SHOOT_DELAY_TIME
    if SHOOT_DELAY_TIME > 0:
        SHOOT_DELAY_TIME -= 1


#Game Running Zone#

while playing:
    global keys
    keys = pygame.key.get_pressed()
    clock.tick(60)
    for event in pygame.event.get():
        ###Exit Game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        ###Detect Mouse Wheel Event
        #----------------------------------------------------------------#
        #   Button 4 = MOUSESCROLLUP        Button 5 = MOUSESCROLLDOWN   #
        #----------------------------------------------------------------#
        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(inventory_list) > 1:
                if event.button == 5:
                    if SELECT_TILE < len(inventory_list):
                        SELECT_TILE += 1
                    else:
                        SELECT_TILE = 1
                elif event.button == 4:
                    if SELECT_TILE > 1:
                        SELECT_TILE -= 1
                    else:
                        SELECT_TILE = len(inventory_list)
    if len(inventory_list) in [0, 1]:
        SELECT_TILE = len(inventory_list)
    #Player Movement
    move_speed_set()
    if keys[pygame.K_w]:
        player_hitbox.y -= MOVEMENT_SPEED
    if keys[pygame.K_s]:
        player_hitbox.y += MOVEMENT_SPEED
    if keys[pygame.K_a]:
        player_hitbox.x -= MOVEMENT_SPEED
    if keys[pygame.K_d]:
        player_hitbox.x += MOVEMENT_SPEED

    #Enemy Movement
    enemy_movement()

    #Shooting Delay Time
    shoot_delay_func()

    #Moving Shooting Tile
    moving_shoot_tile()

    #Hit Delay
    if hit_delay_time > 0:
        hit_delay_time -= 1
    print(hit_delay_time)

    #Mouse Detection
    mouse_detect_func()

    #Map
    game_screen.blit(map_bg, (0, 0))

    #Player Animation
    player_frame_animate()
    player_sprite = idle_animate[int(player_frame)]

    #Fire Chamber Animation
    global fire_chamber_sprite
    fire_cham_frame_animate()
    fire_chamber_sprite = fire_chamber_animate[int(fire_chamber_frame)]

    #Select Inventory Animation
    select_inven_animate()

    #Position Detect First Time
    if first_time:
        first_time = False
        player_hitbox = player_sprite.get_rect()

    #Hydra
    pygame.draw.rect(game_screen, (255,0,0), hydra_hitbox, 4)
    game_screen.blit(hydra_animation, (100, 100))

    #Wand Position
    wand_pos()

    #Wand Rotation
    wand_x_dist = mouse_pos[0] - wand_x
    wand_y_dist = -(mouse_pos[1] - wand_y)
    wand_radian = math.atan2(wand_y_dist, wand_x_dist)
    wand_angle = math.degrees(wand_radian)
    wand_display = pygame.transform.rotate(wand_image, wand_angle - 90)
    wand_hitbox = wand_display.get_rect(center = (wand_x, wand_y))

    #Wand Blit
    game_screen.blit(wand_display, wand_hitbox)

    #Spawning Tiles Around The Map
    if spawn_tile_time == 0 and TILE_COUNT < LIMIT_TILE_GROUND:
        spawn_tiles()
        spawn_tile_time = 60
    elif TILE_COUNT != LIMIT_TILE_GROUND:
        spawn_tile_time -= 1

    #Tiles On Ground Blit and Detect Touching
    display_tiles_ground()

    #Small Root Animation
    smallroot_frame_animate()
    smallroot_sprite = small_root_animation[int(smallroot_frame)]

    #Summon Enemy Smallroot
    if enemy_spawn_time == 0:
        creating_enemy("smallroot", 1)
        enemy_spawn_time = 300
    else:
        enemy_spawn_time -= 1

    #Display Enemy
    display_enemy()

    #Shooting Tile
    shoot_tile()

    #Fire Chamber Time
    fire_chamber_time()

    #Fire Chamber Blit
    display_fire()

    #Shooting Tile Blit
    for i in range(0, len(SHOOT_TILE_TYPE)):
        if SHOOT_TILE_FIRE[i]:
            display_shoot_flame_tile(i)
        else:
            make_flame_tile(i)
            display_shoot_tile(i)

    #Player Sprite Blit
    game_screen.blit(player_sprite, player_hitbox)

    #Health Bar Blit
    display_health()

    #Inventory Background Blit
    game_screen.blit(inventory_bg_image, (1280, 0))

    #Inventory Tiles Blit
    display_inventory_tiles()

    #Select Inventory Blit 
    display_select_inven_tile()

    #Health Left Check
    if not red_heart in HEALTH_LEFT:
        print("DEAD")

    pygame.time.delay(30)
    pygame.display.update()
