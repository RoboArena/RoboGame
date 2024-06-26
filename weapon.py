import pygame
import bullet
import math


class Weapon:
    kind = "weapon"

    def __init__(self):
        self.force = 1
        self.distance = 1000


class Firearm(Weapon):
    pass
    bullets = []

    def update_weapon(self):
        for x in range(len(self.bullets)):
            self.bullets[x-1].updateBullet()
            if not self.bullets[x-1].valid:
                self.bullets.pop(x-1)
                break


class Gun(Firearm):
    pass

    def draw_weapon(self, player_x, player_y, dir_x, dir_y, surface):
        bullet_destination = (player_x - dir_x, player_y - dir_y)
        for x in range(len(self.bullets)):
            self.bullets[x-1].drawBullet(surface)

        if pygame.mouse.get_pressed()[0]:
            bullet_x = player_x
            bullet_y = player_y
            self.bullets.append(bullet.Gunbullet(
                 bullet_x, bullet_y, (dir_x, dir_y), bullet_destination))


class Lasergun(Firearm):
    pass
    # this is mostly the same as above. Maybe fixable?

    def draw_weapon(self, player_x, player_y, dir_x, dir_y, surface):
        bullet_destination = (player_x - dir_x, player_y - dir_y)
        for x in range(len(self.bullets)):
            self.bullets[x-1].drawBullet(surface)

        if pygame.mouse.get_pressed()[0]:
            bullet_x = player_x
            bullet_y = player_y
            self.bullets.append(bullet.Laserbullet(
                 bullet_x, bullet_y, (dir_x, dir_y), bullet_destination))


class Cutting_Weapon(Weapon):
    pass
    distance = 10
    in_use = False
    start = 0
    angle = 45
    hitting_angle = math.radians(0)
    image = pygame.image.load('assets/robot.png')

    def update_weapon(self):
        if self.in_use:
            self.angle += self.hitting_angle
            self.hitting_angle += math.radians(15)
            if self.hitting_angle >= math.radians(45):
                self.in_use = False
                self.hitting_angle = 0

    def draw_weapon(self, player_x, player_y, dir_x, dir_y, surface):
        if not self.in_use:
            # normalize direction
            dir_len = math.sqrt((dir_x ** 2) + (dir_y ** 2))
            n_dir_x = dir_x / dir_len
            n_dir_y = dir_y / dir_len

            self.start = ((player_x - (n_dir_x * 50)),
                          (player_y - (n_dir_y * 50)))

            self.angle = 360 - math.atan2(dir_y, dir_x)

        if pygame.mouse.get_pressed()[0]:
            self.in_use = True
        image = self.image.copy()
        image = pygame.transform.scale(image, (50, 50))
        image = pygame.transform.rotozoom(
            image, 180 + math.degrees(self.angle + math.degrees(5)),
            1).convert_alpha()
        surface.blit(image, (self.start[0] - image.get_width() // 2,
                             self.start[1] - image.get_height() // 2))


class Knife(Cutting_Weapon):  # keep this in? Maybe better sword as default?
    pass
    kind = "Knife"
    image = pygame.image.load('assets/knife.png')


class Sword(Cutting_Weapon):
    pass
    kind = "Sword"
    image = pygame.image.load('assets/sword.png')


class Longsword(Cutting_Weapon):
    pass
    kind = "Longsword"
    image = pygame.image.load('assets/longSword.png')


class Lasersword(Cutting_Weapon):
    pass
    kind = "Lasersword"
    image = pygame.image.load('assets/laserSword.png')
