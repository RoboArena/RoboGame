import pygame


class Player:
    def __init__(self, game, x, y, energy, wood, stone,
                 battery, speed, healing, force, points):
        self.x = x
        self.y = y
        self.energy = energy
        self.wood = wood
        self.stone = stone
        self.battery = battery
        self.speed = speed
        self.healing = healing
        self.force = force
        self.points = points
        self.dir = (90, 90)
        self.game = game
        self.surface = game.canvas
        self.image = pygame.image.load('robot.png').convert_alpha()

        # This is the player's hitbox
        self.rect = self.image.get_rect()
        self.rect.width -= 12   # Adjust the hitbox size
        self.rect.height -= 12
        self.rect.center = (self.x, self.y)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.dir = (self.x - mouse_pos[0], self.y - mouse_pos[1])
        self.movement(500)
        self.draw()

    def draw(self):
        # make Hitbox visible
        pygame.draw.rect(self.surface, "black", self.rect)
        # (1) The player is a blue circle
        # pygame.draw.circle(self.surface, "blue", (self.x, self.y), self.r)
        # (2) The player is a robot
        self.surface.blit(self.image, (self.x - self.image.get_width() // 2,
                                       self.y - self.image.get_height() // 2))
        endOfLine = (self.x - self.dir[0], self.y - self.dir[1])
        pygame.draw.line(self.surface, "black", (self.x, self.y), endOfLine)

    def movement(self, speed):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx -= speed * self.game.delta_time
        if keys[pygame.K_RIGHT]:
            dx += speed * self.game.delta_time
        if keys[pygame.K_UP]:
            dy -= speed * self.game.delta_time
        if keys[pygame.K_DOWN]:
            dy += speed * self.game.delta_time

        # Aufteilen der Bewegung in kleinere Schritte
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            return

        dx /= steps
        dy /= steps

        for _ in range(int(steps)):
            if dx != 0:
                self.x += dx
                self.checkCollisionsx(self.game.map.tiles, keys)
            if dy != 0:
                self.y += dy
                self.checkCollisionsy(self.game.map.tiles, keys)

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            tile_rect = pygame.Rect(tile.rect.x + self.game.offset_x,
                                    tile.rect.y + self.game.offset_y,
                                    tile.rect.width, tile.rect.height)
            if self.rect.colliderect(tile_rect):
                if tile.tileName != "background.png":
                    hits.append(tile)
        return hits

    def checkCollisionsx(self, tiles, keys):
        self.rect.center = (self.x, self.y)  # Update the Hitbox Position
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if keys[pygame.K_LEFT]:
                self.x = tile.rect.right + self.rect.width // 2
                self.x += self.game.offset_x
            if keys[pygame.K_RIGHT]:
                self.x = tile.rect.left - self.rect.width // 2
                self.x += self.game.offset_x
        self.rect.center = (self.x, self.y)  # Update the Hitbox Position

    def checkCollisionsy(self, tiles, keys):
        self.rect.center = (self.x, self.y)  # Update the Hitbox Position
        self.rect.bottom += 1
        self.rect.top -= 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if keys[pygame.K_UP]:
                self.y = tile.rect.bottom + self.rect.height // 2
                self.y += self.game.offset_y
            if keys[pygame.K_DOWN]:
                self.y = tile.rect.top - self.rect.height // 2
                self.y += self.game.offset_y
        self.rect.center = (self.x, self.y)  # Update the Hitbox Position
