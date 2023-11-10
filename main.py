###mport Libraries
import pygame, sys, math, json, random

###Load Datas
with open("Data/game_data.txt") as game_data:
    UPGRADE_DATA_DICT = json.loads(game_data.read())

with open("Data/game_settings.txt") as game_settings:
    GAME_SETTINGS_DICT = json.loads(game_settings.read())



###Game Starting
playing = "main_menu"
pygame.init()
pygame.mixer.init()
SCREEN_WEIGHT = 1380
SCREEN_HEIGHT = 720
game_screen = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))
pygame.display.set_icon(pygame.image.load("game_icon.png"))
pygame.display.set_caption("RPG ตี Root")
clock = pygame.time.Clock()
first_time = True
spawn_tile_time = 0
GAME_STAGE = 1
GAME_ENEMY_COUNT = 0
RAINDROPS_COOLDOWN = 0
GAME_EVENT_LEFT = [1, "trading_event"]
TALKING_FRAME = 0
ULTIMATE_CHEAT_MODE = "OFF"
CHEAT_ACTIVATE_DELAY = 0

#Font
silkscreen_font = pygame.font.Font("Texture/Fonts/Silkscreen/slkscr.ttf", 30)
silkscreen_font_ingame = pygame.font.Font("Texture/Fonts/Silkscreen/slkscr.ttf", 12)
#Set Text
DISPLAY_DEBUG_TEXT = silkscreen_font.render("DEBUG MODE: ON", True, (114, 255, 131))

#Rain Weather
BLACK_RAINY_DAY_ALPHA = 0
black_background = pygame.Surface((SCREEN_WEIGHT, SCREEN_HEIGHT), pygame.SRCALPHA)
raindrops = pygame.Surface((SCREEN_WEIGHT, SCREEN_HEIGHT), pygame.SRCALPHA)
raindrops_pos_list = []
raindrops = pygame.transform.rotate(raindrops, 90)

###Wand
wand_image = pygame.image.load('Texture/Wand/original_form.png').convert_alpha()

###Player Data
#Creating idle_animate
num0121 = [0, 1, 2, 1]
left_idle_animate = []
right_idle_animate = []
left_walk_animate = []
right_walk_animate = []
left_death_animate = []
right_death_animate = []
for i in num0121:
    left_player_idle = pygame.image.load(f'Texture/Player/idle_{i}.png').convert_alpha()
    right_player_idle = pygame.transform.flip(left_player_idle, True, False)
    left_idle_animate.append(left_player_idle)
    right_idle_animate.append(right_player_idle)
for _ in range(2):
    for i in range(0, 2):
        left_player_walk = pygame.image.load(f'Texture/Player/walk_{i}.png').convert_alpha()
        right_player_walk = pygame.transform.flip(left_player_walk, True, False)
        left_walk_animate.append(left_player_walk)
        right_walk_animate.append(right_player_walk)
for i in range(0, 2):
    left_death_image = pygame.image.load(f'Texture/Player/death_{i}.png').convert_alpha()
    right_death_image = pygame.transform.flip(left_death_image, True, False)
    left_death_animate.append(left_death_image)
    right_death_animate.append(right_death_image)
player_frame = 0
death_frame = 0

#Health Asset
red_heart = pygame.image.load('Texture/Others/Heart/Red_Heart.png').convert_alpha()
black_heart = pygame.image.load('Texture/Others/Heart/Black_Heart.png').convert_alpha()
HEALTH_LEFT = []
for _ in range(UPGRADE_DATA_DICT["Max Health"]):
    HEALTH_LEFT.append(red_heart)
hit_delay_time = 0

###Map Assets
map_bg = pygame.image.load('Texture/Map/City_1.png').convert_alpha()
map_bg = pygame.transform.scale(map_bg, (1280,720))

#Hydra Asset
hydra_animation_list = [[], [], []]
for i in range(1, 4):
    for j in num0121:
        TEM_HYDRA_IMAGE = pygame.image.load(f'Texture/Entitys/Hydra/{i}_heads_form_{j+1}.png').convert_alpha()
        hydra_animation_list[i-1].append(TEM_HYDRA_IMAGE)
HYDRA_HEALTH = 3
hydra_frame = 0
hydra_status = "Move"
hydra_head_left = -1
hydra_heal_frame = 30

###Tiles Inventory
inventory_list = []

###Ground Tile Asset
tile_image_list = []
tile_name_list_tem1 = list(range(0, 10))
tile_name_list_tem2 = ["plus", "minus", "times", "obelus", "equal"]
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
ENEMY_TILE_ATTRIBUTE = []
ENEMY_HP =  []
small_root_animation = []
#Enemy Asset
for i in range(0, 6):
    smallroot_animate = pygame.image.load(f'Texture/Entitys/Small_Root/{i}.png').convert_alpha()
    small_root_animation.append(smallroot_animate)
smallroot_frame = 0
enemy_spawn_time = 60
enemy_heart = pygame.transform.scale(red_heart, (30, 30))
flame_icon = pygame.image.load(f'Texture/Others/flame_icon.png').convert_alpha()
#Coins drop
COINS_COUNT = []
COINS_POS = []

#Merchant Assets
merchant_image = pygame.image.load('Texture/Entitys/merchant.png').convert_alpha()
white_talk_box = pygame.image.load('Texture/Gui/white_talk_box.png').convert_alpha()
MERCHANT_TALK = ["I'm a wandering merchant.", \
                 "I can upgrade your abilities for just 100 coins.", \
                 "Do you want to receive this offer?"]
l00_coin_button = pygame.image.load('Texture/Gui/100_coin_button.png').convert_alpha()
l00_coin_button = pygame.transform.scale(l00_coin_button, (60, 30))
no_button = pygame.image.load('Texture/Gui/no_button.png').convert_alpha()
no_button = pygame.transform.scale(no_button, (55, 30))


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

#Inventory Background Asset
inventory_bg_image = pygame.image.load('Texture/Others/Inventory_BG.png').convert_alpha()

#Select Tile Asset
select_tile_image_list = []
for i in range(0, 2):
    TEM_IMAGE = pygame.image.load(f'Texture/Tiles/Select/{i}.png').convert_alpha()
    select_tile_image_list.append(TEM_IMAGE)
select_inven_frame = 0

#For Calculate
operators_list = ["+", "-", "*", "/", "="]

