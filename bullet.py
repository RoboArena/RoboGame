import pygame
import math


class Bullet:
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


class Arrow(Bullet):
    pass

    def drawBullet(self, surface, angle):
        arrow = pygame.image.load('assets/arrow.png')
        arrow = pygame.transform.scale(arrow, (24, 24))
        arrow = pygame.transform.rotozoom(
                arrow, 180 + math.degrees(angle + 2.8),
                1).convert_alpha()
        surface.blit(arrow, (self.x, self.y))


class Gunbullet(Bullet):
    pass

    def drawBullet(self, surface):
        g_bullet = pygame.image.load('assets/bullet.png')
        g_bullet = pygame.transform.scale(g_bullet, (16, 16))
        surface.blit(g_bullet, (self.x, self.y))


class Rifflebullet(Bullet):
    pass

    def drawBullet(self, surface):
        g_bullet = pygame.image.load('assets/bullet.png')
        g_bullet = pygame.transform.scale(g_bullet, (8, 8))
        surface.blit(g_bullet, (self.x, self.y))
