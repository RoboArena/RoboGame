
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
        self.tile_size = 32
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.tile_names = self.create_tile_names()  # added
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()
        self.tile_grid = self.create_tile_grid()

    # creates a tile_grid of all the tiles so that updating a tile
    # at a given position of the tilemap is easier to do
    def create_tile_grid(self):
        grid = []
        for row in range(self.map_h // self.tile_size):
            grid.append([None] * (self.map_w // self.tile_size))
        for tile in self.tiles:
            grid[tile.rect.y // self.tile_size][tile.rect.x //
                                                self.tile_size] = tile
        return grid

    # Creates a dictionary to store tile names by their coordinates
    def create_tile_names(self):
        names = {}
        for tile in self.tiles:
            names[(tile.rect.x, tile.rect.y)] = tile.tileName
        return names

    # update_tiles overrides a tile at x,y with a new tile new_tile
    def update_tile(self, x, y, new_tile_name):
        # adapt the tile coordinates to conform to the grid coordinates
        grid_x = x // self.tile_size
        grid_y = y // self.tile_size
        # check if grid coordinates are within grid coordinates to avoid bugs
        if (0 <= grid_x < len(self.tile_grid[0])) and \
                (0 <= grid_y < len(self.tile_grid)):
            # instantiate new tile
            new_tile = Tile(
                new_tile_name, grid_x * self.tile_size,
                grid_y * self.tile_size, self.spritesheet
                )
            # replace previous tile in grid with new tile
            self.tile_grid[grid_y][grid_x] = new_tile
            # refresh tile list of tiles in grid
            self.tiles = [tile for row in self.tile_grid
                          for tile in row if tile is not None]
            self.tile_names[(grid_x * self.tile_size,
                             grid_y * self.tile_size)] = new_tile_name
            # redraw the map
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
                    tiles.append(Tile('wall.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                elif tile == '1':
                    tiles.append(Tile('material.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                elif tile == '2':
                    tiles.append(Tile('stone.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                elif tile == '3':
                    tiles.append(Tile('background.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                elif tile == '4':
                    tiles.append(Tile('toxic_puddle.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                elif tile == '5':
                    tiles.append(Tile('wood.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                elif tile == '6':
                    tiles.append(Tile('wall_edge.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                elif tile == '7':
                    tiles.append(Tile('stone_wall.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                elif tile == '8':
                    tiles.append(Tile('wood_wall.png', x * self.tile_size,
                                      y * self.tile_size, self.spritesheet))
                x += 1
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