#Gui Main Menu
main_menu_bg = pygame.transform.scale(pygame.image.load('TExture/Others/main_menu_background.png').convert_alpha(), (1380, 720))
game_icon_image = pygame.transform.scale(pygame.image.load('game_icon.png').convert_alpha(), (300, 300))
play_button_image = pygame.transform.scale(pygame.image.load('Texture/Gui/play_button.png').convert_alpha(), (300, 100))
upgrade_button_image = pygame.transform.scale(pygame.image.load('Texture/Gui/upgrade_button.png').convert_alpha(), (300, 100))
exit_button_image = pygame.transform.scale(pygame.image.load('Texture/Gui/exit_button.png').convert_alpha(), (300, 100))
upgrade_gui_image = pygame.transform.scale(pygame.image.load('Texture/Gui/upgrade_gui.png').convert_alpha(), (600, 500))
hanging_line_image = pygame.transform.scale(pygame.image.load('Texture/Gui/hanging_line.png').convert_alpha(), (120, 180))
volume_circle_image = pygame.transform.scale(pygame.image.load('Texture/Gui/volume_circle.png').convert_alpha(), (25, 25))
volume_bar_image = pygame.transform.scale(pygame.image.load('Texture/Gui/volume_bar.png').convert_alpha(), (202, 20))
yes_no_gui = pygame.image.load('Texture/Gui/yes_no_gui.png').convert_alpha()
#Get Hitbox Gui
game_icon_hitbox = game_icon_image.get_rect()
play_button_hitbox = play_button_image.get_rect()
upgrade_button_hitbox = play_button_image.get_rect()
exit_button_hitbox = play_button_image.get_rect()
hanging_line_hitbox = hanging_line_image.get_rect()
upgrade_gui_hitbox = upgrade_gui_image.get_rect()
volume_circle_hitbox = volume_circle_image.get_rect()
volume_bar_hitbox = volume_bar_image.get_rect()
#Set Gui Position
game_icon_hitbox.x, game_icon_hitbox.y = 540, 0
play_button_hitbox.x, play_button_hitbox.y = 540, 280
upgrade_button_hitbox.x, upgrade_button_hitbox.y = 540, 380
exit_button_hitbox.x, exit_button_hitbox.y = 540, 480
hanging_line_hitbox.x, hanging_line_hitbox.y = 640, 330
upgrade_gui_hitbox.x, upgrade_gui_hitbox.y = -1850, 150
volume_circle_hitbox.x, volume_circle_hitbox.y = 1100, 685
volume_bar_hitbox.x, volume_bar_hitbox.y = 1109, 689

#Rotate Upgrade Gui
MOVE_UPGRADE_MENU_VAR = 0
STATUS_UPGRADE_MENU = "Close"
STATUS_SWITCH_DELAY = 0

#Upgrade Assets
backpack_upgrade_image = pygame.transform.scale(pygame.image.load('Texture/Upgrade/backpack.png').convert_alpha(), (50, 50))
length_upgrade_image = pygame.transform.scale(pygame.image.load('Texture/Upgrade/health.png').convert_alpha(), (50, 50))
health_upgrade_image = pygame.transform.scale(pygame.image.load('Texture/Upgrade/length.png').convert_alpha(), (50, 50))
click_to_upgrade_image = pygame.transform.scale(pygame.image.load('Texture/Upgrade/click_to_upgrade.png').convert_alpha(), (25, 25))
gray_click_to_upgrade_image = pygame.transform.scale(pygame.image.load('Texture/Upgrade/gray_click_to_upgrade.png').convert_alpha(), (25, 25))
coin_image = pygame.transform.scale(pygame.image.load('Texture/Others/coin.png').convert_alpha(), (30, 30))
gray_coin_image = pygame.transform.scale(pygame.image.load('Texture/Others/gray_coin.png').convert_alpha(), (30, 30))

#Click to Upgrade Button
UPGRADE_DELAY_TIME = 0
upgrade_inv_hitbox = click_to_upgrade_image.get_rect()
upgrade_health_hitbox = click_to_upgrade_image.get_rect()
upgrade_length_hitbox = click_to_upgrade_image.get_rect()
upgrade_inv_hitbox.x, upgrade_inv_hitbox.y = 390, 303
upgrade_health_hitbox.x, upgrade_health_hitbox.y = 390, 403
upgrade_length_hitbox.x, upgrade_length_hitbox.y = 390, 503


#Sound Loader
open_upgrade_sound = pygame.mixer.Sound("Sound/open_upgrade_sound.mp3")
close_upgrade_sound = pygame.mixer.Sound("Sound/close_upgrade_sound.mp3")
main_menu_theme = pygame.mixer.Sound("Sound/main_menu_theme.mp3")
buy_complete_sound = pygame.mixer.Sound("Sound/buy_complete.mp3")
buy_incomplete_sound = pygame.mixer.Sound("Sound/buy_incomplete.mp3")
collect_coin_sound = pygame.mixer.Sound("Sound/collect_coin.mp3")
SOUND_LIST = [open_upgrade_sound, close_upgrade_sound, main_menu_theme, buy_complete_sound, buy_incomplete_sound]

#Upgrade Prices For Each Level
PRICES_UPGRADE = {0: 0, 1: 200, 2: 500, 3: 1000, 4: 2000, 5: 3500, 6: 5000, 7: 7500, 8: 10000, 9: 12500, 10: "MAX"}

#Main Menu Function Code Zone

