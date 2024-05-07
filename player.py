import pygame


class Player:
    def __init__(self, game, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.game = game
        self.surface = game.window
        self.rect = pygame.Rect(self.x, self.y, self.r, self.r)

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.r, self.r)
        self.movement(500)
        self.draw()

    def draw(self):
        pygame.draw.circle(self.surface, "blue", (self.x, self.y), self.r)

    def movement(self, speed):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= speed * self.game.delta_time
        if keys[pygame.K_RIGHT]:
            self.x += speed * self.game.delta_time
        if keys[pygame.K_UP]:
            self.y -= speed * self.game.delta_time
        if keys[pygame.K_DOWN]:
            self.y += speed * self.game.delta_time
