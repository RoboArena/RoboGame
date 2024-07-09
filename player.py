import pygame
import bullet


class Player:
    def __init__(self, game, x, y, energy, wood, stone,
                 battery, speed, healing, force, points, weapon):
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
        self.image = pygame.image.load('assets/robot.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.weapon = weapon

        self.tileTupleList = []
        for tile in self.game.map.tiles:
            tile_rect = pygame.Rect(tile.rect.x + self.game.offset_x,
                                    tile.rect.y + self.game.offset_y,
                                    tile.rect.width, tile.rect.height)
            self.tileTupleList.append((tile_rect, tile.tileName))

        # This is the player's hitbox
        self.rect = self.image.get_rect()
        self.rect.width -= 12   # Adjust the hitbox size
        self.rect.height -= 12
        self.rect.center = (self.x, self.y)

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
        self.weapon.update_weapon()
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
        self.weapon.draw_weapon(
            self.x, self.y, self.dir[0], self.dir[1], self.surface)
        self.draw_health_bar(self.x, self.y, self.surface)

    def shoot(self):
        bullet_destination = (self.x - self.dir[0], self.y - self.dir[1])
        bullet_x = self.x
        bullet_y = self.y
        self.bullets.append(bullet.Bullet(bullet_x, bullet_y,
                                          self.dir,
                                          bullet_destination))

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
                self.checkCollisionsx(keys)
            if dy != 0:
                self.y += dy
                self.checkCollisionsy(keys)

    def get_collisions(self):
        hits = []
        for tile_rect, tile_name in self.tileTupleList:
            # This is a simple optimization to only check for nearby tiles
            if (abs(self.x - tile_rect.x) > 300 or
                    abs(self.y - tile_rect.y) > 300):
                continue
            if self.rect.colliderect(tile_rect):
                if tile_name not in ["background.png",
                                     "stone_wall.png",
                                     "wall_edge.png",
                                     "wood_wall.png"]:
                    hits.append(tile_rect)
        return hits

    def checkCollisionsx(self, keys):
        self.rect.center = (self.x, self.y)  # Update the Hitbox Position
        collisions = self.get_collisions()
        for tile_rect in collisions:
            if keys[pygame.K_LEFT]:
                self.x = tile_rect.right + self.rect.width // 2
            if keys[pygame.K_RIGHT]:
                self.x = tile_rect.left - self.rect.width // 2
        self.rect.center = (self.x, self.y)  # Update the Hitbox Position

    def checkCollisionsy(self, keys):
        self.rect.center = (self.x, self.y)  # Update the Hitbox Position
        self.rect.bottom += 1
        self.rect.top -= 1
        collisions = self.get_collisions()
        for tile_rect in collisions:
            if keys[pygame.K_UP]:
                self.y = tile_rect.bottom + self.rect.height // 2
            if keys[pygame.K_DOWN]:
                self.y = tile_rect.top - self.rect.height // 2
        self.rect.center = (self.x, self.y)  # Update the Hitbox Position

    # check if the mining_hitbox collides with wood/stone tiles.
    # If a collision happens and the player is clicking
    # on the colliding tile (stone or wood) it will be mined and the resource
    # is added to the players inventory
    def get_hits_mining(self, tiles):
        self.mining_hitbox.center = (self.x, self.y)
        mouse_pos = pygame.mouse.get_pos()
        if self.new_left_mouse_click():
            for i, (tile_rect, tile_name) in enumerate(self.tileTupleList):
                # This is a simple optimization to only check for nearby tiles
                if (abs(self.x - tile_rect.x) > 300 or
                        abs(self.y - tile_rect.y) > 300):
                    continue
                if self.mining_hitbox.colliderect(tile_rect):
                    # checks if the player aims at a tile and also presses
                    # the left mouse button
                    if (self.aiming_at_tile(tile_rect, mouse_pos) and
                            pygame.mouse.get_pressed()[0]):

                        # if the tile that is being mined is a stone tile
                        # correct the walls below and above the tile
                        if tile_name == "stone.png":

                            self.handle_tile_below(tile_rect)

                            if (self.handle_tile_above(tile_rect) == "stone"):
                                self.game.map.update_tile(
                                    tile_rect.x - self.game.offset_x,
                                    tile_rect.y - self.game.offset_y,
                                    'stone_wall.png'
                                )
                                self.tileTupleList[i] = (tile_rect,
                                                         "stone_wall.png")
                            else:
                                self.game.map.update_tile(
                                    tile_rect.x - self.game.offset_x,
                                    tile_rect.y - self.game.offset_y,
                                    'background.png'
                                )
                                self.tileTupleList[i] = (tile_rect,
                                                         "background.png")

                            self.stone += 1

                        # if the tile that is being mined is a wood tile
                        # correct the walls below and above the tile
                        elif tile_name == "wood.png":
                            self.handle_tile_below(tile_rect)

                            if (self.handle_tile_above(tile_rect) == "wood"):
                                self.game.map.update_tile(
                                    tile_rect.x - self.game.offset_x,
                                    tile_rect.y - self.game.offset_y,
                                    'wood_wall.png'
                                )
                                self.tileTupleList[i] = (tile_rect,
                                                         "wood_wall.png")
                            elif (self.handle_tile_above(tile_rect) == "wall"):
                                self.game.map.update_tile(
                                    tile_rect.x - self.game.offset_x,
                                    tile_rect.y - self.game.offset_y,
                                    'wall_edge.png'
                                )
                                self.tileTupleList[i] = (tile_rect,
                                                         "edge_wall.png")
                            else:
                                self.game.map.update_tile(
                                    tile_rect.x - self.game.offset_x,
                                    tile_rect.y - self.game.offset_y,
                                    'background.png'
                                )
                                self.tileTupleList[i] = (tile_rect,
                                                         "background.png")

                            # update the wood in player inventory
                            self.wood += 1
        self.mining_hitbox.center = (self.x, self.y)

    # if the tile above tile_rect is either stone, wood or a wall return
    def handle_tile_above(self, tile_rect):

        # coordinates of the tile directly above
        ab_tile_x = tile_rect.x
        ab_tile_y = tile_rect.y - tile_rect.height

        for j, (ab_tile_rect, ab_tile_name) in enumerate(self.tileTupleList):
            if ab_tile_rect.collidepoint(ab_tile_x, ab_tile_y):
                if ab_tile_name == "stone.png":

                    return "stone"

                elif ab_tile_name == "wood.png":

                    return "wood"

                elif ab_tile_name == "wall.png":

                    return "wall"

                break

    # if the tile above tile_rect is either stone, wood or a wall return
    def handle_tile_below(self, tile_rect):

        # coordinates of the tile directly above
        bl_tile_x = tile_rect.x
        bl_tile_y = tile_rect.y + tile_rect.height

        for j, (bl_tile_rect, bl_tile_name) in enumerate(self.tileTupleList):
            if bl_tile_rect.collidepoint(bl_tile_x, bl_tile_y):
                if bl_tile_name == "stone_wall.png":
                    self.game.map.update_tile(
                                    bl_tile_x - self.game.offset_x,
                                    bl_tile_y - self.game.offset_y,
                                    'background.png'
                                            )
                    self.tileTupleList[j] = (bl_tile_rect,
                                             "background.png")

                elif bl_tile_name == "wood_wall.png":
                    self.game.map.update_tile(
                                    bl_tile_x - self.game.offset_x,
                                    bl_tile_y - self.game.offset_y,
                                    'background.png'
                                            )
                    self.tileTupleList[j] = (bl_tile_rect,
                                             "background.png")
                break

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

    # display the health bar depending on the health (healing) of the player
    def draw_health_bar(self, player_x, player_y, surface):

        if self.healing > 0:
            image = pygame.image.load('assets/health_bar.png')
            surface.blit(image, (player_x - 2 - image.get_width() // 2,
                                 player_y - 30 - image.get_height() // 2))