def upgrade_system():
    global UPGRADE_DELAY_TIME
    CURRENT_INV_LVL = UPGRADE_DATA_DICT["Inventory Slot"]-3
    CURRENT_HEALTH_LVL = UPGRADE_DATA_DICT["Max Health"]-1
    CURRENT_LENGTH_LVL = UPGRADE_DATA_DICT["Length of Equation"]-5
    if CURRENT_INV_LVL < 9:
        if upgrade_inv_hitbox.collidepoint(mouse_pos) and UPGRADE_DELAY_TIME == 0 and UPGRADE_DATA_DICT["Coins"] >= PRICES_UPGRADE[CURRENT_INV_LVL+1] and pygame.mouse.get_pressed()[0]:
            buy_complete_sound.play()
            UPGRADE_DATA_DICT["Coins"] -= PRICES_UPGRADE[CURRENT_INV_LVL+1]
            UPGRADE_DATA_DICT["Inventory Slot"] += 1
            UPGRADE_DELAY_TIME = 15
        if upgrade_inv_hitbox.collidepoint(mouse_pos) and UPGRADE_DELAY_TIME == 0 and pygame.mouse.get_pressed()[0]:
            buy_incomplete_sound.play()
    if CURRENT_HEALTH_LVL < 9:
        if upgrade_health_hitbox.collidepoint(mouse_pos) and UPGRADE_DELAY_TIME == 0 and UPGRADE_DATA_DICT["Coins"] >= PRICES_UPGRADE[CURRENT_HEALTH_LVL+1] and pygame.mouse.get_pressed()[0]:
            buy_complete_sound.play()
            UPGRADE_DATA_DICT["Coins"] -= PRICES_UPGRADE[CURRENT_HEALTH_LVL+1]
            UPGRADE_DATA_DICT["Max Health"] += 1
            UPGRADE_DELAY_TIME = 15
        elif upgrade_health_hitbox.collidepoint(mouse_pos) and UPGRADE_DELAY_TIME == 0 and pygame.mouse.get_pressed()[0]:
            buy_incomplete_sound.play()
    if CURRENT_LENGTH_LVL < 9:
        if upgrade_length_hitbox.collidepoint(mouse_pos) and UPGRADE_DELAY_TIME == 0 and UPGRADE_DATA_DICT["Coins"] >= PRICES_UPGRADE[CURRENT_LENGTH_LVL+1] and pygame.mouse.get_pressed()[0]:
            buy_complete_sound.play()
            UPGRADE_DATA_DICT["Coins"] -= PRICES_UPGRADE[CURRENT_LENGTH_LVL+1]
            UPGRADE_DATA_DICT["Length of Equation"] += 1
            UPGRADE_DELAY_TIME = 15
        elif upgrade_length_hitbox.collidepoint(mouse_pos) and UPGRADE_DELAY_TIME == 0 and pygame.mouse.get_pressed()[0]:
            buy_incomplete_sound.play()

def set_volume():
    for TEM_SOUND in SOUND_LIST:
        TEM_SOUND.set_volume(GAME_SETTINGS_DICT["Game Volume"]/100)

def save_settings():
    #Update Settings Data
    with open("Data/game_settings.txt", "w") as game_settings:
        json.dump(GAME_SETTINGS_DICT, game_settings)

def save_upgrade_data():
    #Update Upgrade Data
    with open("Data/game_data.txt", "w") as game_data:
        json.dump(UPGRADE_DATA_DICT, game_data)

def display_volume():
    if volume_bar_hitbox.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        GAME_SETTINGS_DICT["Game Volume"] = int(((mouse_pos[0]-10) - 1100)/2)
        for TEM_SOUND in SOUND_LIST:
            TEM_SOUND.set_volume(GAME_SETTINGS_DICT["Game Volume"]/100)
    volume_circle_hitbox.x = 1100+(GAME_SETTINGS_DICT["Game Volume"]*2)
    game_screen.blit(volume_bar_image, volume_bar_hitbox)
    game_screen.blit(volume_circle_image, volume_circle_hitbox)

def animation_upgrade_menu():
    global STATUS_UPGRADE_MENU, MOVE_UPGRADE_MENU_VAR
    if STATUS_UPGRADE_MENU == "Open" and MOVE_UPGRADE_MENU_VAR != 1800:
        MOVE_UPGRADE_MENU_VAR += 180
        if MOVE_UPGRADE_MENU_VAR == 1440:
            open_upgrade_sound.play()
    elif STATUS_UPGRADE_MENU == "Close" and MOVE_UPGRADE_MENU_VAR != 0:
        MOVE_UPGRADE_MENU_VAR -= 180
    elif STATUS_UPGRADE_MENU == "Close":
        STATUS_UPGRADE_MENU = "None"

def display_upgrade_menu():
    if STATUS_UPGRADE_MENU != "None":
        game_screen.blit(upgrade_gui_image, (upgrade_gui_hitbox.x+MOVE_UPGRADE_MENU_VAR, upgrade_gui_hitbox.y))
    if MOVE_UPGRADE_MENU_VAR == 1800:
        game_screen.blit(backpack_upgrade_image, (60, 290))
        game_screen.blit(length_upgrade_image, (60, 390))
        game_screen.blit(health_upgrade_image, (60, 490))
        #Set Upgrade Levels
        CURRENT_INV_LVL = UPGRADE_DATA_DICT["Inventory Slot"]-3
        CURRENT_HEALTH_LVL = UPGRADE_DATA_DICT["Max Health"]-1
        CURRENT_LENGTH_LVL = UPGRADE_DATA_DICT["Length of Equation"]-5
        #Show Levels
        game_screen.blit(silkscreen_font.render(str(CURRENT_INV_LVL+3), True, (217, 90, 90)), (350, 302))
        game_screen.blit(silkscreen_font.render(str(CURRENT_HEALTH_LVL+1), True, (217, 90, 90)), (350, 402))
        game_screen.blit(silkscreen_font.render(str(CURRENT_LENGTH_LVL+5), True, (217, 90, 90)), (350, 502))
        #Display Prices and Coins Image
        if CURRENT_INV_LVL < 9:
            if UPGRADE_DATA_DICT["Coins"] >= PRICES_UPGRADE[CURRENT_INV_LVL+1]:
                CURRENT_INV_PRICE = silkscreen_font.render(str(PRICES_UPGRADE[CURRENT_INV_LVL+1]), True, (255, 249, 134))
                game_screen.blit(coin_image, (150, 300))
                game_screen.blit(CURRENT_INV_PRICE, (180, 302))
                game_screen.blit(click_to_upgrade_image, upgrade_inv_hitbox)
            else:
                CURRENT_INV_PRICE = silkscreen_font.render(str(PRICES_UPGRADE[CURRENT_INV_LVL+1]), True, (217, 217, 217))
                game_screen.blit(gray_coin_image, (150, 300))
                game_screen.blit(CURRENT_INV_PRICE, (180, 302))
                game_screen.blit(gray_click_to_upgrade_image, upgrade_inv_hitbox)
        else:
            CURRENT_INV_PRICE = silkscreen_font.render(str(PRICES_UPGRADE[CURRENT_INV_LVL+1]), True, (217, 217, 217))
            game_screen.blit(gray_coin_image, (150, 300))
            game_screen.blit(CURRENT_INV_PRICE, (180, 302))
        if CURRENT_HEALTH_LVL < 9:
            if UPGRADE_DATA_DICT["Coins"] >= PRICES_UPGRADE[CURRENT_HEALTH_LVL+1]:
                CURRENT_HEALTH_PRICE = silkscreen_font.render(str(PRICES_UPGRADE[CURRENT_HEALTH_LVL+1]), True, (255, 249, 134))
                game_screen.blit(coin_image, (150, 400))
                game_screen.blit(CURRENT_HEALTH_PRICE, (180, 402))
                game_screen.blit(click_to_upgrade_image, upgrade_health_hitbox)
            else:
                CURRENT_HEALTH_PRICE = silkscreen_font.render(str(PRICES_UPGRADE[CURRENT_HEALTH_LVL+1]), True, (217, 217, 217))
                game_screen.blit(gray_coin_image, (150, 400))
                game_screen.blit(CURRENT_HEALTH_PRICE, (180, 402))
                game_screen.blit(gray_click_to_upgrade_image, upgrade_health_hitbox)
        else:
            CURRENT_HEALTH_PRICE = silkscreen_font.render(str(PRICES_UPGRADE[CURRENT_HEALTH_LVL+1]), True, (217, 217, 217))
            game_screen.blit(gray_coin_image, (150, 400))
            game_screen.blit(CURRENT_HEALTH_PRICE, (180, 402))
        if CURRENT_LENGTH_LVL < 9:
            if UPGRADE_DATA_DICT["Coins"] >= PRICES_UPGRADE[CURRENT_LENGTH_LVL+1]:
                CURRENT_LENGTH_PRICE = silkscreen_font.render(str(PRICES_UPGRADE[CURRENT_LENGTH_LVL+1]), True, (255, 249, 134))
                game_screen.blit(coin_image, (150, 500))
                game_screen.blit(CURRENT_LENGTH_PRICE, (180, 502))
                game_screen.blit(click_to_upgrade_image, upgrade_length_hitbox)
            else:
                CURRENT_LENGTH_PRICE = silkscreen_font.render(str(PRICES_UPGRADE[CURRENT_LENGTH_LVL+1]), True, (217, 217, 217))
                game_screen.blit(gray_coin_image, (150, 500))
                game_screen.blit(CURRENT_LENGTH_PRICE, (180, 502))
                game_screen.blit(gray_click_to_upgrade_image, upgrade_length_hitbox)
        else:
            CURRENT_LENGTH_PRICE = silkscreen_font.render(str(PRICES_UPGRADE[CURRENT_LENGTH_LVL+1]), True, (217, 217, 217))
            game_screen.blit(gray_coin_image, (150, 500))
            game_screen.blit(CURRENT_LENGTH_PRICE, (180, 502))

