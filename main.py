import pygame
import player
from spritesheet import Spritesheet
from tiles import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.window_witdh = 1000
        self.window_height = 1000
        self.canvas = pygame.Surface((self.window_witdh,
                                self.window_height))

        self.window = pygame.display.set_mode((self.window_witdh,
                                               self.window_height))
        spritesheet = Spritesheet('Tiles50.png')
        self.map = TileMap('test_level.csv', spritesheet )
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
            #self.window.fill((25, 25, 25))
            self.player.update()

            self.canvas.fill((0, 180, 240)) # Fills the entire screen with light blue
            self.map.draw_map(self.canvas)
            #self.canvas.blit(player_img, player_rect)
            self.window.blit(self.canvas, (0,0))
            pygame.display.update()

        pygame.quit()


game = Game()
