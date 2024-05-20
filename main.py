import pygame
import player
from spritesheet import Spritesheet
from tiles import TileMap


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.window_witdh = 1000
        self.window_height = 1000
        self.canvas = pygame.Surface((self.window_witdh,
                                      self.window_height))
        self.window = pygame.display.set_mode((self.window_witdh,
                                               self.window_height))
        ###
        # pygame.display.set_caption("RoboArena")
        ###
        spritesheet = Spritesheet('Tiles50.png')
        self.map = TileMap('RoboArena.csv', spritesheet)
        self.clock = pygame.time.Clock()
        self.player = player.Player(self, 500, 500)
        self.run()

    def draw_start_menu(self):
        self.window.fill((0, 0, 0))
        font = pygame.font.SysFont('sans-serif', 40)
        title = font.render('ROBO-ARENA', True, (255, 255, 255))
        start_button = font.render('Press SPACE to START', True,
                                   (255, 255, 255))
        self.window.blit(title, (self.window_witdh/2 - title.get_width()/2,
                                 self.window_height/2 - title.get_height()/2))
        self.window.blit(start_button, (self.window_witdh/2 -
                                        start_button.get_width()/2,
                                        self.window_height/2 +
                                        start_button.get_height()/2))
        pygame.display.update()

    def run(self):
        game_state = "start_menu"
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                    running = False
            if game_state == "start_menu":
                self.draw_start_menu()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    game_state = "game"

            if game_state == "game":

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

                pygame.display.update()

        pygame.quit()


game = Game()