def main_game_menu():
    global mouse_pos, STATUS_UPGRADE_MENU, ROTATE_UPGRADE_MENU_VAR, STATUS_SWITCH_DELAY
    if exit_button_hitbox.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        pygame.quit()
        sys.exit()
    if upgrade_button_hitbox.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        if STATUS_SWITCH_DELAY == 0:
            if STATUS_UPGRADE_MENU == "Open":
                STATUS_SWITCH_DELAY = 15
                close_upgrade_sound.play()
                STATUS_UPGRADE_MENU = "Close"
            elif STATUS_UPGRADE_MENU == "Close" or STATUS_UPGRADE_MENU == "None":
                STATUS_SWITCH_DELAY = 15
                STATUS_UPGRADE_MENU = "Open"
    if play_button_hitbox.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        global playing
        playing = "in_game"
        main_menu_theme.fadeout(1000)
    game_screen.blit(game_icon_image, game_icon_hitbox)
    game_screen.blit(hanging_line_image, hanging_line_hitbox)
    game_screen.blit(play_button_image, play_button_hitbox)
    game_screen.blit(upgrade_button_image, upgrade_button_hitbox)
    game_screen.blit(exit_button_image, exit_button_hitbox)
    #Coin
    CURRENT_COIN = silkscreen_font.render(str(UPGRADE_DATA_DICT["Coins"]), True, (255, 249, 134))
    game_screen.blit(coin_image, (20, 680))
    game_screen.blit(CURRENT_COIN, (50, 682))

def mouse_detect_func():
    #Mouse Position
    global mouse_pos
    mouse_pos = pygame.mouse.get_pos()

def play_main_menu_music():
    main_menu_theme.play(loops=-1)

#Main Menu Running Zone#

if playing == "main_menu":
    play_main_menu_music()

while playing == "main_menu":
    keys = pygame.key.get_pressed()
    clock.tick(60)
    set_volume()
    for event in pygame.event.get():
        ###Exit Game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #Mouse Detection
    mouse_detect_func()

    if STATUS_SWITCH_DELAY != 0:
        STATUS_SWITCH_DELAY -= 1

    if UPGRADE_DELAY_TIME != 0:
        UPGRADE_DELAY_TIME -= 1

    #Background
    game_screen.blit(main_menu_bg, (0, 0))

    #Display Ugrade Menu
    animation_upgrade_menu()
    display_upgrade_menu()

    #Main Menu
    main_game_menu()

    #Volume Button
    display_volume()

    upgrade_system()

    #Saving Data
    save_settings()
    save_upgrade_data()

    pygame.time.delay(30)
    pygame.display.update()












#In-Game Function Code Zone#

