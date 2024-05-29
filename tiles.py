import pygame
import csv
import os


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        self.tileName = image
        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface, offset_x=0, offset_y=0):
        surface.blit(self.image, (self.rect.x + offset_x,
                                  self.rect.y + offset_y))


class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface, offset_x=0, offset_y=0):
        for tile in self.tiles:
            tile.draw(surface, offset_x, offset_y)

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '-1':
                    self.start_x = x * self.tile_size,
                    self.start_y = y * self.tile_size
                elif tile == '0':
                    tiles.append(Tile('lightGrey.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                elif tile == '1':
                    tiles.append(Tile('blue.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                elif tile == '2':
                    tiles.append(Tile('black.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                elif tile == '3':
                    tiles.append(Tile('darkGrey.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                elif tile == '4':
                    tiles.append(Tile('green.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                elif tile == '5':
                    tiles.append(Tile('brown.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                x += 1
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
