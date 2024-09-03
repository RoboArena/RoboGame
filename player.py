import pygame
import bullet
import random
import time
from spritesheet import Spritesheet
from tiles import TileMap
import sound_effects


class Player:
    def __init__(self, game, x, y, energy, wood, stone,
                 speed, healing, points, weapon, keymode):
        self.x = x
        self.y = y
        self.energy = energy
        self.wood = wood
        self.stone = stone
        self.speed = speed
        self.healing = healing
        self.points = points
        self.dir = (90, 90)
        self.game = game
        self.surface = game.canvas
        # image is the right looking robot, image2 looks left
        self.image = pygame.image.load('assets/robot.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image = pygame.image.load('assets/robot.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image2 = pygame.image.load(
                                       'assets/robot_flip.png'
                                       ).convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, (40, 40))
        self.image3 = pygame.image.load('battery.png').convert_alpha()
        self.weapon = weapon
        self.keymode = keymode

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

        # To track previous mouse clicks of left mouse button
        self.previous_mouse_state = pygame.mouse.get_pressed()[0]

        # Right mouse button tracking for mining_timer
        self.rmb_pressed = False
        self.rmb_press_start_time = 0

        # is the player currently in a puddle? used for get_puddle_collisions
        self.in_puddle = False

        # Get the current display information
        display_info = pygame.display.Info()
        self.window_width = display_info.current_w
        self.window_height = display_info.current_h

        # Update the canvas and window to use the display size
        self.canvas = pygame.Surface((self.window_width, self.window_height))
        self.window = pygame.display.set_mode((self.window_width,
                                               self.window_height))

        # Load in the Spritesheet and the Tilemap
        spritesheet = Spritesheet('assets/Tiles.png')
        self.map = TileMap('RoboArena.csv', spritesheet)

        # Calculate the offsets to center the map
        self.offset_x = (self.window_width - self.map.map_w) // 2
        self.offset_y = (self.window_height - self.map.map_h) // 2

        # Initialize the class attribute last_called_time
        self.last_called_time = None

        self.battery_hitbox = pygame.Rect(0, 0, 40, 40)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.dir = (self.x - mouse_pos[0], self.y - mouse_pos[1])

        if (self.in_puddle):
            self.movement(100)
        else:
            self.movement(250)

        self.weapon.update_weapon()
        self.draw()
        # update the currently mineable tiles
        self.get_hits_mining(self.game.map.tiles)
        # save the previous mouse click so that you can't hold left mouse click
        # to mine stone/wood but have to click each time, this is not in
        # effect now to try out another technique for mining
        self.previous_mouse_state = pygame.mouse.get_pressed()[0]

        # display and handle picking up batteries
        global battery_xy
        if (self.timer_function() or self.rect.colliderect(
                                                         self.battery_hitbox)):
            self.energy += 40
            sound_effects.upgrade_healing_speed.play()
            # generating hitbox for battery
            battery_xy = self.generate_random_location_on_map(self.surface)
            self.battery_hitbox = pygame.Rect(battery_xy[0],
                                              battery_xy[1], 40, 40)
            while (self.is_battery_in_wall(self.battery_hitbox)):
                # generating hitbox for battery
                battery_xy = self.generate_random_location_on_map(self.surface)
                self.battery_hitbox = pygame.Rect(battery_xy[0],
                                                  battery_xy[1], 40, 40)
        elif battery_xy is not None:
            # display the battery to the surface
            self.blit_battery_onto_surface(battery_xy[0],
                                           battery_xy[1], self.surface)

        # update Right mouse button press tracking
        self.mining_timer()

    def draw(self):
        # make Hitbox visible
        pygame.draw.rect(self.surface, "black", self.rect)
        # draw mining hitbox (for debugging)
        pygame.draw.rect(self.surface, "red", self.mining_hitbox, 2)
        # (1) The player is a blue circle
        # pygame.draw.circle(self.surface, "blue", (self.x, self.y), self.r)
        # (2) The player is a robot

        # display the robot image, depending on the player looking right
        # or left
        if (self.robot_looking_right()):
            self.surface.blit(self.image,
                              (self.x - self.image.get_width() // 2,
                               self.y - self.image.get_height() // 2))
        else:
            self.surface.blit(self.image2,
                              (self.x - self.image2.get_width() // 2,
                               self.y - self.image2.get_height() // 2))
        # draw the weapon
        self.weapon.draw_weapon(
            self.x, self.y, self.dir[0], self.dir[1], self.surface)
        # draw the healthbar
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
        l_pressed = False
        r_pressed = False
        u_pressed = False
        d_pressed = False
        if self.keymode == "wasd":
            left = pygame.K_a
            right = pygame.K_d
            up = pygame.K_w
            down = pygame.K_s
        else:
            left = pygame.K_LEFT
            right = pygame.K_RIGHT
            up = pygame.K_UP
            down = pygame.K_DOWN
        if keys[left]:
            dx -= speed * self.game.delta_time
            l_pressed = True
        if keys[right]:
            dx += speed * self.game.delta_time
            r_pressed = True
        if keys[up]:
            dy -= speed * self.game.delta_time
            u_pressed = True
        if keys[down]:
            dy += speed * self.game.delta_time
            d_pressed = True

        # Aufteilen der Bewegung in kleinere Schritte
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            return

        dx /= steps
        dy /= steps

        for _ in range(int(steps)):
            if dx != 0:
                self.x += dx
                self.checkCollisionsx(l_pressed, r_pressed)
            if dy != 0:
                self.y += dy
                self.checkCollisionsy(u_pressed, d_pressed)
            self.in_puddle = False
            self.get_puddle_collisions()

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
                                     "wood_wall.png",
                                     "toxic_puddle_1.png",
                                     "toxic_puddle_2.png",
                                     "toxic_puddle_3.png",
                                     "toxic_puddle_4.png",
                                     "toxic_puddle_5.png",
                                     "toxic_puddle_6.png",
                                     "toxic_puddle_7.png",
                                     "toxic_puddle_8.png",
                                     "toxic_puddle_9.png",
                                     "toxic_puddle_10.png",
                                     "toxic_puddle_11.png",
                                     "toxic_puddle_12.png",]:
                    hits.append(tile_rect)
        return hits

    def checkCollisionsx(self, l_pressed, r_pressed):
        self.rect.center = (self.x, self.y)  # Update the Hitbox Position
        collisions = self.get_collisions()
        for tile_rect in collisions:
            if l_pressed:
                self.x = tile_rect.right + self.rect.width // 2
            if r_pressed:
                self.x = tile_rect.left - self.rect.width // 2
        self.rect.center = (self.x, self.y)  # Update the Hitbox Position

    def checkCollisionsy(self, u_pressed, d_pressed):
        self.rect.center = (self.x, self.y)  # Update the Hitbox Position
        self.rect.bottom += 1
        self.rect.top -= 1
        collisions = self.get_collisions()
        for tile_rect in collisions:
            if u_pressed:
                self.y = tile_rect.bottom + self.rect.height // 2
            if d_pressed:
                self.y = tile_rect.top - self.rect.height // 2
        self.rect.center = (self.x, self.y)  # Update the Hitbox Position

    # check if the mining_hitbox collides with wood/stone tiles.
    # If a collision happens and the player is clicking
    # on the colliding tile (stone or wood) it will be mined and the resource
    # is added to the players inventory
    def get_hits_mining(self, tiles):
        self.mining_hitbox.center = (self.x, self.y)
        mouse_pos = pygame.mouse.get_pos()
        for i, (tile_rect, tile_name) in enumerate(self.tileTupleList):
            # This is a simple optimization to only check for nearby tiles
            if (abs(self.x - tile_rect.x) > 300 or
                    abs(self.y - tile_rect.y) > 300):
                continue
            if self.mining_hitbox.colliderect(tile_rect):
                # checks if the player aims at a tile and also presses
                # the left mouse button
                if (self.aiming_at_tile(tile_rect, mouse_pos) and
                        pygame.mouse.get_pressed()[2]):
                    if self.mining_timer():

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

                                sound_effects.pickaxe_break.play()
                            else:
                                self.game.map.update_tile(
                                    tile_rect.x - self.game.offset_x,
                                    tile_rect.y - self.game.offset_y,
                                    'background.png'
                                )
                                self.tileTupleList[i] = (tile_rect,
                                                         "background.png")

                                sound_effects.pickaxe_break.play()

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

                                sound_effects.pickaxe_break.play()

                            elif (self.handle_tile_above(tile_rect) == "wall"):
                                self.game.map.update_tile(
                                    tile_rect.x - self.game.offset_x,
                                    tile_rect.y - self.game.offset_y,
                                    'wall_edge.png'
                                )
                                self.tileTupleList[i] = (tile_rect,
                                                         "edge_wall.png")

                                sound_effects.pickaxe_break.play()

                            else:
                                self.game.map.update_tile(
                                    tile_rect.x - self.game.offset_x,
                                    tile_rect.y - self.game.offset_y,
                                    'background.png'
                                )
                                self.tileTupleList[i] = (tile_rect,
                                                         "background.png")

                                sound_effects.pickaxe_break.play()

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

    # Check if Right mouse button has been held for 1 second,
    # if so, return true (rmb = right mouse button)
    def mining_timer(self):

        if pygame.mouse.get_pressed()[2]:
            if not self.rmb_press:
                self.rmb_press = True
                self.rmb_press_start_time = pygame.time.get_ticks()
            else:
                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - self.rmb_press_start_time

                # all things considered this tests for roughly a second of
                # holding RMB even though it tests for ">= 700ms"
                if elapsed_time >= 700:
                    elapsed_time = current_time - self.rmb_press_start_time
                    self.rmb_press = False
                    return True
        else:
            self.rmb_press = False
            self.rmb_press_start_time = 0
        return False

    # display the health bar depending on the health (energy) of the player
    def draw_health_bar(self, player_x, player_y, surface):

        if self.energy > 80:
            image = pygame.image.load('assets/health_bar.png')
            surface.blit(image, (player_x - 2 - image.get_width() // 2,
                                 player_y - 30 - image.get_height() // 2))
        elif self.energy > 60:
            image = pygame.image.load('assets/health_bar_80.png')
            surface.blit(image, (player_x - 2 - image.get_width() // 2,
                                 player_y - 30 - image.get_height() // 2))
        elif self.energy > 40:
            image = pygame.image.load('assets/health_bar_60.png')
            surface.blit(image, (player_x - 2 - image.get_width() // 2,
                                 player_y - 30 - image.get_height() // 2))
        elif self.energy > 20:
            image = pygame.image.load('assets/health_bar_40.png')
            surface.blit(image, (player_x - 2 - image.get_width() // 2,
                                 player_y - 30 - image.get_height() // 2))
        elif self.energy > 0:
            image = pygame.image.load('assets/health_bar_20.png')
            surface.blit(image, (player_x - 2 - image.get_width() // 2,
                                 player_y - 30 - image.get_height() // 2))
        elif self.energy == 0:
            image = pygame.image.load('assets/health_bar_0.png')
            surface.blit(image, (player_x - 2 - image.get_width() // 2,
                                 player_y - 30 - image.get_height() // 2))
        elif self.energy < 0:
            image = pygame.image.load('assets/health_bar_0.png')
            surface.blit(image, (player_x - 2 - image.get_width() // 2,
                                 player_y - 30 - image.get_height() // 2))

    # get collisions with puddle tiles and return True if the player is
    # colliding with a puddle tile and also reduce energy
    def get_puddle_collisions(self):
        hits = []
        for tile_rect, tile_name in self.tileTupleList:
            # This is a simple optimization to only check for nearby tiles
            if (abs(self.x - tile_rect.x) > 300 or
                    abs(self.y - tile_rect.y) > 300):
                continue
            if self.rect.colliderect(tile_rect):
                if tile_name in ["toxic_puddle_1.png",
                                 "toxic_puddle_2.png",
                                 "toxic_puddle_3.png",
                                 "toxic_puddle_4.png",]:
                    self.in_puddle = True
                    # self.energy = self.energy - 2 # for testing damage

        return hits

    # is the player looking left or right?
    def robot_looking_right(self):
        mouse_pos = pygame.mouse.get_pos()
        # if the x axis value of the mouse cursor is bigger than the players
        # x-coordinate then the player is looking to the right - return True
        # otherwise return False
        if mouse_pos[0] > self.x:
            return True
        else:
            return False

    # generate coordinates for the battery
    def generate_random_location_on_map(self, surface):

        random_x = random.randint(0, 928)
        random_y = random.randint(0, 480)
        surface.blit(self.image3,
                     (random_x + self.offset_x + 32,
                      random_y + self.offset_y + 32))
        # print(self.offset_x)
        # print(self.offset_y)

        return (random_x + self.offset_x + 32,
                random_y + self.offset_y + 32)

    # is the battery not in the background tile? if so return true
    def is_battery_in_wall(self, battery):
        for tile_rect, tile_name in self.tileTupleList:
            # This is a simple optimization to only check for nearby tiles
            # if (abs(self.x - tile_rect.x) > 300 or
            #        abs(self.y - tile_rect.y) > 300):
            #   continue
            if battery.colliderect(tile_rect):
                if tile_name not in ["background.png"]:
                    return True
                else:
                    return False

    # blit the battery on to self.surface
    def blit_battery_onto_surface(self, x, y, surface):
        surface.blit(self.image3,
                     (x, y))
        return

    # 200 second timer, returns True every 200 seconds when called
    # the duration can be adapted so the battery despawns and spawns randomly
    # on its own
    def timer_function(self):

        current_time = time.time()

        if self.last_called_time is None:
            # First time the function is called, so initialize last_called_time
            self.last_called_time = current_time
            return True

        # Check if 200 seconds have passed since the last call
        if current_time - self.last_called_time >= 200:
            self.last_called_time = current_time
            return True
        else:
            # print("printed false")
            return False