def trading_event():
    global TALKING_FRAME, silkscreen_font_ingame, GAME_STAGE
    l00_coin_button_hitbox = l00_coin_button.get_rect()
    no_button_hitbox = no_button.get_rect()
    l00_coin_button_hitbox.x, l00_coin_button_hitbox.y = MERCHANT_X+70, MERCHANT_Y-40
    no_button_hitbox.x, no_button_hitbox.y = MERCHANT_X+150, MERCHANT_Y-40
    if ((player_hitbox.x-MERCHANT_X)**2+(player_hitbox.y-MERCHANT_Y)**2)**(0.5) < 150:
        TALKING_FRAME += 2
        if 0 < TALKING_FRAME <= 50:
            TEM_SCALE = TALKING_FRAME
            TEM_TALK_BOX = pygame.transform.scale(white_talk_box, ((TEM_SCALE+50)*3, TEM_SCALE*3))
            game_screen.blit(TEM_TALK_BOX, (MERCHANT_X-20, MERCHANT_Y-150))
        elif TALKING_FRAME > 50:
            TEM_TALK_BOX = pygame.transform.scale(white_talk_box, (300, 150))
            TEM_TEXT = silkscreen_font_ingame.render(MERCHANT_TALK[0][:int(TALKING_FRAME)-50], True, (0, 0, 0))
            game_screen.blit(TEM_TALK_BOX, (MERCHANT_X-20, MERCHANT_Y-150))
            game_screen.blit(TEM_TEXT, (MERCHANT_X, MERCHANT_Y-120))
            if TALKING_FRAME > 150:
                if TALKING_FRAME < 178:
                    TEM_TEXT = silkscreen_font_ingame.render(MERCHANT_TALK[1][:int(TALKING_FRAME)-150], True, (0, 0, 0))
                    game_screen.blit(TEM_TEXT, (MERCHANT_X, MERCHANT_Y-100))
                else:
                    TEM_TEXT = silkscreen_font_ingame.render(MERCHANT_TALK[1][0:28], True, (0, 0, 0))
                    game_screen.blit(TEM_TEXT, (MERCHANT_X, MERCHANT_Y-100))
                if TALKING_FRAME > 179:
                    TEM_TEXT = silkscreen_font_ingame.render(MERCHANT_TALK[1][29:int(TALKING_FRAME)-150], True, (0, 0, 0))
                    game_screen.blit(TEM_TEXT, (MERCHANT_X, MERCHANT_Y-80))
            if TALKING_FRAME > 250:
                TEM_TEXT = silkscreen_font_ingame.render(MERCHANT_TALK[2][:int(TALKING_FRAME)-250], True, (0, 0, 0))
                game_screen.blit(TEM_TEXT, (MERCHANT_X, MERCHANT_Y-60))
            if TALKING_FRAME > 275:
                if l00_coin_button_hitbox.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                    if UPGRADE_DATA_DICT["Coins"] >= 100:
                        UPGRADE_DATA_DICT["Coins"] -= 100
                    else:
                        UPGRADE_DATA_DICT["Coins"] = 0
                    MERCHANT_TALK[0], MERCHANT_TALK[1], MERCHANT_TALK[2] = "", "", ""
                    MERCHANT_TALK.append("Ha free coins. Nigerundayooooo.")
                    TALKING_FRAME = -50
                elif l00_coin_button_hitbox.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                    MERCHANT_TALK[0], MERCHANT_TALK[1], MERCHANT_TALK[2] = "", "", ""
                    MERCHANT_TALK.append("Nevermind, smell you later hehe.")
                    TALKING_FRAME = -50
                game_screen.blit(l00_coin_button, l00_coin_button_hitbox)
                game_screen.blit(no_button, no_button_hitbox)
        elif -50 < TALKING_FRAME < -1:
            TEM_TEXT = silkscreen_font_ingame.render(MERCHANT_TALK[3][:50-abs(int(TALKING_FRAME))], True, (0, 0, 0))
            TEM_TALK_BOX = pygame.transform.scale(white_talk_box, (300, 150))
            game_screen.blit(TEM_TALK_BOX, (MERCHANT_X-20, MERCHANT_Y-150))
            game_screen.blit(TEM_TEXT, (MERCHANT_X, MERCHANT_Y-100))
            if TALKING_FRAME == -2:
                GAME_STAGE = 1
    game_screen.blit(merchant_image, (MERCHANT_X, MERCHANT_Y))
                

def display_coins():
    for i in range(0, len(COINS_POS)):
        if COINS_POS[i].colliderect(player_hitbox):
            collect_coin_sound.play()
            UPGRADE_DATA_DICT["Coins"] += COINS_COUNT[i]
            COINS_POS.pop(i)
            COINS_COUNT.pop(i)
            return
        game_screen.blit(coin_image, COINS_POS[i])

def display_enemy_health():
    #Display Enemy Health Bar
    global silkscreen_font
    for i in range(0, len(ENEMY_TYPE)):
        TEM_HP_LEFT = str(ENEMY_HP[i])
        TEM_POS = ENEMY_POS[i]
        TEM_TEXT = silkscreen_font.render(TEM_HP_LEFT, True, (204, 0, 0))
        if ENEMY_TYPE[i] == "smallroot":
            game_screen.blit(TEM_TEXT, (TEM_POS.x+5-(10*(len(TEM_HP_LEFT)-1)), (TEM_POS.y-20)))
            game_screen.blit(enemy_heart, (TEM_POS.x+25+(10*(len(TEM_HP_LEFT)-1)), (TEM_POS.y-20)))
        elif ENEMY_TYPE[i] == "hydra":
            game_screen.blit(TEM_TEXT, (TEM_POS.x+20-(10*(len(TEM_HP_LEFT)-1)), (TEM_POS.y-20)))
            game_screen.blit(flame_icon, (TEM_POS.x+40+(10*(len(TEM_HP_LEFT)-1)), (TEM_POS.y-20)))

def rainy_day(start_from=0):
    #Change Weather To Raining (Running when Hydra Boss has arrived.)
    global BLACK_RAINY_DAY_ALPHA, RAINDROPS_COOLDOWN
    if BLACK_RAINY_DAY_ALPHA < 120:
        BLACK_RAINY_DAY_ALPHA += 2
    if RAINDROPS_COOLDOWN == 0:
        TEM_POS = raindrops.get_rect()
        raindrops_pos_list.append(TEM_POS)
        RAINDROPS_COOLDOWN = 10
    else:
        RAINDROPS_COOLDOWN -= 1
    for i in range(start_from, len(raindrops_pos_list)):
        if raindrops_pos_list[i][0] < 0 or raindrops_pos_list[i][1] > SCREEN_HEIGHT:
            raindrops_pos_list.pop(i)
            rainy_day(i)
            return
        raindrops_pos_list[i].x -= 10
        raindrops_pos_list[i].y += 10
        TEM_POS = raindrops_pos_list[i]
        game_screen.blit(raindrops, TEM_POS)

def operatorcheck(equation, operator_count=0):
    #This function check that equation are in correctly form not like "1+=1", "--1" and more..
    for is_operator in equation:
        if is_operator in operators_list:
            operator_count += 1
    if operator_count > len(equation)-operator_count:
        return "Reset"
    else:
        return dodamage(equation)

