import pygame
import bullet
import math


class Weapon:
    kind = "weapon"
    pickaxe_image = pygame.image.load('assets/pickaxe.png')

    def __init__(self):
        self.force = 1
        self.distance = 1000

    def adjustImage(image, scale):
        im = pygame.image.load(image)
        im = pygame.transform.scale(im, (scale))
        return im

    def normalizeDir(dir):
        new_dir = []
        dir_len = math.sqrt((dir[0] ** 2) + (dir[1] ** 2))
        new_dir.append(dir[0] / dir_len)
        new_dir.append(dir[1] / dir_len)
        return new_dir

    def set_start(self, player_x, player_y, dir_x, dir_y):
        new_dir = Weapon.normalizeDir((dir_x, dir_y))
        self.start = ((player_x - (new_dir[0] * 50)),
                      (player_y - (new_dir[1] * 50)))

    def show_image(self, image, angle, surface):
        image = pygame.transform.rotozoom(
            image, 180 + math.degrees(self.angle + angle),
            1).convert_alpha()
        surface.blit(image, (self.start[0] - image.get_width() // 2,
                             self.start[1] - image.get_height() // 2))

    def draw_weapon(self, player_x, player_y, dir_x, dir_y, surface):
        if not self.in_use:

            Weapon.set_start(self, player_x, player_y, dir_x, dir_y)
            self.angle = 360 - math.atan2(dir_y, dir_x)

        if pygame.mouse.get_pressed()[0]:

            self.use_weapon(player_x, player_y, dir_x, dir_y, surface)

        elif pygame.mouse.get_pressed()[2]:
            self.in_use = True
            image = self.pickaxe_image.copy()
            Weapon.show_image(self, image, math.degrees(5), surface)

        else:
            self.not_use_weapon(player_x, player_y, dir_x, dir_y, surface)

    def update_weapon(self):
        if self.in_use:
            self.angle += self.hitting_angle
            self.hitting_angle += math.radians(15)
            if self.hitting_angle >= math.radians(45):
                self.in_use = False
                self.hitting_angle = 0
        else:
            self.update_bullets()


class Firearm(Weapon):
    pass
    bullets = []
    kind = "weapon"
    image = pygame.image.load('assets/robot.png')
    in_use = True
    start = 0
    angle = 45
    hitting_angle = math.radians(0)

    def update_bullets(self):
        for x in range(len(self.bullets)):
            self.bullets[x-1].updateBullet()
            if not self.bullets[x-1].valid:
                self.bullets.pop(x-1)
                break

    def add_bullet(self, bulletclass,
                   bullet_x, bullet_y, dir_x, dir_y, bullet_destination):
        self.bullets.append(bulletclass(
            bullet_x, bullet_y, (dir_x, dir_y), bullet_destination))

    def use_weapon(self, player_x, player_y, dir_x, dir_y, surface):
        self.in_use = False
        for x in range(len(self.bullets)):
            self.bullets[x-1].drawBullet(surface, self.angle)
        bullet_destination = (player_x - dir_x, player_y - dir_y)
        bullet_x = player_x
        bullet_y = player_y
        self.add_bullet(
            bullet_x, bullet_y, dir_x, dir_y, bullet_destination)
        image = self.image.copy()

        Weapon.set_start(self, player_x, player_y, dir_x, dir_y)
        Weapon.show_image(self, image, 2.8, surface)

    def not_use_weapon(self, player_x, player_y, dir_x, dir_y, surface):
        for x in range(len(self.bullets)):
            self.bullets[x-1].drawBullet(surface, self.angle)
        image = self.image.copy()
        Weapon.set_start(self, player_x, player_y, dir_x, dir_y)
        Weapon.show_image(self, image, 2.8, surface)


class Bow(Firearm):
    pass
    image = Weapon.adjustImage('assets/bow.png', (30, 30))
    kind = "Bow"
    wood_cost = 3
    stone_cost = 7

    def add_bullet(self, bullet_x, bullet_y, dir_x, dir_y, bullet_destination):
        Firearm.add_bullet(
            self, bullet.Arrow, bullet_x, bullet_y,
            dir_x, dir_y, bullet_destination)


class Gun(Firearm):
    pass
    image = Weapon.adjustImage('assets/gun.png', (30, 30))
    kind = "Gun"
    wood_cost = 9
    stone_cost = 6

    def add_bullet(self, bullet_x, bullet_y, dir_x, dir_y, bullet_destination):
        Firearm.add_bullet(
            self, bullet.Gunbullet, bullet_x, bullet_y,
            dir_x, dir_y, bullet_destination)


class Rifle(Firearm):
    pass
    image = Weapon.adjustImage('assets/rifle2.png', (50, 50))
    kind = "Rifle"
    wood_cost = 5
    stone_cost = 10

    def add_bullet(self, bullet_x, bullet_y, dir_x, dir_y, bullet_destination):
        Firearm.add_bullet(
            self, bullet.Rifflebullet, bullet_x, bullet_y,
            dir_x, dir_y, bullet_destination)


class Cutting_Weapon(Weapon):
    pass
    distance = 10
    in_use = False
    start = 0
    angle = 45
    hitting_angle = math.radians(0)
    image = pygame.image.load('assets/robot.png')

    def update_bullets(self):
        return

    def use_weapon(self, player_x, player_y, dir_x, dir_y, surface):
        self.in_use = True
        image = self.image.copy()
        Weapon.show_image(self, image, math.degrees(5), surface)

    def not_use_weapon(self, player_x, player_y, dir_x, dir_y, surface):
        image = self.image.copy()
        Weapon.show_image(self, image, math.degrees(5), surface)


class Knife(Cutting_Weapon):
    pass
    kind = "Knife"
    image = Weapon.adjustImage('assets/knife.png', (20, 20))


class Sword(Cutting_Weapon):
    pass
    kind = "Sword"
    image = Weapon.adjustImage('assets/sword.png', (30, 30))
    wood_cost = 6
    stone_cost = 4


class Longsword(Cutting_Weapon):
    pass
    kind = "Longsword"
    image = Weapon.adjustImage('assets/Longsword2.png', (128, 128))
    wood_cost = 7
    stone_cost = 8


class Lasersword(Cutting_Weapon):
    pass
    kind = "Lasersword"
    image = Weapon.adjustImage('assets/laserSword.png', (40, 40))
    wood_cost = 11
    stone_cost = 4


class DefaultWeapon(Cutting_Weapon):
    pass
    kind = "DefaultWeapon"
