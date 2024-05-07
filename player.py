import pygame


class Player:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.r = 32
        self.dir = (90, 90)
        self.game = game
        self.surface = game.canvas
        self.rect = pygame.Rect(self.x, self.y, self.r, self.r)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.dir = (self.x - mouse_pos[0], self.y - mouse_pos[1])
        self.movement(500)
        self.draw()

    def draw(self):
        pygame.draw.circle(self.surface, "blue", (self.x, self.y), self.r)
        endOfLine = (self.x - self.dir[0], self.y - self.dir[1])
        pygame.draw.line(self.surface, "black", (self.x, self.y), endOfLine)

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