def dodamage(equation):
    #This function runs once when a new tile is approached in the equation.
    if equation.find("=") != -1:
        left_equation = equation[0:equation.find("=")]
        right_equation = equation[equation.find("=")+1:]
        try:
            eval(left_equation)
            eval(right_equation)
        except SyntaxError:
            if len(equation) >= UPGRADE_DATA_DICT["Length of Equation"]:
                return "Reset"
            else:
                return "Continue"
        except ZeroDivisionError:
            return "Reset"
        else:
            if len(equation) > UPGRADE_DATA_DICT["Length of Equation"]:
                return "Reset"
            elif eval(left_equation) == eval(right_equation):
                return eval(left_equation)
            elif len(equation) == UPGRADE_DATA_DICT["Length of Equation"]:
                return "Reset"
            else:
                return "Continue"
    elif len(equation) >= UPGRADE_DATA_DICT["Length of Equation"]:
        return "Reset"
    else:
        return "Continue"
    if len(equation) == UPGRADE_DATA_DICT["Length of Equation"]:
        return "Reset"

def cal_enemy_equation(start_from=0):
    #Calculate Enemy Equation
    global hydra_head_left
    for i in range(start_from, len(ENEMY_TYPE)):
        TEM_RESULT = operatorcheck(ENEMY_EQUATION[i])
        if TEM_RESULT == "Reset":
            ENEMY_EQUATION[i] = ""
            ENEMY_TILE_ATTRIBUTE[i] = []
        elif isinstance(TEM_RESULT, float) or isinstance(TEM_RESULT, int):
            if ENEMY_TYPE[i] == "smallroot":
                ENEMY_HP[i] -= TEM_RESULT
                ENEMY_EQUATION[i] = ""
                if ENEMY_HP[i] <= 0:
                    TEM_HITBOX = coin_image.get_rect()
                    TEM_HITBOX.x, TEM_HITBOX.y = ENEMY_POS[i].x, ENEMY_POS[i].y
                    COINS_POS.append(TEM_HITBOX)
                    COINS_COUNT.append(100)
                    ENEMY_TYPE.pop(i)
                    ENEMY_POS.pop(i)
                    ENEMY_EQUATION.pop(i)
                    ENEMY_TILE_ATTRIBUTE.pop(i)
                    ENEMY_HP.pop(i)
                    cal_enemy_equation(i)
            elif ENEMY_TYPE[i] == "hydra":
                TEM_FLAME_COUNT = 0
                for j in range(0, len(ENEMY_TILE_ATTRIBUTE[i])):
                    if ENEMY_TILE_ATTRIBUTE[i][j]:
                        TEM_FLAME_COUNT += 1
                    if len(ENEMY_TILE_ATTRIBUTE[i])-1 == j:
                        TEM_RESULT = (TEM_RESULT*(TEM_FLAME_COUNT/len(ENEMY_TILE_ATTRIBUTE[i])))
                ENEMY_HP[i] += TEM_RESULT
                ENEMY_EQUATION[i] = ""
                ENEMY_TILE_ATTRIBUTE[i] = []
                hydra_head_left -= 1
                if hydra_head_left == 0:
                    COINS_POS.append(ENEMY_POS[i])
                    COINS_COUNT.append(500)
                    ENEMY_TYPE.pop(i)
                    ENEMY_POS.pop(i)
                    ENEMY_EQUATION.pop(i)
                    ENEMY_TILE_ATTRIBUTE.pop(i)
                    ENEMY_HP.pop(i)
                    hydra_head_left = -1
                    cal_enemy_equation(i)

def delete_shoot_tile(index):
    #Delete Shooting Tile When It Already Touch Enemy
    SHOOT_TILE_TYPE.pop(index)
    SHOOT_TILE_POS.pop(index)
    SHOOT_TILE_FIRE.pop(index)
    SHOOT_TILE_VEL.pop(index)

def enemy_movement():
    #Enemy Movement
    for i in range(0, len(ENEMY_TYPE)):
        if ENEMY_TYPE[i] == "smallroot" and int(smallroot_frame) < 4:
            TEM_X_DIST = player_hitbox.x - ENEMY_POS[i].x
            TEM_Y_DIST = -(player_hitbox.y - ENEMY_POS[i].y)
            TEM_RADIAN = math.atan2(TEM_Y_DIST, TEM_X_DIST)
            ENEMY_POS[i].x += math.cos(TEM_RADIAN)
            ENEMY_POS[i].y += -(math.sin(TEM_RADIAN))
        elif ENEMY_TYPE[i] == "hydra" and hydra_status == "Move":
            TEM_X_DIST = player_hitbox.x - ENEMY_POS[i].x
            TEM_Y_DIST = -(player_hitbox.y - ENEMY_POS[i].y)
            TEM_RADIAN = math.atan2(TEM_Y_DIST, TEM_X_DIST)
            ENEMY_POS[i].x += math.cos(TEM_RADIAN)*1.5
            ENEMY_POS[i].y += -(math.sin(TEM_RADIAN))*1.5

def display_enemy_tile():
    for i in range(0, len(ENEMY_TYPE)):
        TEM_VAR = 0
        for j in ENEMY_EQUATION[i]:
            if len(ENEMY_EQUATION[i]) != 0:
                TEM_TILE_COUNT = len(ENEMY_EQUATION[i])
                if ENEMY_TILE_ATTRIBUTE[i][TEM_VAR] == True:
                    TEM_IMAGE_LIST = shoot_flame_tile_image_list
                else:
                    TEM_IMAGE_LIST = shoot_tile_image_list
                try:
                    int(j)
                except ValueError:
                    if j == "+":
                        TEM_TILE = TEM_IMAGE_LIST[10]
                    elif j == "-":
                        TEM_TILE = TEM_IMAGE_LIST[11]
                    elif j == "*":
                        TEM_TILE = TEM_IMAGE_LIST[12]
                    elif j == "/":
                        TEM_TILE = TEM_IMAGE_LIST[13]
                    elif j == "=":
                        TEM_TILE = TEM_IMAGE_LIST[14]
                else:
                    TEM_TILE = TEM_IMAGE_LIST[int(j)]
                ###Calculate Tile Position
                if ENEMY_TYPE[i] == "smallroot":
                    TEM_POS = ((ENEMY_POS[i].x)-((-18+36*TEM_TILE_COUNT/2)-(36*TEM_VAR)), (ENEMY_POS[i].y)-80)
                elif ENEMY_TYPE[i] == "hydra":
                    TEM_POS = ((ENEMY_POS[i].x)-((-35+36*TEM_TILE_COUNT/2)-(36*TEM_VAR)), (ENEMY_POS[i].y)-80)
                game_screen.blit(TEM_TILE, TEM_POS)
                TEM_VAR += 1

