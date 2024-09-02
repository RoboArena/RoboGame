import pygame
import sys
import os
import player
import weapon
import sound_effects
from spritesheet import Spritesheet
from tiles import TileMap
from button import Button
from weapon import Cutting_Weapon


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


class Game:

    def __init__(self, playerpos, enemypos) -> None:
        pygame.init()
        self.status = 1

        # clock variables:
        self.clock = pygame.time.Clock()
        self.timer = 120

        # Get the current display information
        display_info = pygame.display.Info()
        self.window_width = display_info.current_w
        self.window_height = display_info.current_h

        # Calculate the center position
        window_x = (display_info.current_w - self.window_width) // 2
        window_y = (display_info.current_h - self.window_height) // 2

        # Set the SDL window position to the center
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_x},{window_y}"

        # Reinitialize Pygame display module to apply the new position
        pygame.display.quit()
        pygame.display.init()

        # Update the canvas and window to use the display size
        self.canvas = pygame.Surface((self.window_width, self.window_height))
        self.window = pygame.display.set_mode((self.window_width,
                                               self.window_height))

        # Load in the Spritesheet and the Tilemap
        spritesheet = Spritesheet('assets/Tiles.png')
        self.map = TileMap('RoboArena.csv', spritesheet)

        # Calculate the offsets to center the map
        self.offset_x = (self.window_width - self.map.map_w) // 2
        self.offset_y = (self.window_height - self.map.map_h) // 2

        self.player = player.Player(self, x=playerpos[0], y=playerpos[1],
                                    energy=100, wood=0, stone=0,
                                    speed=1, healing=1, points=0,
                                    weapon=weapon.Knife())
        self.enemy = player.Player(self, x=enemypos[0], y=enemypos[1],
                                   energy=100, wood=0, stone=0,
                                   speed=1, healing=1, points=0,
                                   weapon=weapon.Knife())
        self.enemyDamage = 0

    def main_menu(self):

        # Fills the entire screen with dark grey
        self.canvas.fill((25, 25, 25))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(self.window_width * 0.5,
                                               self.window_height * 0.15))

        PLAY_BTN = Button(image=pygame.image.load("assets/Play Rect.png"),
                          pos=(self.window_width * 0.5,
                          self.window_height * 0.35),
                          text_input="PLAY",
                          font=get_font(75),
                          base_color="#d7fcd4",
                          hovering_color="White")
        OPT_BTN = Button(image=pygame.image.load(
                        "assets/Options Rect.png"),
                            pos=(self.window_width * 0.5,
                                 self.window_height * 0.5),
                            text_input="OPTIONS",
                            font=get_font(75),
                            base_color="#d7fcd4",
                            hovering_color="White")
        QUIT_BTN = Button(image=pygame.image.load(
                        "assets/Quit Rect.png"),
                            pos=(self.window_width * 0.5,
                                 self.window_height * 0.65),
                            text_input="QUIT",
                            font=get_font(75),
                            base_color="#d7fcd4",
                            hovering_color="White")

        self.canvas.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BTN, OPT_BTN, QUIT_BTN]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(self.canvas)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BTN.checkForInput(MENU_MOUSE_POS):
                    sound_effects.button_main.play()
                    self.play()
                if OPT_BTN.checkForInput(MENU_MOUSE_POS):
                    sound_effects.button_main.play()
                    self.options()
                if QUIT_BTN.checkForInput(MENU_MOUSE_POS):
                    sound_effects.button_main.play()
                    pygame.quit()
                    sys.exit()
        self.window.blit(self.canvas, (0, 0))
        pygame.display.update()

    def options(self):

        OPT_MOUSE_POS = pygame.mouse.get_pos()

        self.canvas.fill("white")

        OPT_TEXT = get_font(45).render("OPTIONS screen.", True, "Black")
        OPT_RECT = OPT_TEXT.get_rect(center=(self.window_width * 0.5,
                                             self.window_height * 0.25))
        self.canvas.blit(OPT_TEXT, OPT_RECT)

        OPT_BACK = Button(image=None,
                          pos=(self.window_width * 0.5,
                               self.window_height * 0.45),
                          text_input="BACK",
                          font=get_font(75),
                          base_color="Black",
                          hovering_color="Green")

        OPT_BACK.changeColor(OPT_MOUSE_POS)
        OPT_BACK.update(self.canvas)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPT_BACK.checkForInput(OPT_MOUSE_POS):
                    sound_effects.options_menu_button.play()
                    self.status = 0

        self.canvas.blit(self.canvas, (0, 0))
        pygame.display.update()

    def get_upgrade_cost(self, ability, ressource):
        if ability == "speed":
            abi = 0
            level = self.player.speed
        else:
            abi = 1
            level = self.player.healing
        if ressource == "wood":
            res = 0
        else:
            res = 1
        wood_cost_speed = [3, 5, 10]
        stone_cost_speed = [2, 7, 14]
        wood_cost_healing = [4, 6, 12]
        stone_cost_healing = [1, 4, 13]
        costs = [[wood_cost_speed, stone_cost_speed],
                 [wood_cost_healing, stone_cost_healing]]
        return costs[abi][res][level - 1]

    def get_weapon_color(self, weapon):
        if ((weapon.wood_cost <= self.player.wood) and (
             weapon.stone_cost <= self.player.stone)):
            return pygame.Color(29, 160, 0)
        else:
            return pygame.Color(215, 0, 0)

    def draw_cost(self, wood_cost, stone_cost, rel_pos):
        image_scale = (35, 35)
        text_size = 25
        y_pos = self.window_height * rel_pos[1]
        x_wood = self.window_width * (rel_pos[0] - 0.045)
        x_wood_im = self.window_width * (rel_pos[0] - 0.015)
        x_stone = self.window_width * (rel_pos[0] + 0.015)
        x_stone_im = self.window_width * (rel_pos[0] + 0.045)
        self.displayText(
            text_size, str(wood_cost), (x_wood, y_pos), 'topleft')
        self.displaySprite(
            image_scale, 'wood.png', (x_wood_im, y_pos))
        self.displayText(
            text_size, str(stone_cost),
            (x_stone, y_pos))
        self.displaySprite(
            image_scale, 'stone.png',
            (x_stone_im, y_pos))

    def draw_ability(self, level, icon, rel_pos):
        image_scale = (35, 35)
        text_size = 25
        self.displayText(
            text_size, str(level),
            (self.window_width * (rel_pos[0] - 0.015),
             self.window_height * rel_pos[1]))
        self.displayImage(
            image_scale, icon,
            (self.window_width * (rel_pos[0] + 0.015),
             self.window_height * rel_pos[1]))

    def draw_ressource(self, level, icon, rel_pos):
        image_scale = (35, 35)
        text_size = 25
        self.displayText(
            text_size, str(level),
            (self.window_width * (rel_pos[0] - 0.015),
             self.window_height * rel_pos[1]))
        self.displaySprite(
            image_scale, icon,
            (self.window_width * (rel_pos[0] + 0.015),
             self.window_height * rel_pos[1]))

    def draw_bg_weapon(self, center_x, center_y, color):
        square = pygame.Rect(0, 0, 65, 65)
        square.center = (self.window_width * center_x,
                         self.window_height * center_y)
        pygame.draw.rect(self.canvas, color, square)
        pygame.draw.rect(self.canvas, "black", square, 4)

    def draw_bg_square(self, center_x, center_y, height, width, color):
        square = pygame.Rect(0, 0, self.window_width * width,
                             self.window_height * height)
        square.center = (self.window_width * center_x,
                         self.window_height * center_y)
        pygame.draw.rect(self.canvas, color, square)

    def draw_info(self):
        # positions
        y_s_info = 0.889
        y_h_info = 0.95
        upg_c_abi = 0.145
        x_icon = 0.235
        # button positions
        y_w_1 = self.weaponButtons()[0].y_pos / self.window_height
        y_w_2 = self.weaponButtons()[1].y_pos / self.window_height
        x_w_1_button = self.weaponButtons()[0].x_pos / self.window_width
        x_w_2_button = self.weaponButtons()[1].x_pos / self.window_width
        x_upg_c_w_1 = 0.395
        x_upg_c_w_2 = 0.565
        # collection position
        x_coll = 0.885

        # draw background
        light_gray = pygame.Color(133, 133, 133)
        dark_gray = pygame.Color(110, 110, 110)
        weapon_1_color = self.get_weapon_color(self.getNextWeapons()[0])
        weapon_2_color = self.get_weapon_color(self.getNextWeapons()[1])

        # draw background of speed upgrade costs:
        self.draw_bg_square(upg_c_abi, y_s_info, 0.06, 0.12, light_gray)
        # draw background of healing upgrade costs:
        self.draw_bg_square(upg_c_abi, y_h_info, 0.06, 0.12, light_gray)
        # draw background of speed level and icon:
        self.draw_bg_square(x_icon + 0.025, y_s_info, 0.06, 0.1, dark_gray)
        # draw background of healing level and icon:
        self.draw_bg_square(x_icon + 0.025, y_h_info, 0.06, 0.1, dark_gray)
        # draw background of collected wood
        self.draw_bg_square(x_coll, y_s_info, 0.06, 0.06, dark_gray)
        # draw background of collected stone
        self.draw_bg_square(x_coll, y_h_info, 0.06, 0.06, dark_gray)
        # draw background of first weapon button
        self.draw_bg_square(x_upg_c_w_1 + 0.025,
                            y_w_1, 0.085, 0.165, light_gray)
        self.draw_bg_weapon(x_w_1_button, y_w_1, weapon_1_color)
        # draw background of second weapon button
        self.draw_bg_square(x_upg_c_w_2 + 0.025,
                            y_w_2, 0.085, 0.165, light_gray)
        self.draw_bg_weapon(x_w_2_button, y_w_2, weapon_2_color)

        # display timer
        self.displayText(
            50, str(self.timer),
            (self.window_width * 0.9, self.window_height * 0.1),
            'topright')
        # display points
        self.displayText(35,
                         "Points: " + str(self.player.points),
                         (self.window_width * 0.14,
                          self.window_height * 0.1))
        # display speed
        self.draw_ability(self.player.speed,
                          'assets/speedometer.png', (x_icon, y_s_info))
        # display upgrade costs for speed
        w_c_speed = self.get_upgrade_cost("speed", "wood")
        s_c_speed = self.get_upgrade_cost("speed", "stone")
        self.draw_cost(w_c_speed, s_c_speed, (upg_c_abi, y_s_info))
        # display healing ability
        self.draw_ability(self.player.healing,
                          'assets/wrench.png', (x_icon, y_h_info))
        # display upgrade costs for healing ability
        w_c_healing = self.get_upgrade_cost("healing", "wood")
        s_c_healing = self.get_upgrade_cost("healing", "stone")
        self.draw_cost(w_c_healing, s_c_healing, (upg_c_abi, y_h_info))
        # display collected wood
        self.draw_ressource(self.player.wood, 'wood.png', (x_coll, y_s_info))
        # display collected stone
        self.draw_ressource(self.player.stone, 'stone.png', (x_coll, y_h_info))
        # display costs for weapon 1
        w_c_w_1 = self.getNextWeapons()[0].wood_cost
        s_c_w_1 = self.getNextWeapons()[0].stone_cost
        self.draw_cost(w_c_w_1, s_c_w_1, (x_upg_c_w_1, y_w_1))
        # display costs for weapon 2
        w_c_w_2 = self.getNextWeapons()[1].wood_cost
        s_c_w_2 = self.getNextWeapons()[1].stone_cost
        self.draw_cost(w_c_w_2, s_c_w_2, (x_upg_c_w_2, y_w_2))

    def play(self):
        timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(timer_event, 1000)
        clock = pygame.time.Clock()
        mouse_pos = pygame.mouse.get_pos()

        self.delta_time = self.clock.tick(60) / 1000

        # Fills the entire screen with dark grey
        self.canvas.fill((25, 25, 25))

        # draw the tilemap with the calculated offsets
        self.map.draw_map(self.canvas, self.offset_x, self.offset_y)

        # draw the player
        self.player.update()
        self.enemy.draw()
        self.dealDamage()
        self.draw_info()

        WEAPON_BTNS = self.weaponButtons()
        for button in [WEAPON_BTNS[0], WEAPON_BTNS[1]]:
            button.changeColor(mouse_pos)
            button.update(self.canvas)

        UPGRADE_BTNS = self.upgradeButtons()
        for up_button in [UPGRADE_BTNS[0], UPGRADE_BTNS[1]]:
            up_button.changeColor(mouse_pos)
            up_button.update(self.canvas)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN and
                    event.key == pygame.K_ESCAPE):
                self.status = 0
            if event.type == timer_event:
                self.timer -= 1
                if self.timer == 0:
                    pygame.time.set_timer(timer_event, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                next_weapons = self.getNextWeapons()
                for i in [0, 1]:
                    if (
                        (WEAPON_BTNS[i].checkForInput(mouse_pos)) and (
                            self.weapon_is_affordable(next_weapons[i]))):
                        self.player.wood -= next_weapons[i].wood_cost
                        self.player.stone -= next_weapons[i].stone_cost
                        self.player.weapon = next_weapons[i]
                        print(next_weapons[i])
                        kind = self.player.weapon.kind
                        if (kind == "Knife"):
                            sound_effects.sword_equip.play()
                        if (kind == "Bow"):
                            # this could be bow_equip sound, but I havent
                            # found a good way to distinguise between rifle
                            # and bow as both are kind = bow
                            sound_effects.sword_equip.play()
                        if (kind == "Sword"):
                            sound_effects.sword_equip.play()
                if UPGRADE_BTNS[0].checkForInput(
                    mouse_pos) and self.is_affordable(
                        "speed"):
                    self.player.wood -= self.get_upgrade_cost(
                        "speed", "wood")
                    self.player.stone -= self.get_upgrade_cost(
                        "speed", "stone")
                    self.player.speed += 1
                    sound_effects.upgrade_healing_speed.play()
                if UPGRADE_BTNS[1].checkForInput(
                    mouse_pos) and self.is_affordable(
                        "healing"):
                    self.player.wood -= self.get_upgrade_cost(
                        "healing", "wood")
                    self.player.stone -= self.get_upgrade_cost(
                        "healing", "stone")
                    self.player.healing += 1
                    sound_effects.upgrade_healing_speed.play()

        # display the canvas on the window
        self.window.blit(self.canvas, (0, 0))
        pygame.display.flip()

        pygame.display.update()

        clock.tick(30)

    def dealDamage(self):
        if isinstance(self.player.weapon, Cutting_Weapon):
            # The current weapon is a Cutting_Weapon
            if (self.enemy.rect.collidepoint(self.player.weapon.swordpoint)
                    and self.player.weapon.in_use):
                self.enemy.energy -= self.player.weapon.force
                print(self.enemy.energy)

                # uncomment this to have a sound for taking damage
                # sound_effects.take_damage.play()
        else:
            # The current weapon is not a Cutting_Weapon
            print("This is not a cutting weapon.")

    def displayText(self, fontSize, text, pos, align='center'):
        info_font = get_font(fontSize)
        info_text = info_font.render(text, True, "White")
        info_rect = info_text.get_rect()
        info_rect.center = pos

        self.canvas.blit(info_text, info_rect)

    def displayLoadedImage(self, scale, image, pos):
        image = pygame.transform.scale(image, scale)
        image_rect = image.get_rect(center=(pos[0], pos[1]))
        self.canvas.blit(image, image_rect)

    def displayImage(self, scale, image, pos):
        image = pygame.image.load(image)
        self.displayLoadedImage(scale, image, pos)

    def displaySprite(self, scale, image, pos):
        image = self.map.spritesheet.parse_sprite(image)
        self.displayLoadedImage(scale, image, pos)

    def weaponButtons(self):
        nextWeapons = self.getNextWeapons()
        # weapon buttons
        W1_BUTTON = Button(
                        pygame.transform.scale(nextWeapons[0].image, (40, 40)),
                        pos=(self.window_width * 0.48,
                             self.window_height * 0.9195),
                        text_input="",
                        font=get_font(75),
                        base_color="#d7fcd4",
                        hovering_color="White")
        W2_BUTTON = Button(
                        pygame.transform.scale(nextWeapons[1].image, (40, 40)),
                        pos=(self.window_width * 0.65,
                             self.window_height * 0.9195),
                        text_input="",
                        font=get_font(75),
                        base_color="#d7fcd4",
                        hovering_color="White")
        return [W1_BUTTON, W2_BUTTON]

    def upgradeButtons(self):
        if self.is_affordable("speed"):
            im_1 = pygame.image.load('assets/upgrade_green.png')
        else:
            im_1 = pygame.image.load('assets/upgrade_red.png')
        im_1 = pygame.transform.scale(im_1, (40, 40))
        U1_BUTTON = Button(
            im_1, pos=(self.window_width * 0.29, self.window_height * 0.889),
            text_input="", font=get_font(75),
            base_color="#d7fcd4", hovering_color="White")

        if self.is_affordable("healing"):
            im_2 = pygame.image.load('assets/upgrade_green.png')
        else:
            im_2 = pygame.image.load('assets/upgrade_red.png')
        im_2 = pygame.transform.scale(im_2, (40, 40))
        U2_BUTTON = Button(
            im_2, pos=(self.window_width * 0.29, self.window_height * 0.95),
            text_input="", font=get_font(75),
            base_color="#d7fcd4", hovering_color="White")
        return [U1_BUTTON, U2_BUTTON]

    def is_affordable(self, ability):
        return self.get_upgrade_cost(
            ability, "wood") <= self.player.wood and self.get_upgrade_cost(
                ability, "stone") <= self.player.stone

    def weapon_is_affordable(self, weapon):
        return (
            (weapon.wood_cost <= self.player.wood) and (
                weapon.stone_cost <= self.player.stone))

    def getNextWeapons(self):
        kind = self.player.weapon.kind
        if (kind == "Knife"):
            return (weapon.Bow(), weapon.Sword())
        if (kind == "Bow"):
            return (weapon.Gun(), weapon.Rifle())
        if (kind == "Sword"):
            return (weapon.Longsword(), weapon.Lasersword())
        else:
            return (weapon.DefaultWeapon(), weapon.DefaultWeapon())
