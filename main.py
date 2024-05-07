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

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                    running = False

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
