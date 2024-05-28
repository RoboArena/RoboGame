import pygame


class Player:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.r = 32
        self.dir = (90, 90)
        self.game = game
        self.surface = game.canvas
        # This is the player's hitbox, change when we have a sprite
        self.image = pygame.Surface((self.r * 2, self.r * 2))
        self.rect = self.image.get_rect()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.dir = (self.x - mouse_pos[0], self.y - mouse_pos[1])
        self.movement(500)
        self.draw()

    def draw(self):
        pygame.draw.rect(self.surface, "black", self.rect)
        pygame.draw.circle(self.surface, "blue", (self.x, self.y), self.r)
        endOfLine = (self.x - self.dir[0], self.y - self.dir[1])
        pygame.draw.line(self.surface, "black", (self.x, self.y), endOfLine)

    def movement(self, speed):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= speed * self.game.delta_time
        if keys[pygame.K_RIGHT]:
            self.x += speed * self.game.delta_time
        self.checkCollisionsx(self.game.map.tiles, keys)
        if keys[pygame.K_UP]:
            self.y -= speed * self.game.delta_time
        if keys[pygame.K_DOWN]:
            self.y += speed * self.game.delta_time
        self.checkCollisionsy(self.game.map.tiles, keys)

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def checkCollisionsx(self, tiles, keys):
        self.rect.x = self.x - self.r  # Update the Hitbox Position
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if keys[pygame.K_LEFT]:
                self.x = tile.rect.right + self.r
            if keys[pygame.K_RIGHT]:
                self.x = tile.rect.left - self.rect.w + self.r
        self.rect.x = self.x - self.r  # Update the Hitbox Position

    def checkCollisionsy(self, tiles, keys):
        self.rect.y = self.y - self.r  # Update the Hitbox Position
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if keys[pygame.K_UP]:
                self.y = tile.rect.bottom + self.r
            if keys[pygame.K_DOWN]:
                self.y = tile.rect.top - self.r
        self.rect.y = self.y - self.r  # Update the Hitbox Position
