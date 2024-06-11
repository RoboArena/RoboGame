import pygame
import bullet


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
        self.image = pygame.transform.scale(self.image, (40, 40))

        # This is the player's hitbox
        self.rect = self.image.get_rect()
        self.rect.width -= 12   # Adjust the hitbox size
        self.rect.height -= 12
        self.rect.center = (self.x, self.y)

        self.bullets = []

        # player's mining hitbox - change pygame.rect to change size of hitbox
        self.mining_hitbox = pygame.Rect(0, 0, 150, 150)
        self.mining_hitboxX = -75
        self.mining_hitboxY = -75

        # To track mouse clicks of left mouse button
        self.previous_mouse_state = pygame.mouse.get_pressed()[0]


    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.dir = (self.x - mouse_pos[0], self.y - mouse_pos[1])
        self.movement(500)
        for x in range(len(self.bullets)):
            self.bullets[x-1].updateBullet()
            if not self.bullets[x-1].valid:
                self.bullets.pop(x-1)
                break
        self.draw()
        # update the currently mineable tiles
        self.get_hits_mining(self.game.map.tiles)
        # save the previous mouse click so that you can't hold left mouse click
        # to mine stone/wood but have to click each time
        self.previous_mouse_state = pygame.mouse.get_pressed()[0]

    def draw(self):
        # make Hitbox visible
        pygame.draw.rect(self.surface, "black", self.rect)
        # draw mining hitbox (for debugging)
        pygame.draw.rect(self.surface, "red", self.mining_hitbox, 2)
        # (1) The player is a blue circle
        # pygame.draw.circle(self.surface, "blue", (self.x, self.y), self.r)
        # (2) The player is a robot
        self.surface.blit(self.image, (self.x - self.image.get_width() // 2,
                                       self.y - self.image.get_height() // 2))
        bullet_destination = (self.x - self.dir[0], self.y - self.dir[1])
        for x in range(len(self.bullets)):
            self.bullets[x-1].drawBullet(self.surface)

        if pygame.mouse.get_pressed()[0]:
            bullet_x = self.x
            bullet_y = self.y
            self.bullets.append(bullet.Bullet(bullet_x, bullet_y,
                                              self.dir, bullet_destination))

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
            
        self.get_hits_mining(self.game.map.tiles)

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

    # check if the mining_hitbox collides with wood/stone tiles.
    # If a collision happens and the player is clicking
    # on the colliding tile (stone or wood) it will be mined and the resource
    # is added to the players inventory
    def get_hits_mining(self, tiles):
        self.mining_hitbox.center = (self.x, self.y)
        mouse_pos = pygame.mouse.get_pos()
        if self.new_left_mouse_click():
            for tile in tiles:
                tile_rect = pygame.Rect(tile.rect.x + self.game.offset_x,
                                        tile.rect.y + self.game.offset_y,
                                        tile.rect.width, tile.rect.height)
                if self.mining_hitbox.colliderect(tile_rect):
                    # checks if the player aims at a tile and also presses
                    # the left mouse button
                    if self.aiming_at_tile(tile_rect, mouse_pos) and \
                       pygame.mouse.get_pressed()[0]:
                        if tile.tileName == "stone.png":
                            # update the stone tile at x,y with background.png
                            self.game.map.update_tile(tile.rect.x, tile.rect.y,
                                                      'background.png')
                            self.stone = self.stone + 1
                        if tile.tileName == "wood.png":
                            self.game.map.update_tile(tile.rect.x, tile.rect.y,
                                                      'background.png')
                            self.wood = self.wood + 1
        self.mining_hitbox.center = (self.x, self.y)
        return

    # Is the mouse currently aiming at the tile tile_rect?
    def aiming_at_tile(self, tile_rect, mouse_pos):
        # Check if the mouse position is within the bounds of the tile
        return tile_rect.collidepoint(mouse_pos)

    # if the current LMB click is a "new" click (not holding LMB)
    # then return true
    def new_left_mouse_click(self):
        current_mouse_state = pygame.mouse.get_pressed()[0]
        is_new_click = current_mouse_state and not self.previous_mouse_state
        return is_new_click

