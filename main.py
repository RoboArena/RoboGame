import pygame
import sys
import os
import player
import weapon
from spritesheet import Spritesheet
from tiles import TileMap
from button import Button
from weapon import Cutting_Weapon


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


class Game:

    def __init__(self) -> None:
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

        self.player = player.Player(self, 500, 450, 100, 0, 0, 0, 0, 1, 1, 0,
                                    weapon.Knife())
        self.player2 = player.Player(self, 900, 450, 100, 0, 0, 0, 0, 1, 1, 0,
                                     weapon.Knife())
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
                    self.play()
                if OPT_BTN.checkForInput(MENU_MOUSE_POS):
                    self.options()
                if QUIT_BTN.checkForInput(MENU_MOUSE_POS):
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
        # return pygame.Color(215, 0, 0)
        return pygame.Color(29, 160, 0)

    def draw_info(self):
        # positions
        y_speed_info = self.window_height * 0.889
        y_healing_info = self.window_height * 0.95
        x_icons = self.window_width * 0.25
        x_levels = self.window_width * 0.22
        x_wood_cost = self.window_width * 0.1
        x_wood_cost_im = self.window_width * 0.13
        x_stone_cost = self.window_width * 0.16
        x_stone_cost_im = self.window_width * 0.19
        x_collected = self.window_width * 0.87
        x_collected_im = self.window_width * 0.9
        # button positions
        x_speed_button = self.upgradeButtons()[0].x_pos
        x_healing_button = self.upgradeButtons()[1].x_pos
        x_weapon_button_1 = self.weaponButtons()[0].x_pos
        y_weapon_button_1 = self.weaponButtons()[0].y_pos
        x_weapon_button_2 = self.weaponButtons()[1].x_pos
        y_weapon_button_2 = self.weaponButtons()[1].y_pos
        # scales
        image_scale = (35, 35)
        text_size = 25

        # draw background

        # get widths by calculating:
        # position of button - position of text that show the level
        # + buffer to make it look nicer
        speed_bg_dark = pygame.Rect(0, 0, x_speed_button - x_levels + 40, 50)
        healing_bg_dark = pygame.Rect(
            0, 0, x_healing_button - x_levels + 40, 50)
        # or by calculating:
        # position of end of upgrade costs
        # - position of start of upgrade costs + buffer
        speed_bg_light = pygame.Rect(
            0, 0, x_stone_cost_im - x_wood_cost + 50, 50)
        healing_bg_light = pygame.Rect(
            0, 0, x_stone_cost_im - x_wood_cost + 50, 50)
        # or by calculating:
        # position of ressource image - position of ressource counter + buffer
        wood_bg = pygame.Rect(0, 0, x_collected_im - x_collected + 50, 50)
        stone_bg = pygame.Rect(0, 0, x_collected_im - x_collected + 50, 50)
        # for the weapon you can just take a square bigger than the weapons
        weapon_1_bg = pygame.Rect(0, 0, 65, 65)
        weapon_2_bg = pygame.Rect(0, 0, 65, 65)
        # get positions by calculating:
        # middle of button and start of level display
        # + fourth of the buttons size
        speed_bg_dark.center = x_levels + (
            (x_speed_button - x_levels)/2), y_speed_info
        healing_bg_dark.center = x_levels + (
            (x_healing_button - x_levels)/2), y_healing_info
        # or by calculating:
        # middle of start of upgrade costs and end of upgrade costs
        # + fourth of image size
        speed_bg_light.center = x_wood_cost + (
            (x_stone_cost_im - x_wood_cost)/2), y_speed_info
        healing_bg_light.center = x_wood_cost + (
            (x_stone_cost_im - x_wood_cost)/2), y_healing_info
        # or by calculating:
        # middle of ressource image and ressource counter
        # - fourth of image size
        wood_bg.center = x_collected + (
            (x_collected_im - x_collected)/2), y_speed_info
        stone_bg.center = x_collected + (
            (x_collected_im - x_collected)/2), y_healing_info
        # for the weapons you can just use the buttons position
        weapon_1_bg.center = x_weapon_button_1, y_weapon_button_1
        weapon_2_bg.center = x_weapon_button_2, y_weapon_button_2
        # draw rectangles:
        light_gray = pygame.Color(133, 133, 133)
        dark_gray = pygame.Color(110, 110, 110)
        weapon_1_color = self.get_weapon_color(self.getNextWeapons()[0])
        weapon_2_color = self.get_weapon_color(self.getNextWeapons()[1])
        pygame.draw.rect(self.canvas, dark_gray, speed_bg_dark)
        pygame.draw.rect(self.canvas, dark_gray, healing_bg_dark)
        pygame.draw.rect(self.canvas, light_gray, speed_bg_light)
        pygame.draw.rect(self.canvas, light_gray, healing_bg_light)
        pygame.draw.rect(self.canvas, dark_gray, wood_bg)
        pygame.draw.rect(self.canvas, dark_gray, stone_bg)
        pygame.draw.rect(self.canvas, weapon_1_color, weapon_1_bg)
        pygame.draw.rect(self.canvas, weapon_2_color, weapon_2_bg)
        pygame.draw.rect(self.canvas, "black", weapon_1_bg, 4)
        pygame.draw.rect(self.canvas, "black", weapon_2_bg, 3)

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
        self.displayText(
            text_size, str(self.player.speed),
            (x_levels, y_speed_info))
        self.displayImage(
            image_scale, 'assets/speedometer.png',
            (x_icons, y_speed_info))
        # display upgrade costs for speed
        self.displayText(
            text_size, str(self.get_upgrade_cost("speed", "wood")),
            (x_wood_cost, y_speed_info), 'topleft')
        self.displaySprite(
            image_scale, 'wood.png',
            (x_wood_cost_im, y_speed_info))
        self.displayText(
            text_size, str(self.get_upgrade_cost("speed", "stone")),
            (x_stone_cost, y_speed_info))
        self.displaySprite(
            image_scale, 'stone.png',
            (x_stone_cost_im, y_speed_info))
        # display healing ability
        self.displayText(
            text_size, str(self.player.healing),
            (x_levels, y_healing_info))
        self.displayImage(
            image_scale, 'assets/wrench.png',
            (x_icons, y_healing_info))
        # display upgrade costs for healing ability
        self.displayText(
            text_size, str(self.get_upgrade_cost("healing", "wood")),
            (x_wood_cost, y_healing_info))
        self.displaySprite(
            image_scale, 'wood.png',
            (x_wood_cost_im, y_healing_info))
        self.displayText(
            text_size, str(self.get_upgrade_cost("healing", "stone")),
            (x_stone_cost, y_healing_info))
        self.displaySprite(
            image_scale, 'stone.png',
            (x_stone_cost_im, y_healing_info))
        # display collected wood
        self.displayText(
            text_size, str(self.player.wood),
            (x_collected, y_speed_info))
        self.displaySprite(
            image_scale, 'wood.png',
            (x_collected_im, y_speed_info))
        # display collected stone
        self.displayText(
            text_size, str(self.player.stone),
            (x_collected, y_healing_info))
        self.displaySprite(
            image_scale, 'stone.png',
            (x_collected_im, y_healing_info))

    def play(self):
        timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(timer_event, 1000)
        clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(60) / 1000

        # Fills the entire screen with dark grey
        self.canvas.fill((25, 25, 25))

        # draw the tilemap with the calculated offsets
        self.map.draw_map(self.canvas, self.offset_x, self.offset_y)

        # draw the player
        self.player.update()
        self.player2.draw()
        self.dealDamage()
        self.draw_info()

        WEAPON_BTNS = self.weaponButtons()
        for button in [WEAPON_BTNS[0], WEAPON_BTNS[1]]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(self.canvas)

        UPGRADE_BTNS = self.upgradeButtons()
        for up_button in [UPGRADE_BTNS[0], UPGRADE_BTNS[1]]:
            up_button.changeColor(pygame.mouse.get_pos())
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
                if WEAPON_BTNS[0].checkForInput(pygame.mouse.get_pos()):
                    self.player.weapon = self.getNextWeapons()[0]
                if WEAPON_BTNS[1].checkForInput(pygame.mouse.get_pos()):
                    self.player.weapon = self.getNextWeapons()[1]
                if UPGRADE_BTNS[0].checkForInput(
                    pygame.mouse.get_pos()) and self.is_affordable(
                        "speed"):
                    self.player.wood -= self.get_upgrade_cost(
                        "speed", "wood")
                    self.player.stone -= self.get_upgrade_cost(
                        "speed", "stone")
                    self.player.speed += 1
                if UPGRADE_BTNS[1].checkForInput(
                    pygame.mouse.get_pos()) and self.is_affordable(
                        "healing"):
                    self.player.wood -= self.get_upgrade_cost(
                        "healing", "wood")
                    self.player.stone -= self.get_upgrade_cost(
                        "healing", "stone")
                    self.player.healing += 1

        # display the canvas on the window
        self.window.blit(self.canvas, (0, 0))
        pygame.display.flip()

        pygame.display.update()

        clock.tick(30)

    def dealDamage(self):
        if isinstance(self.player.weapon, Cutting_Weapon):
            # The current weapon is a Cutting_Weapon
            if (self.player2.rect.collidepoint(self.player.weapon.swordpoint)
                    and self.player.weapon.in_use):
                self.player2.energy -= self.player.weapon.force
                print(self.player2.energy)
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
                        pos=(self.window_width * 0.45,
                             self.window_height * 0.9),
                        text_input="",
                        font=get_font(75),
                        base_color="#d7fcd4",
                        hovering_color="White")
        W2_BUTTON = Button(
                        pygame.transform.scale(nextWeapons[1].image, (40, 40)),
                        pos=(self.window_width * 0.55,
                             self.window_height * 0.9),
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
