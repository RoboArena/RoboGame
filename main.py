import pygame
import sys
import os
import player
import weapon
from spritesheet import Spritesheet
from tiles import TileMap
from button import Button


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


class Game:

    def __init__(self) -> None:
        pygame.init()

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

        self.player = player.Player(
            self, 500, 450, 10, 0, 0, 1, 1, 0, weapon.Knife())
        self.main_menu()

    def main_menu(self):
        while True:
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
        while True:
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
                        self.main_menu()

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

    def draw_info(self):
        # display timer
        self.displayText(
            50, str(self.timer),
            (self.window_width * 0.945, self.window_height * 0.085),
            'topright')
        # display points
        self.displayText(35,
                         "Points: " + str(self.player.points),
                         (self.window_width * 0.055,
                          self.window_height * 0.085), 'topleft')
        # display speed
        self.displayText(
            25, str(self.player.speed),
            (self.window_width * 0.22, self.window_height * 0.878), 'topleft')
        self.displayImage(
            (35, 35), 'assets/speedometer.png',
            (self.window_width * 0.25, self.window_height * 0.889), 'topleft')
        # display upgrade costs for speed
        self.displayText(
            25, str(self.get_upgrade_cost("speed", "wood")),
            (self.window_width * 0.09, self.window_height * 0.878), 'topleft')
        self.displaySprite(
            (35, 35), 'wood.png',
            (self.window_width * 0.12, self.window_height * 0.889), 'topleft')
        self.displayText(
            25, str(self.get_upgrade_cost("speed", "stone")),
            (self.window_width * 0.15, self.window_height * 0.878), 'topleft')
        self.displaySprite(
            (35, 35), 'stone.png',
            (self.window_width * 0.18, self.window_height * 0.889), 'topleft')
        # display healing ability
        self.displayText(
            25, str(self.player.healing),
            (self.window_width * 0.22, self.window_height * 0.939), 'topleft')
        self.displayImage(
            (35, 35), 'assets/wrench.png',
            (self.window_width * 0.25, self.window_height * 0.95), 'topleft')
        # display upgrade costs for healing ability
        self.displayText(
            25, str(self.get_upgrade_cost("healing", "wood")),
            (self.window_width * 0.09, self.window_height * 0.939), 'topleft')
        self.displaySprite(
            (35, 35), 'wood.png',
            (self.window_width * 0.12, self.window_height * 0.95), 'topleft')
        self.displayText(
            25, str(self.get_upgrade_cost("healing", "stone")),
            (self.window_width * 0.15, self.window_height * 0.939), 'topleft')
        self.displaySprite(
            (35, 35), 'stone.png',
            (self.window_width * 0.18, self.window_height * 0.95), 'topleft')
        # display collected wood
        self.displayText(
            25, str(self.player.wood),
            (self.window_width * 0.75, self.window_height * 0.878), 'topright')
        self.displaySprite(
            (35, 35), 'wood.png',
            (self.window_width * 0.78, self.window_height * 0.889), 'topright')
        # display collected stone
        self.displayText(
            25, str(self.player.stone),
            (self.window_width * 0.75, self.window_height * 0.939), 'topright')
        self.displaySprite(
            (35, 35), 'stone.png',
            (self.window_width * 0.78, self.window_height * 0.95), 'topright')

    def play(self):
        running = True
        timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(timer_event, 1000)
        clock = pygame.time.Clock()
        while running:

            self.delta_time = self.clock.tick(60) / 1000

            # Fills the entire screen with dark grey
            self.canvas.fill((25, 25, 25))

            # draw the tilemap with the calculated offsets
            self.map.draw_map(self.canvas, self.offset_x, self.offset_y)

            # draw the player
            self.player.update()
            self.player.draw()

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
                    running = False
                if (event.type == pygame.KEYDOWN and
                        event.key == pygame.K_ESCAPE):
                    running = False
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

    def displayText(self, fontSize, text, pos, align='center'):
        info_font = get_font(fontSize)
        info_text = info_font.render(text, True, "White")
        info_rect = info_text.get_rect()

        if align == 'center':
            info_rect.center = pos
        elif align == 'topleft':
            info_rect.topleft = pos
        elif align == 'topright':
            info_rect.topright = pos
        # Add other alignment options if needed

        self.canvas.blit(info_text, info_rect)

    def displayLoadedImage(self, scale, image, pos, align='center'):
        image = pygame.transform.scale(image, scale)
        image_rect = image.get_rect(center=(pos[0], pos[1]))
        self.canvas.blit(image, image_rect)

    def displayImage(self, scale, image, pos, align='center'):
        image = pygame.image.load(image)
        self.displayLoadedImage(scale, image, pos, align='center')

    def displaySprite(self, scale, image, pos, align='center'):
        image = self.map.spritesheet.parse_sprite(image)
        self.displayLoadedImage(scale, image, pos, align='center')

    def weaponButtons(self):
        nextWeapons = self.getNextWeapons()
        # weapon buttons
        W1_BUTTON = Button(
                        nextWeapons[0].image,
                        pos=(self.window_width * 0.45,
                             self.window_height * 0.9),
                        text_input="",
                        font=get_font(75),
                        base_color="#d7fcd4",
                        hovering_color="White")
        W2_BUTTON = Button(
                        nextWeapons[1].image,
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
            im_2, pos=(self.window_width * 0.29, self.window_height * 0.939),
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


game = Game()