def display_enemy():
    global hit_delay_time, hydra_heal_frame
    for i in range(0, len(ENEMY_TYPE)):
        TEM_HITBOX = ENEMY_POS[i]
        if ENEMY_TYPE[i] == "smallroot":
            TEM_ENEMY_IMAGE = smallroot_sprite
        elif ENEMY_TYPE[i] == "hydra":
            TEM_ENEMY_IMAGE = hydra_sprite
            HYDRA_HEALTH = ENEMY_HP[i]
        if TEM_HITBOX.colliderect(player_hitbox) and hit_delay_time == 0:
            hit_delay_time = 60
            for j in range(len(HEALTH_LEFT)-1, -1, -1):
                if HEALTH_LEFT[j] == red_heart:
                    HEALTH_LEFT[j] = black_heart
                    break
        for j in range(0, len(SHOOT_TILE_TYPE)):
            TEM_SHOOT_TILE_HITBOX = SHOOT_TILE_POS[j]
            if TEM_HITBOX.colliderect(TEM_SHOOT_TILE_HITBOX):
                if SHOOT_TILE_TYPE[j] == "plus":
                    ENEMY_EQUATION[i] += "+"
                elif SHOOT_TILE_TYPE[j] == "minus":
                    ENEMY_EQUATION[i] += "-"
                elif SHOOT_TILE_TYPE[j] == "times":
                    ENEMY_EQUATION[i] += "*"
                elif SHOOT_TILE_TYPE[j] == "obelus":
                    ENEMY_EQUATION[i] += "/"
                elif SHOOT_TILE_TYPE[j] == "equal":
                    ENEMY_EQUATION[i] += "="
                else:
                    ENEMY_EQUATION[i] += str(SHOOT_TILE_TYPE[j])
                ENEMY_TILE_ATTRIBUTE[i].append(SHOOT_TILE_FIRE[j])
                delete_shoot_tile(j)
                break
        if ENEMY_TYPE[i] == "hydra":
            global hydra_head_left
            if ENEMY_HP[i] >= 1 and hydra_heal_frame == 0:
                hydra_heal_frame = 30
                ENEMY_HP[i] = ENEMY_HP[i] - 1
            elif 1 > ENEMY_HP[i] > 0 and hydra_heal_frame == 0:
                hydra_heal_frame = 30
                ENEMY_HP[i] = 0
            elif ENEMY_HP[i] == 0:
                hydra_head_left = 3
                hydra_heal_frame = 30
            else:
                hydra_heal_frame -= 1
            TEM_X_DIST = player_hitbox.x - ENEMY_POS[i].x
            TEM_Y_DIST = -(player_hitbox.y - ENEMY_POS[i].y)
            TEM_RADIAN = math.atan2(TEM_Y_DIST, TEM_X_DIST)
            ENEMY_POS[i].x += math.cos(TEM_RADIAN)
            ENEMY_POS[i].y += -(math.sin(TEM_RADIAN))
            TEM_ANGLE = math.degrees(TEM_RADIAN)
            TEM_ENEMY_IMAGE = pygame.transform.rotate(TEM_ENEMY_IMAGE, TEM_ANGLE + 90)
        game_screen.blit(TEM_ENEMY_IMAGE, ENEMY_POS[i])

def creating_enemy(types, count, enemy_health):
    for _ in range(count):
        ENEMY_TYPE.append(types)
        ENEMY_TILE_ATTRIBUTE.append(list())
        ENEMY_EQUATION.append("")
        if types == "smallroot":
            TEM_HITBOX = smallroot_sprite.get_rect()
        if types == "hydra":
            TEM_HITBOX = hydra_sprite.get_rect()
            HYDRA_HEALTH = 3
        TEM_HITBOX.x = 1300
        TEM_HITBOX.y = random.randint(250, 720)
        ENEMY_POS.append(TEM_HITBOX)
        ENEMY_HP.append(enemy_health)

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
        if ULTIMATE_CHEAT_MODE == "OFF":
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
    elif TEM_RANDOM_NUM == "flame_tile":
        TEM_GET_RECT = tile_image_list[15].get_rect()
    TEM_GET_RECT.x = random.randint(100, 1200)
    TEM_GET_RECT.y = random.randint(250, 550)
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
        elif TEM_VAR == "flame_tile":
            TEM_TILE_IMAGE = tile_image_list[15]
        game_screen.blit(TEM_TILE_IMAGE, TILE_POS[i])
        if TEM_TILE_HITBOX.colliderect(player_hitbox) and len(inventory_list) < UPGRADE_DATA_DICT["Inventory Slot"]:
            if TEM_VAR != "flame_tile":
                inventory_list.append(TEM_VAR)
                TILE_TYPE.pop(i)
                TILE_POS.pop(i)
                TILE_COUNT -= 1
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

def hydra_frame_animate():
    #Smail Root Animation Frame
    global hydra_frame
    if hydra_frame >= 3.9:
        hydra_frame = 0
    else:
        hydra_frame += 0.1

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


