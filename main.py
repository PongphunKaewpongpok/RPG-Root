BLACK_BG_SWITCH_ALPHA = 0
while True:
    ###mport Libraries
    import pygame, sys, math, json, random, os

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
    silkscreen_font_leaderboard = pygame.font.Font("Texture/Fonts/Silkscreen/slkscr.ttf", 16)
    game_over_title_font = pygame.font.Font("Texture/Fonts/Silkscreen/slkscr.ttf", 100)
    game_over_desc_font = silkscreen_font
    pause_title_font = game_over_title_font
    #Set Text
    DISPLAY_DEBUG_TEXT = silkscreen_font.render("DEBUG MODE: ON", True, (114, 255, 131))

    #Game Over
    GAME_OVER_ALPHA = 0

    #Switch Scene
    black_bg_switch = pygame.Surface((SCREEN_WEIGHT, SCREEN_HEIGHT), pygame.SRCALPHA)


    #Rain Weather
    BLACK_RAINY_DAY_ALPHA = 0
    black_background = pygame.Surface((SCREEN_WEIGHT, SCREEN_HEIGHT), pygame.SRCALPHA)
    raindrops = pygame.image.load('Texture/Others/raindrops.png').convert_alpha()
    raindrops = pygame.transform.rotate(raindrops, -45)
    raindrops_ground = pygame.image.load('Texture/Others/raindrops_ground.png').convert_alpha()
    raindrops_ground = pygame.transform.scale(raindrops_ground, (9, 45))
    raindrops_pos_list = []
    raindrops_y_end_list = []
    raindrops_time_list = []

    #Got Damage
    red_background = pygame.Surface((SCREEN_WEIGHT, SCREEN_HEIGHT), pygame.SRCALPHA)
    RED_GOT_DAMAGE_ALPHA = 0

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
    poison_area_frame = 0
    poison_ball_image = pygame.image.load('Texture/Entitys/Hydra/poison_ball.png').convert_alpha()
    poison_area_list = []
    for i in range(0, 5):
        poison_area_image = pygame.image.load(f'Texture/Entitys/Hydra/poison_area/{i}.png').convert_alpha()
        poison_area_list.append(poison_area_image)
    poison_area_warn_image = pygame.image.load('Texture/Entitys/Hydra/poison_area/red.png').convert_alpha()
    POISON_BALL_POS = []
    POISON_BALL_END = []
    POISON_BALL_TIME = []
    POISON_AREA_POS = []
    POISON_AREA_TIME = []
    hydra_skill_cooldown = 90

    #Game Paused
    pause_bg = pygame.Surface((SCREEN_WEIGHT, SCREEN_HEIGHT), pygame.SRCALPHA)
    PAUSE_DELAY = 0
    press_to_pause_image = pygame.image.load('Texture/Gui/press_to_pause.png').convert_alpha()
    press_to_continue_image = pygame.image.load('Texture/Gui/press_to_continue.png').convert_alpha()
    back_to_main_menu_image = pygame.transform.scale(pygame.image.load('Texture/Gui/back_to_main_menu.png').convert_alpha(), (300, 100))
    #Set Position
    press_to_pause_hitbox = press_to_pause_image.get_rect()
    press_to_continue_hitbox = press_to_continue_image.get_rect()
    back_to_main_menu_hitbox = back_to_main_menu_image.get_rect()
    press_to_pause_hitbox.x, press_to_pause_hitbox.y = 10, 10
    press_to_continue_hitbox.x, press_to_continue_hitbox.y = 10, 10

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
    GOT_UPGRADE_MERCHANT = [None, None]

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
    leaderboard_button_image = pygame.transform.scale(pygame.image.load('Texture/Gui/leaderboard_button.png').convert_alpha(), (300, 100))
    leaderboard_gui_image = pygame.transform.scale(pygame.image.load('Texture/Gui/leaderboard_gui.png').convert_alpha(), (500, 350))
    #Get Hitbox Gui
    game_icon_hitbox = game_icon_image.get_rect()
    play_button_hitbox = play_button_image.get_rect()
    upgrade_button_hitbox = play_button_image.get_rect()
    exit_button_hitbox = play_button_image.get_rect()
    hanging_line_hitbox = hanging_line_image.get_rect()
    upgrade_gui_hitbox = upgrade_gui_image.get_rect()
    volume_circle_hitbox = volume_circle_image.get_rect()
    volume_bar_hitbox = volume_bar_image.get_rect()
    leaderboard_button_hitbox = leaderboard_button_image.get_rect()
    leaderboard_gui_hitbox = leaderboard_gui_image.get_rect()
    #Set Gui Position
    game_icon_hitbox.x, game_icon_hitbox.y = 540, 0
    play_button_hitbox.x, play_button_hitbox.y = 540, 280
    upgrade_button_hitbox.x, upgrade_button_hitbox.y = 540, 380
    exit_button_hitbox.x, exit_button_hitbox.y = 540, 480
    hanging_line_hitbox.x, hanging_line_hitbox.y = 640, 330
    upgrade_gui_hitbox.x, upgrade_gui_hitbox.y = -1850, 150
    volume_circle_hitbox.x, volume_circle_hitbox.y = 1100, 685
    volume_bar_hitbox.x, volume_bar_hitbox.y = 1109, 689
    leaderboard_gui_hitbox.x, leaderboard_gui_hitbox.y = 870, -300
    leaderboard_button_hitbox.x, leaderboard_button_hitbox.y = 980, 0

    #Moving Gui
    MOVE_UPGRADE_MENU_VAR = 0
    STATUS_LEADERBOARD_MENU = "Close"
    MOVE_LEADERBOARD_MENU_VAR = 0
    STATUS_UPGRADE_MENU = "Close"
    STATUS_SWITCH_DELAY = 0

    #Upgrade Assets
    backpack_upgrade_image = pygame.transform.scale(pygame.image.load('Texture/Upgrade/backpack.png').convert_alpha(), (50, 50))
    health_upgrade_image = pygame.transform.scale(pygame.image.load('Texture/Upgrade/health.png').convert_alpha(), (50, 50))
    length_upgrade_image = pygame.transform.scale(pygame.image.load('Texture/Upgrade/length.png').convert_alpha(), (50, 50))
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
    got_damaged_sound = pygame.mixer.Sound("Sound/got_damaged.mp3")
    SOUND_LIST = [open_upgrade_sound, close_upgrade_sound, main_menu_theme, buy_complete_sound, \
                  buy_incomplete_sound, collect_coin_sound, got_damaged_sound]

    #Upgrade Prices For Each Level
    PRICES_UPGRADE = {0: 0, 1: 200, 2: 500, 3: 1000, 4: 2000, 5: 3500, 6: 5000, 7: 7500, 8: 10000, 9: 12500, 10: "MAX"}

    #Main Menu Function Code Zone

    def switch_scene_animation():
        global BLACK_BG_SWITCH_ALPHA
        if BLACK_BG_SWITCH_ALPHA > 0:
            BLACK_BG_SWITCH_ALPHA -= 5
            pygame.draw.rect(black_bg_switch, (0, 0, 0, BLACK_BG_SWITCH_ALPHA), [0, 0, 1380, SCREEN_HEIGHT])
            game_screen.blit(black_bg_switch, (0, 0))

    def display_text_leaderboard():
        for i in range(0, 3):
            TEM_EQUATION = UPGRADE_DATA_DICT["Most Damage Equation"][i]
            TEM_DAMAGE = str(UPGRADE_DATA_DICT["Most Damage"][i])
            game_screen.blit(silkscreen_font_leaderboard.render(TEM_EQUATION, True, (255, 255, 255)), (1055-(8*len(TEM_EQUATION)), 100+70*i))
            game_screen.blit(silkscreen_font_leaderboard.render(TEM_DAMAGE, True, (255, 255, 255)), (1235-(8*len(TEM_DAMAGE)), 100+70*i))

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

    def animation_leaderboard_menu():
        global STATUS_LEADERBOARD_MENU, MOVE_LEADERBOARD_MENU_VAR
        if STATUS_LEADERBOARD_MENU == "Open" and MOVE_LEADERBOARD_MENU_VAR != 300:
            MOVE_LEADERBOARD_MENU_VAR += 60
            leaderboard_button_hitbox.y += 60
            if MOVE_LEADERBOARD_MENU_VAR == 60:
                open_upgrade_sound.play()
        elif STATUS_LEADERBOARD_MENU == "Close" and MOVE_LEADERBOARD_MENU_VAR != 0:
            MOVE_LEADERBOARD_MENU_VAR -= 60
            leaderboard_button_hitbox.y -= 60
        elif STATUS_LEADERBOARD_MENU == "Close":
            STATUS_LEADERBOARD_MENU = "None"
        game_screen.blit(leaderboard_gui_image, (leaderboard_gui_hitbox.x, leaderboard_gui_hitbox.y+MOVE_LEADERBOARD_MENU_VAR))

    def display_upgrade_menu():
        if STATUS_UPGRADE_MENU != "None":
            game_screen.blit(upgrade_gui_image, (upgrade_gui_hitbox.x+MOVE_UPGRADE_MENU_VAR, upgrade_gui_hitbox.y))
        if MOVE_UPGRADE_MENU_VAR == 1800:
            game_screen.blit(backpack_upgrade_image, (60, 290))
            game_screen.blit(health_upgrade_image, (60, 390))
            game_screen.blit(length_upgrade_image, (60, 490))
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
        global mouse_pos, STATUS_UPGRADE_MENU, STATUS_SWITCH_DELAY, STATUS_LEADERBOARD_MENU, BLACK_BG_SWITCH_ALPHA
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
            BLACK_BG_SWITCH_ALPHA = 255
            main_menu_theme.fadeout(1000)
        if leaderboard_button_hitbox.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            if STATUS_SWITCH_DELAY == 0:
                if STATUS_LEADERBOARD_MENU == "Open":
                    STATUS_SWITCH_DELAY = 15
                    close_upgrade_sound.play()
                    STATUS_LEADERBOARD_MENU = "Close"
                elif STATUS_LEADERBOARD_MENU == "Close" or STATUS_LEADERBOARD_MENU == "None":
                    STATUS_SWITCH_DELAY = 15
                    STATUS_LEADERBOARD_MENU = "Open"
        game_screen.blit(leaderboard_button_image, leaderboard_button_hitbox)
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










    #In-Game Function Code Zone#
        

    def back_main_menu_button_func():
        global keys, playing, BLACK_BG_SWITCH_ALPHA
        if back_to_main_menu_hitbox.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            playing = "main_menu"
            BLACK_BG_SWITCH_ALPHA = 255
            main_menu_theme.fadeout(1000)

    def pause_button_function(TEM_PASS=False):
        global keys, PAUSE_DELAY, playing
        if PAUSE_DELAY == 0:
            if keys[pygame.K_ESCAPE]:
                TEM_PASS = True
            if press_to_pause_hitbox.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                TEM_PASS = True
            if TEM_PASS:
                if playing == "in_game":
                    playing = "game_paused"
                    PAUSE_DELAY = 15
                    back_to_main_menu_hitbox.x, back_to_main_menu_hitbox.y = 500, 300
                elif playing == "game_paused":
                    playing = "in_game"
                    PAUSE_DELAY = 15

    def game_paused_function():
        global keys, PAUSE_DELAY, playing
        while playing == "game_paused":
            keys = pygame.key.get_pressed()
            clock.tick(60)
            for event in pygame.event.get():
                ###Exit Game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            mouse_detect_func()
            display_everything()
            pygame.draw.rect(pause_bg, (0, 0, 0, 100), [0, 0, 1380, SCREEN_HEIGHT])
            game_screen.blit(pause_bg, (0, 0))
            game_screen.blit(game_over_title_font.render("Game Paused", True, (255, 255, 255)), (300, 100))
            back_main_menu_button_func()
            game_screen.blit(back_to_main_menu_image, back_to_main_menu_hitbox)
            pause_button_function()
            if PAUSE_DELAY == 0:
                if playing == "in_game":
                    PAUSE_DELAY = 15
                    continue
            else:
                PAUSE_DELAY -= 1
            if playing == "in_game":
                game_screen.blit(press_to_pause_image, press_to_pause_hitbox)
            elif playing == "game_paused":
                game_screen.blit(press_to_continue_image, press_to_continue_hitbox)
            pygame.time.delay(30)
            pygame.display.update()

    def display_everything():
        #Display Everything in Scene But Didnt Move
        game_screen.blit(map_bg, (0, 0))
        display_warn_poison_area()
        for i in range(0, len(POISON_AREA_POS)):
            game_screen.blit(poison_area_sprite, POISON_AREA_POS[i])
        for i in range(0, len(COINS_POS)):
            game_screen.blit(coin_image, COINS_POS[i])
        game_screen.blit(wand_display, wand_hitbox)
        for i in range(0, len(TILE_TYPE)):
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
        display_enemy_tile()
        display_fire()
        for i in range(0, len(SHOOT_TILE_TYPE)):
            if SHOOT_TILE_FIRE[i]:
                display_shoot_flame_tile(i)
            else:
                display_shoot_tile(i)
        game_screen.blit(player_sprite, player_hitbox)
        display_enemy_health()
        display_poison_ball()
        display_got_damage_effect()
        for i in range(0, len(raindrops_pos_list)):
            if raindrops_pos_list[i][1] > raindrops_y_end_list[i]:
                game_screen.blit(raindrops_ground, (raindrops_pos_list[i][0], raindrops_y_end_list[i]))
            else:
                game_screen.blit(raindrops, (raindrops_pos_list[i][0], raindrops_pos_list[i][1]))
        pygame.draw.rect(black_background, (0, 0, 0, BLACK_RAINY_DAY_ALPHA), [0, 0, 1280, SCREEN_HEIGHT])
        game_screen.blit(black_background, (0, 0))
        display_health()
        game_screen.blit(inventory_bg_image, (1280, 0))
        display_inventory_tiles()
        display_select_inven_tile()
        CURRENT_COIN = silkscreen_font.render(str(UPGRADE_DATA_DICT["Coins"]), True, (255, 249, 134))
        game_screen.blit(coin_image, (20, 680))
        game_screen.blit(CURRENT_COIN, (50, 682))
        if ULTIMATE_CHEAT_MODE == "ON":
            game_screen.blit(DISPLAY_DEBUG_TEXT, (1000, 680))

    def display_got_damage_effect():
        global hit_delay_time, RED_GOT_DAMAGE_ALPHA
        if hit_delay_time == 60:
            got_damaged_sound.play()
        if 45 <= hit_delay_time <= 60:
            RED_GOT_DAMAGE_ALPHA = 255*((hit_delay_time-45)/15)
        pygame.draw.rect(red_background, (255, 0, 0, RED_GOT_DAMAGE_ALPHA), [0, 0, 1280, SCREEN_HEIGHT])
        game_screen.blit(red_background, (0, 0))

    def display_warn_poison_area():
        for i in range(0, len(POISON_BALL_END)):
            game_screen.blit(poison_area_warn_image, (POISON_BALL_END[i].x-25, POISON_BALL_END[i].y-25))

    def display_poison_area(start_from=0):
        global hit_delay_time
        for i in range(start_from, len(POISON_AREA_POS)):
            POISON_AREA_TIME[i] += 1
            if POISON_AREA_POS[i].colliderect(player_hitbox) and hit_delay_time == 0:
                hit_delay_time = 60
                for j in range(len(HEALTH_LEFT)-1, -1, -1):
                    if HEALTH_LEFT[j] == red_heart:
                        HEALTH_LEFT[j] = black_heart
                        break
            game_screen.blit(poison_area_sprite, POISON_AREA_POS[i])
            if POISON_AREA_TIME[i] >= 300:
                POISON_AREA_POS.pop(i)
                POISON_AREA_TIME.pop(i)
                display_poison_area(i)
                return

    def display_poison_ball():
        for i in range(0, len(POISON_BALL_POS)):
            TEM_X_NOW, TEM_Y_NOW = POISON_BALL_POS[i].x, POISON_BALL_POS[i].y
            TEM_X_END, TEM_Y_END = POISON_BALL_END[i].x, POISON_BALL_END[i].y
            TEM_TIME = POISON_BALL_TIME[i]
            TEM_X = TEM_X_NOW + (TEM_X_END-TEM_X_NOW)*(TEM_TIME/3)
            TEM_Y = TEM_Y_NOW + (TEM_Y_END-TEM_Y_NOW)*(TEM_TIME/3)
            if TEM_TIME >= 3:
                TEM_HITBOX = poison_area_sprite.get_rect()
                TEM_HITBOX.x, TEM_HITBOX.y = TEM_X_END-25, TEM_Y_END-25
                POISON_AREA_POS.append(TEM_HITBOX)
                POISON_AREA_TIME.append(0)
                POISON_BALL_POS.pop(i)
                POISON_BALL_END.pop(i)
                POISON_BALL_TIME.pop(i)
                return
            game_screen.blit(poison_ball_image, (TEM_X, TEM_Y))

    def trading_event():
        global TALKING_FRAME, silkscreen_font_ingame, GAME_STAGE, GOT_UPGRADE_MERCHANT
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
                        CURRENT_INV_LVL = UPGRADE_DATA_DICT["Inventory Slot"]-3
                        CURRENT_HEALTH_LVL = UPGRADE_DATA_DICT["Max Health"]-1
                        CURRENT_LENGTH_LVL = UPGRADE_DATA_DICT["Length of Equation"]-5
                        if CURRENT_INV_LVL < 9 or CURRENT_HEALTH_LVL < 9 or CURRENT_LENGTH_LVL < 9:
                            if UPGRADE_DATA_DICT["Coins"] >= 100:
                                UPGRADE_DATA_DICT["Coins"] -= 100
                                RANDOM_CHANCE = random.randint(0, 9)
                                MERCHANT_TALK[0], MERCHANT_TALK[1], MERCHANT_TALK[2] = "", "", ""
                                TALKING_FRAME = -100
                                if RANDOM_CHANCE != 0:
                                    MERCHANT_TALK.append("Ha free coins. Nigerundayooooo.")
                                else:
                                    RANDOM_UPGRADE_LIST = []
                                    buy_complete_sound.play()
                                    if CURRENT_INV_LVL < 9:
                                        RANDOM_UPGRADE_LIST.append("Inventory Slot")
                                    if CURRENT_HEALTH_LVL < 9:
                                        RANDOM_UPGRADE_LIST.append("Max Health")
                                    if CURRENT_LENGTH_LVL < 9:
                                        RANDOM_UPGRADE_LIST.append("Length of Equation")
                                    RANDOM_UPGRADE = random.choice(RANDOM_UPGRADE_LIST)
                                    UPGRADE_DATA_DICT[RANDOM_UPGRADE] += 1
                                    if RANDOM_UPGRADE == "Max Health":
                                        HEALTH_LEFT.insert(0, red_heart)
                                    GOT_UPGRADE_MERCHANT = [RANDOM_UPGRADE, str(UPGRADE_DATA_DICT[RANDOM_UPGRADE]-1)+" > "+str(UPGRADE_DATA_DICT[RANDOM_UPGRADE])]
                                    MERCHANT_TALK.append("See you next time customer.")
                            else:
                                buy_incomplete_sound.play()
                        else:
                            buy_incomplete_sound.play()
                            MERCHANT_TALK[0], MERCHANT_TALK[1], MERCHANT_TALK[2] = "", "", ""
                            MERCHANT_TALK.append("All of your upgrades are already reached MAX levels.")
                        TALKING_FRAME = -100
                    elif no_button_hitbox.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                        MERCHANT_TALK[0], MERCHANT_TALK[1], MERCHANT_TALK[2] = "", "", ""
                        MERCHANT_TALK.append("Nevermind, sse you next time.")
                        TALKING_FRAME = -100
                    game_screen.blit(l00_coin_button, l00_coin_button_hitbox)
                    game_screen.blit(no_button, no_button_hitbox)
            elif -100 < TALKING_FRAME < -1:
                TEM_TEXT = silkscreen_font_ingame.render(MERCHANT_TALK[3][:100-abs(int(TALKING_FRAME))], True, (0, 0, 0))
                TEM_TALK_BOX = pygame.transform.scale(white_talk_box, (300, 150))
                game_screen.blit(TEM_TALK_BOX, (MERCHANT_X-20, MERCHANT_Y-150))
                game_screen.blit(TEM_TEXT, (MERCHANT_X, MERCHANT_Y-100))
                if GOT_UPGRADE_MERCHANT[0] == "Inventory Slot":
                    game_screen.blit(backpack_upgrade_image, (player_hitbox.x-50, player_hitbox.y-50))
                if GOT_UPGRADE_MERCHANT[0] == "Max Health":
                    game_screen.blit(health_upgrade_image, (player_hitbox.x-50, player_hitbox.y-50))
                if GOT_UPGRADE_MERCHANT[0] == "Length of Equation":
                    game_screen.blit(length_upgrade_image, (player_hitbox.x-50, player_hitbox.y-50))
                TEM_TEXT = silkscreen_font.render(GOT_UPGRADE_MERCHANT[1], True, (255, 255, 255))
                game_screen.blit(TEM_TEXT, (player_hitbox.x, player_hitbox.y-40))
                if TALKING_FRAME == -2:
                    GOT_UPGRADE_MERCHANT = [None, None]
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
        global BLACK_RAINY_DAY_ALPHA, RAINDROPS_COOLDOWN, raindrops
        if BLACK_RAINY_DAY_ALPHA < 120:
            BLACK_RAINY_DAY_ALPHA += 2
        if RAINDROPS_COOLDOWN == 0:
            raindrops_pos_list.append([random.randint(0, 1800), -10])
            raindrops_y_end_list.append(random.randint(250, 800))
            raindrops_time_list.append(0)
            RAINDROPS_COOLDOWN = 1
        else:
            RAINDROPS_COOLDOWN -= 1
        for i in range(start_from, len(raindrops_pos_list)):
            if raindrops_pos_list[i][1] > raindrops_y_end_list[i]:
                game_screen.blit(raindrops_ground, (raindrops_pos_list[i][0], raindrops_y_end_list[i]))
                if raindrops_time_list[i] >= 10:
                    raindrops_pos_list.pop(i)
                    raindrops_y_end_list.pop(i)
                    raindrops_time_list.pop(i)
                    rainy_day(i)
                    return
                else:
                    raindrops_time_list[i] += 1
            else:
                raindrops_pos_list[i][0], raindrops_pos_list[i][1] = raindrops_pos_list[i][0] - 10, raindrops_pos_list[i][1] + 10
                TEM_POS = raindrops_pos_list[i]
                game_screen.blit(raindrops, (TEM_POS[0], TEM_POS[1]))

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
                for j in range(0, 3):
                    if not ENEMY_EQUATION[i] in UPGRADE_DATA_DICT["Most Damage Equation"]:
                        if UPGRADE_DATA_DICT["Most Damage"][j] < TEM_RESULT or UPGRADE_DATA_DICT["Most Damage Equation"][j] == "N/A":
                            if j == 0:
                                UPGRADE_DATA_DICT["Most Damage"][2] = UPGRADE_DATA_DICT["Most Damage"][1]
                                UPGRADE_DATA_DICT["Most Damage"][1] = UPGRADE_DATA_DICT["Most Damage"][0]
                                UPGRADE_DATA_DICT["Most Damage Equation"][2] = UPGRADE_DATA_DICT["Most Damage Equation"][1]
                                UPGRADE_DATA_DICT["Most Damage Equation"][1] = UPGRADE_DATA_DICT["Most Damage Equation"][0]
                            if j == 1:
                                UPGRADE_DATA_DICT["Most Damage"][2] = UPGRADE_DATA_DICT["Most Damage"][1]
                                UPGRADE_DATA_DICT["Most Damage Equation"][1] = UPGRADE_DATA_DICT["Most Damage Equation"][0]
                            UPGRADE_DATA_DICT["Most Damage"][j] = int(TEM_RESULT)
                            UPGRADE_DATA_DICT["Most Damage Equation"][j] = ENEMY_EQUATION[i]
                            break
                        elif UPGRADE_DATA_DICT["Most Damage"][j] == TEM_RESULT and len(ENEMY_EQUATION[i]) >= len(UPGRADE_DATA_DICT["Most Damage Equation"][j]):
                            if j == 0:
                                UPGRADE_DATA_DICT["Most Damage"][2] = UPGRADE_DATA_DICT["Most Damage"][1]
                                UPGRADE_DATA_DICT["Most Damage"][1] = UPGRADE_DATA_DICT["Most Damage"][0]
                                UPGRADE_DATA_DICT["Most Damage Equation"][2] = UPGRADE_DATA_DICT["Most Damage Equation"][1]
                                UPGRADE_DATA_DICT["Most Damage Equation"][1] = UPGRADE_DATA_DICT["Most Damage Equation"][0]
                            if j == 1:
                                UPGRADE_DATA_DICT["Most Damage"][2] = UPGRADE_DATA_DICT["Most Damage"][1]
                                UPGRADE_DATA_DICT["Most Damage Equation"][1] = UPGRADE_DATA_DICT["Most Damage Equation"][0]
                            UPGRADE_DATA_DICT["Most Damage"][j] = int(TEM_RESULT)
                            UPGRADE_DATA_DICT["Most Damage Equation"][j] = ENEMY_EQUATION[i]
                            break
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

    def shooting_tile_pos_detect(start_from=0):
        for i in range(start_from, len(SHOOT_TILE_TYPE)):
            if SHOOT_TILE_POS[i].y >= 820 or SHOOT_TILE_POS[i].y <= -100:
                delete_shoot_tile(i)
                shooting_tile_pos_detect(i)
                return
            elif SHOOT_TILE_POS[i].x >= 1480 or SHOOT_TILE_POS[i].y <= -100:
                delete_shoot_tile(i)
                shooting_tile_pos_detect(i)
                return

    def enemy_movement():
        #Enemy Movement
        global poison_area_sprite, hydra_status, hydra_skill_cooldown
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
            elif ENEMY_TYPE[i] == "hydra" and hydra_status == "Skill":
                TEM_HITBOX = poison_ball_image.get_rect()
                TEM_HITBOX.x, TEM_HITBOX.y = ENEMY_POS[i].x, ENEMY_POS[i].y
                POISON_BALL_POS.append(TEM_HITBOX)
                TEM_HITBOX = poison_ball_image.get_rect()
                TEM_HITBOX.x, TEM_HITBOX.y = player_hitbox.x, player_hitbox.y
                POISON_BALL_END.append(TEM_HITBOX)
                POISON_BALL_TIME.append(0)
                hydra_status = "Move"
                hydra_skill_cooldown = 90

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
            game_screen.blit(HEALTH_LEFT[i], (60+(50*i), 10))

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

    def poison_area_animate():
        global poison_area_frame
        if poison_area_frame >= 4.9:
            poison_area_frame = 0
        else:
            poison_area_frame += 0.1

    def shoot_delay_func():
        global SHOOT_DELAY_TIME
        if SHOOT_DELAY_TIME > 0:
            SHOOT_DELAY_TIME -= 1

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
        animation_leaderboard_menu()

        #Main Menu
        main_game_menu()

        #Volume Button
        display_volume()

        #Upgrade System
        upgrade_system()

        #Display Text in Leaderboard
        if STATUS_LEADERBOARD_MENU == "Open" and MOVE_LEADERBOARD_MENU_VAR == 300:
            display_text_leaderboard()

        #Saving Data
        save_settings()
        save_upgrade_data()

        #Switch Black Scene
        switch_scene_animation()

        pygame.time.delay(30)
        pygame.display.update()

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
            if player_hitbox.y <= 170:
                player_hitbox.y += MOVEMENT_SPEED
        if keys[pygame.K_s]:
            player_hitbox.y += MOVEMENT_SPEED
            if player_hitbox.y >= 670:
                player_hitbox.y -= MOVEMENT_SPEED
        if keys[pygame.K_a]:
            player_hitbox.x -= MOVEMENT_SPEED
            if player_hitbox.x <= 0:
                player_hitbox.x += MOVEMENT_SPEED
        if keys[pygame.K_d]:
            player_hitbox.x += MOVEMENT_SPEED
            if player_hitbox.x >= 1230:
                player_hitbox.x -= MOVEMENT_SPEED

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

        #Game Paused
        if PAUSE_DELAY != 0:
            PAUSE_DELAY -= 1
        pause_button_function()
        game_paused_function()

        #Calculate Enemy Equation
        cal_enemy_equation()

        #Hydra_Frame
        hydra_frame_animate()

        #Hydra
        hydra_sprite = hydra_animation_list[hydra_head_left-1][int(hydra_frame)]
        poison_area_sprite = poison_area_list[int(poison_area_frame)]

        for i in range(0, len(POISON_BALL_TIME)):
            POISON_BALL_TIME[i] += 0.05

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

        #Display Warn Poison Area
        display_warn_poison_area()

        #Display Posion Area
        display_poison_area()

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

        #Delete Shooting Tile That Out of the Map
        shooting_tile_pos_detect()

        #Shooting Tile Blit
        for i in range(0, len(SHOOT_TILE_TYPE)):
            if SHOOT_TILE_FIRE[i]:
                display_shoot_flame_tile(i)
            else:
                make_flame_tile(i)
                display_shoot_tile(i)

        #Player Sprite Blit
        game_screen.blit(player_sprite, player_hitbox)

        #Health Left Check
        if not red_heart in HEALTH_LEFT:
            GAME_STAGE = "game_over"

        #Display Enemy Health
        display_enemy_health()

        #Display Poison Ball
        display_poison_ball()

        if GAME_STAGE == "trading_event":
            trading_event()

        #Display Got Damage Effect
        display_got_damage_effect()

        #Rainy Day
        if "hydra" in ENEMY_TYPE:
            rainy_day()
            poison_area_animate()
            if hydra_skill_cooldown != 0:
                hydra_skill_cooldown -= 1
            else:
                hydra_status = "Skill"

        pygame.draw.rect(black_background, (0, 0, 0, BLACK_RAINY_DAY_ALPHA), [0, 0, 1280, SCREEN_HEIGHT])
        game_screen.blit(black_background, (0, 0))

        #Health Bar Blit
        display_health()

        #Saving Data
        save_upgrade_data()

        #Inventory Background Blit
        game_screen.blit(inventory_bg_image, (1280, 0))

        #Inventory Tiles Blit
        display_inventory_tiles()

        #Select Inventory Blit 
        display_select_inven_tile()

        if playing == "in_game":
            game_screen.blit(press_to_pause_image, press_to_pause_hitbox)
        elif playing == "game_paused":
            game_screen.blit(press_to_continue_image, press_to_pause_hitbox)

        CURRENT_COIN = silkscreen_font.render(str(UPGRADE_DATA_DICT["Coins"]), True, (255, 249, 134))
        game_screen.blit(coin_image, (20, 680))
        game_screen.blit(CURRENT_COIN, (50, 682))

        if ULTIMATE_CHEAT_MODE == "ON":
            game_screen.blit(DISPLAY_DEBUG_TEXT, (1000, 680))

        #Switch Black Scene
        switch_scene_animation()

        pygame.time.delay(30)
        pygame.display.update()

    ##Death Zone Code

    def display_game_over_text():
        global GAME_OVER_ALPHA
        if GAME_OVER_ALPHA <= 255:
            GAME_OVER_ALPHA += 2
        else:
            back_main_menu_button_func()
        TITLE_GAME_OVER_TEXT = game_over_title_font.render("GAME OVER", True, (236, 28, 36))
        DESC_GAME_OVER_TEXT = game_over_desc_font.render("Upgrading is the best option to win more easily in this game.", True, (236, 28, 36))
        if GAME_OVER_ALPHA < 127:
            TITLE_GAME_OVER_TEXT.set_alpha(GAME_OVER_ALPHA*2)
            DESC_GAME_OVER_TEXT.set_alpha(0)
            back_to_main_menu_image.set_alpha(0)
        else:
            TITLE_GAME_OVER_TEXT.set_alpha(255)
            DESC_GAME_OVER_TEXT.set_alpha((GAME_OVER_ALPHA-127)*2)
            back_to_main_menu_image.set_alpha((GAME_OVER_ALPHA-127)*2)
        game_screen.blit(TITLE_GAME_OVER_TEXT, (340, 310))
        game_screen.blit(DESC_GAME_OVER_TEXT, (100, 410))
        game_screen.blit(back_to_main_menu_image, back_to_main_menu_hitbox)

    ###Death Zone###
    if playing == "in_game" and GAME_STAGE == "game_over":
        main_menu_theme.play(loops=-1)
        back_to_main_menu_hitbox.x, back_to_main_menu_hitbox.y = 500, 550
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
        mouse_detect_func()
        #Hit Delay
        if hit_delay_time > 0:
            hit_delay_time -= 1
        if death_frame < 4:
            death_frame += 0.1
        if 2 < death_frame < 4:
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
        game_screen.blit(player_sprite, player_hitbox)
        display_got_damage_effect()
        if "hydra" in ENEMY_TYPE:
            rainy_day()
        game_screen.blit(inventory_bg_image, (1280, 0))
        pygame.draw.rect(black_background, (0, 0, 0, BLACK_RAINY_DAY_ALPHA), [0, 0, 1280, SCREEN_HEIGHT])
        game_screen.blit(black_background, (0, 0))
        display_health()

        display_game_over_text()

        pygame.time.delay(30)
        pygame.display.update()
