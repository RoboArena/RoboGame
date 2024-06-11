import pygame
import sys
import os
import player
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
        spritesheet = Spritesheet('Tiles.png')
        self.map = TileMap('RoboArena.csv', spritesheet)

        # Calculate the offsets to center the map
        self.offset_x = (self.window_width - self.map.map_w) // 2
        self.offset_y = (self.window_height - self.map.map_h) // 2

        self.player = player.Player(self, 500, 500, 10, 0, 0, 0, 1, 1, 1, 0)
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

            self.window.blit(self.canvas, (0, 0))
            pygame.display.update()

    def play(self):
        running = True
        timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(timer_event, 1000)
        clock = pygame.time.Clock()
        while running:
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

            self.delta_time = self.clock.tick(60) / 1000

            # Fills the entire screen with dark grey
            self.canvas.fill((25, 25, 25))

            # draw the tilemap with the calculated offsets
            self.map.draw_map(self.canvas, self.offset_x, self.offset_y)

            # draw the player
            self.player.update()
            self.player.draw()

            # display the canvas on the window
            self.window.blit(self.canvas, (0, 0))

            # display timer
            timer_font = get_font(50)
            timer_text = timer_font.render(str(self.timer), True, "Black")
            timer_text_rect = timer_text.get_rect(topright=(1380, 100))
            timer_text = timer_font.render(str(self.timer), True, "Black")
            self.window.blit(timer_text, timer_text_rect)

            # display robot points
            points_font = get_font(35)
            points_text = points_font.render("Points: " +
                                             str(self.player.points),
                                             True, "Black")
            points_text_rect = points_text.get_rect(topleft=(165, 100))
            self.window.blit(points_text, points_text_rect)

        # display robot properties
            prop_font = get_font(25)
            prop_color = "Black"

            # display speed
            speed_text = prop_font.render("Speed: " +
                                          str(self.player.speed),
                                          True, prop_color)
            speed_text_rect = speed_text.get_rect(topleft=(165, 665))
            self.window.blit(speed_text, speed_text_rect)

            # display healing ability
            healing_text = prop_font.render("Healing: " +
                                            str(self.player.healing),
                                            True, prop_color)
            healing_text_rect = healing_text.get_rect(topleft=(165, 700))
            self.window.blit(healing_text, healing_text_rect)

            # display shooting force
            force_text = prop_font.render("Shooting Force: " +
                                          str(self.player.force),
                                          True, prop_color)
            force_text_rect = force_text.get_rect(topleft=(165, 735))
            self.window.blit(force_text, force_text_rect)

        # display robot collections
            collect_font = get_font(25)
            collect_color = "Black"

            # display collected wood
            wood_text = collect_font.render("Wood: " +
                                            str(self.player.wood),
                                            True, collect_color)
            wood_text_rect = wood_text.get_rect(topright=(1380, 665))
            self.window.blit(wood_text, wood_text_rect)

            # display collected stone
            stone_text = collect_font.render("Stone: " +
                                             str(self.player.stone),
                                             True, collect_color)
            stone_text_rect = stone_text.get_rect(topright=(1380, 700))
            self.window.blit(stone_text, stone_text_rect)

            # display collected battery
            battery_text = collect_font.render("Batteries: " +
                                               str(self.player.battery),
                                               True, collect_color)
            battery_text_rect = battery_text.get_rect(topright=(1380, 735))
            self.window.blit(battery_text, battery_text_rect)

            pygame.display.flip()

            pygame.display.update()

            clock.tick(30)


game = Game()
