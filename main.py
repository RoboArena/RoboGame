import pygame
import player


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.window_witdh = 1000
        self.window_height = 1000
        self.window = pygame.display.set_mode((self.window_witdh,
                                               self.window_height))
        pygame.display.set_caption("RoboArena")
        self.clock = pygame.time.Clock()
        self.player = player.Player(self, 500, 500, 32)
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
            self.window.fill((25, 25, 25))
            self.player.update()

            pygame.display.update()

        pygame.quit()


game = Game()