#In-Game Running Zone#
while playing == "in_game" and GAME_STAGE != "game_over":
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

    #Debug Mode
    if keys[pygame.K_F3] and keys[pygame.K_c]:
        if ULTIMATE_CHEAT_MODE == "OFF" and CHEAT_ACTIVATE_DELAY == 0:
            ULTIMATE_CHEAT_MODE = "ON"
            CHEAT_ACTIVATE_DELAY = 15
        elif ULTIMATE_CHEAT_MODE == "ON" and CHEAT_ACTIVATE_DELAY == 0:
            ULTIMATE_CHEAT_MODE = "OFF"
            inventory_list = []
            CHEAT_ACTIVATE_DELAY = 15
    if CHEAT_ACTIVATE_DELAY != 0:
        CHEAT_ACTIVATE_DELAY -= 1
    if ULTIMATE_CHEAT_MODE == "ON":
        inventory_list = ["plus", "minus", "times", "obelus", "equal", 9, 0]

    #Calculate Enemy Equation
    cal_enemy_equation()

    #Hydra_Frame
    hydra_frame_animate()

    #Hydra
    hydra_sprite = hydra_animation_list[hydra_head_left-1][int(hydra_frame)]

    #Enemy Movement
    enemy_movement()

    #Shooting Delay Time
    shoot_delay_func()

    #Moving Shooting Tile
    moving_shoot_tile()

    #Hit Delay
    if hit_delay_time > 0:
        hit_delay_time -= 1

    #Mouse Detection
    mouse_detect_func()

    #Map
    game_screen.blit(map_bg, (0, 0))

    #Display Coins
    display_coins()

    #Position Detect First Time
    if first_time:
        first_time = False
        player_sprite = right_idle_animate[int(player_frame)]
        player_hitbox = player_sprite.get_rect()
        player_hitbox.x, player_hitbox.y = 640, 360

    #Player Animation
    player_frame_animate()
    if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
        if mouse_pos[0] <= player_hitbox.x:
            player_sprite = left_walk_animate[int(player_frame)]
        elif mouse_pos[0] > player_hitbox.x:
            player_sprite = right_walk_animate[int(player_frame)]
    else:
        if mouse_pos[0] <= player_hitbox.x:
            player_sprite = left_idle_animate[int(player_frame)]
        elif mouse_pos[0] > player_hitbox.x:
            player_sprite = right_idle_animate[int(player_frame)]

    #Fire Chamber Animation
    global fire_chamber_sprite
    fire_cham_frame_animate()
    fire_chamber_sprite = fire_chamber_animate[int(fire_chamber_frame)]

    #Select Inventory Animation
    select_inven_animate()

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

    print(player_hitbox)

    #Tiles On Ground Blit and Detect Touching
    display_tiles_ground()

    #Small Root Animation
    smallroot_frame_animate()
    smallroot_sprite = small_root_animation[int(smallroot_frame)]

    #Summon Enemy Smallroot
    if GAME_STAGE == 1:
        if enemy_spawn_time == 0 and GAME_ENEMY_COUNT == 0:
            creating_enemy("smallroot", 1, (GAME_ENEMY_COUNT+1))
            enemy_spawn_time = 9999999999999999999999
            GAME_ENEMY_COUNT += 1
        elif enemy_spawn_time == 0 and GAME_ENEMY_COUNT < 10:
            TEM_RANDOM_EVENT = random.choice(GAME_EVENT_LEFT)
            if TEM_RANDOM_EVENT != 1:
                GAME_EVENT_LEFT.remove(TEM_RANDOM_EVENT)
                GAME_STAGE = TEM_RANDOM_EVENT
                if GAME_STAGE == "trading_event":
                    MERCHANT_X, MERCHANT_Y = random.randint(50, 970), random.randint(250, 550)
            elif TEM_RANDOM_EVENT == 1:
                creating_enemy("smallroot", 1, (GAME_ENEMY_COUNT+1))
                enemy_spawn_time = 9999999999999999999999
                GAME_ENEMY_COUNT += 1
        elif GAME_ENEMY_COUNT == 10 and enemy_spawn_time == 0:
            hydra_head_left = 3
            creating_enemy("hydra", 1, 0)
            GAME_ENEMY_COUNT += 1
        elif GAME_ENEMY_COUNT == 11 and not "hydra" in ENEMY_TYPE:
            GAME_STAGE = 2
        elif len(ENEMY_TYPE) == 0 and GAME_ENEMY_COUNT <= 10:
            enemy_spawn_time = 0

    #Display Enemy
    display_enemy()

    #Display Enemy Equation
    display_enemy_tile()

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

    #Health Left Check
    if not red_heart in HEALTH_LEFT:
        GAME_STAGE = "game_over"

    display_enemy_health()

    if GAME_STAGE == "trading_event":
        trading_event()

    #Rainy Day
    pygame.draw.rect(black_background, (0, 0, 0, BLACK_RAINY_DAY_ALPHA), [0, 0, 1280, SCREEN_HEIGHT])
    game_screen.blit(black_background, (0, 0))
    if "hydra" in ENEMY_TYPE:
        rainy_day()

    #Saving Data
    save_upgrade_data()

    #Inventory Background Blit
    game_screen.blit(inventory_bg_image, (1280, 0))

    #Inventory Tiles Blit
    display_inventory_tiles()

    #Select Inventory Blit 
    display_select_inven_tile()

    if ULTIMATE_CHEAT_MODE == "ON":
        game_screen.blit(DISPLAY_DEBUG_TEXT, (10, 680))

    pygame.time.delay(30)
    pygame.display.update()


###Death Zone###
if playing == "in_game" and GAME_STAGE == "game_over":
    if player_sprite in left_idle_animate or player_sprite in left_walk_animate:
        DEATH_ROTATE = "left"
    else:
        DEATH_ROTATE = "right"

while playing == "in_game" and GAME_STAGE == "game_over":
    #Display Everything but never move
    keys = pygame.key.get_pressed()
    clock.tick(60)
    for event in pygame.event.get():
        ###Exit Game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if death_frame < 4:
        death_frame += 0.1
    if 2 < death_frame < 4:
        print(death_frame)
        if DEATH_ROTATE == "left":
            player_sprite = left_death_animate[0]
        else:
            player_sprite = right_death_animate[0]
    elif death_frame >= 4:
        if DEATH_ROTATE == "left":
            player_sprite = left_death_animate[1]
        else:
            player_sprite = right_death_animate[1]
    game_screen.blit(map_bg, (0, 0))
    game_screen.blit(inventory_bg_image, (1280, 0))
    for i in range(0, len(COINS_POS)):
        game_screen.blit(coin_image, COINS_POS[i])
    for i in range(0, len(ENEMY_TYPE)):
        TEM_HITBOX = ENEMY_POS[i]
        if ENEMY_TYPE[i] == "smallroot":
            TEM_ENEMY_IMAGE = smallroot_sprite
        elif ENEMY_TYPE[i] == "hydra":
            TEM_ENEMY_IMAGE = hydra_sprite
        if ENEMY_TYPE[i] == "hydra":
            TEM_X_DIST = player_hitbox.x - ENEMY_POS[i].x
            TEM_Y_DIST = -(player_hitbox.y - ENEMY_POS[i].y)
            TEM_RADIAN = math.atan2(TEM_Y_DIST, TEM_X_DIST)
            TEM_ANGLE = math.degrees(TEM_RADIAN)
            TEM_ENEMY_IMAGE = pygame.transform.rotate(TEM_ENEMY_IMAGE, TEM_ANGLE + 90)
        game_screen.blit(TEM_ENEMY_IMAGE, ENEMY_POS[i])
    for i in range(0, len(HEALTH_LEFT)):
        game_screen.blit(HEALTH_LEFT[i], (10+(50*i), 10))
    game_screen.blit(player_sprite, player_hitbox)

    pygame.time.delay(30)
    pygame.display.update()
