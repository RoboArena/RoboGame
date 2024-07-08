import pygame
import math


class Bullet:
    image = 'assets/robot.png'
    angle = 0
    scale = (24, 24)

    def __init__(self, x, y, dir, destination):
        self.x = x
        self.y = y
        self.dir = dir
        self.destination = destination
        self.valid = True
        self.x_is_bigger = self.x > self.destination[0]
        self.y_is_bigger = self.y >= self.destination[1]
        self.distance = math.sqrt((self.x - self.destination[0]) ** 2 +
                                  (self.y - self.destination[1]) ** 2)

    def updateBullet(self):
        self.x -= self.dir[0] * 30 / self.distance
        self.y -= self.dir[1] * 30 / self.distance
        if (
            (self.x_is_bigger and self.x <= self.destination[0]) or
            (not self.x_is_bigger and self.x >= self.destination[0]) or
            (self.y_is_bigger and self.y <= self.destination[1]) or
            (not self.y_is_bigger and self.y >= self.destination[1])
        ):
            self.valid = False

    def drawBullet(self, surface, angle):
        image_l = pygame.image.load(self.image)
        image_l = pygame.transform.scale(image_l, (self.scale))
        image_l = pygame.transform.rotozoom(
                image_l, 180 + math.degrees(angle + 2.8),
                1).convert_alpha()
        surface.blit(image_l, (self.x, self.y))


class Arrow(Bullet):
    pass
    image = 'assets/arrow.png'
    scale = (24, 24)


class Gunbullet(Bullet):
    pass
    image = 'assets/bullet.png'
    scale = (16, 16)


class Rifflebullet(Bullet):
    pass
    image = 'assets/bullet.png'
    scale = (8, 8)
