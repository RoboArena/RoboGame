import pygame
import sys
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

        self.window_width = 1000
        self.window_height = 1000
        self.canvas = pygame.Surface((self.window_width,
                                      self.window_height))
        self.window = pygame.display.set_mode((self.window_width,
                                               self.window_height))
        spritesheet = Spritesheet('Tiles50.png')
        self.map = TileMap('RoboArena.csv', spritesheet)
        self.player = player.Player(self, 500, 500, 10, 1, 1, 1, 1, 1, 1, 0)
        self.main_menu()

    def main_menu(self):
        while True:
            """
            #We could use a background image here:
            self.window.blit(self.BG, (0, 0))
            """

            # Fills the entire screen with dark grey
            self.canvas.fill((25, 25, 25))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(self.window_width/2,
                                                   self.window_height*0.15))

            PLAY_BTN = Button(image=pygame.image.load("assets/Play Rect.png"),
                              pos=(self.window_width/2,
                                   self.window_height*0.35),
                              text_input="PLAY",
                              font=get_font(75),
                              base_color="#d7fcd4",
                              hovering_color="White")
            OPT_BTN = Button(pygame.image.load("assets/Options Rect.png"),
                             pos=(self.window_width/2,
                                  self.window_height*0.5),
                             text_input="OPTIONS",
                             font=get_font(75),
                             base_color="#d7fcd4",
                             hovering_color="White")
            QUIT_BTN = Button(image=pygame.image.load("assets/Quit Rect.png"),
                              pos=(self.window_width/2,
                                   self.window_height*0.65),
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

            OPT_TEXT = get_font(45).render("OPTIONS screen.",
                                           True,
                                           "Black")
            OPT_RECT = OPT_TEXT.get_rect(center=(self.window_width/2,
                                                 self.window_height*0.25))
            self.canvas.blit(OPT_TEXT, OPT_RECT)

            OPT_BACK = Button(image=None,
                              pos=(self.window_width/2,
                                   self.window_height*0.45),
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

        # timer display variables
        timer_event = pygame.USEREVENT+1
        timer_font = pygame.font.SysFont(None, 100)
        timer_text = timer_font.render(str(self.timer), True, (0, 128, 0))
        pygame.time.set_timer(timer_event, 1000)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                    running = False
                if event.type == timer_event:
                    self.timer -= 1
                    timer_text = timer_font.render(str(self.timer),
                                                   True, (0, 128, 0))
                    if self.timer == 0:
                        pygame.time.set_timer(timer_event, 0)

            self.delta_time = self.clock.tick(60)/1000

            # Fills the entire screen with dark grey
            self.canvas.fill((25, 25, 25))

            # draw the tilemap
            self.map.draw_map(self.canvas)

            # draw the player
            self.player.update()
            self.player.draw()

            # display the canvas on the window
            self.window.blit(self.canvas, (0, 0))

            # display timer
            timer_text_rect = timer_text.get_rect(topright=(945, 80))
            self.window.blit(timer_text, timer_text_rect)

            # display robot points
            points_font = pygame.font.SysFont(None, 50)
            points_text = points_font.render("Points: " +
                                             str(self.player.points),
                                             True, (0, 128, 0))
            points_text_rect = points_text.get_rect(topleft=(55, 80))
            self.window.blit(points_text, points_text_rect)

            # display robot properties
            properties_font = pygame.font.SysFont(None, 35)

            speed_text = properties_font.render("Speed: " +
                                                str(self.player.speed),
                                                True, (0, 128, 0))
            speed_text_rect = speed_text.get_rect(topleft=(55, 780))
            self.window.blit(speed_text, speed_text_rect)

            healing_text = properties_font.render("Healing: " +
                                                  str(self.player.healing),
                                                  True, (0, 128, 0))
            healing_text_rect = healing_text.get_rect(topleft=(55, 815))
            self.window.blit(healing_text, healing_text_rect)

            force_text = properties_font.render("Shooting Force: " +
                                                str(self.player.force),
                                                True, (0, 128, 0))
            force_text_rect = force_text.get_rect(topleft=(55, 850))
            self.window.blit(force_text, force_text_rect)

            pygame.display.flip()

            pygame.display.update()


game = Game()
