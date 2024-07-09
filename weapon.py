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
    kind = "weapon"
    image = pygame.image.load('assets/robot.png')

    # below is only for generating the mining animation and pickaxe image
    pickaxe_image = pygame.image.load('assets/pickaxe.png')
    distance = 10
    in_use = False
    start = 0
    angle = 45
    hitting_angle = math.radians(0)

    def update_weapon(self):
        # for the mining animation
        if self.in_use:
            self.angle += self.hitting_angle
            self.hitting_angle += math.radians(15)
            if self.hitting_angle >= math.radians(45):
                self.in_use = False
                self.hitting_angle = 0

        for x in range(len(self.bullets)):
            self.bullets[x-1].updateBullet()
            if not self.bullets[x-1].valid:
                self.bullets.pop(x-1)
                break

    def add_bullet(self, bullet_x, bullet_y, dir_x, dir_y, bullet_destination):
        self.bullets.append(bullet.Arrow(
            bullet_x, bullet_y, (dir_x, dir_y), bullet_destination))

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

            self.in_use = False
            for x in range(len(self.bullets)):
                self.bullets[x-1].drawBullet(surface, self.angle)
            bullet_destination = (player_x - dir_x, player_y - dir_y)
            bullet_x = player_x
            bullet_y = player_y
            self.add_bullet(
                bullet_x, bullet_y, dir_x, dir_y, bullet_destination)
            image = self.image.copy()

            dir_len = math.sqrt((dir_x ** 2) + (dir_y ** 2))
            n_dir_x = dir_x / dir_len
            n_dir_y = dir_y / dir_len

            self.start = ((player_x - (n_dir_x * 50)),
                          (player_y - (n_dir_y * 50)))
            image = pygame.transform.rotozoom(
                image, 180 + math.degrees(self.angle + 2.8),
                1).convert_alpha()

        # when the player hits the right mouse button display the pickaxe
        elif pygame.mouse.get_pressed()[2]:
            self.in_use = True
            image = self.pickaxe_image.copy()
            image = pygame.transform.rotozoom(
                image, 180 + math.degrees(self.angle + math.degrees(5)),
                1).convert_alpha()

        else:
            for x in range(len(self.bullets)):
                self.bullets[x-1].drawBullet(surface, self.angle)
            bullet_destination = (player_x - dir_x, player_y - dir_y)
            image = self.image.copy()
            dir_len = math.sqrt((dir_x ** 2) + (dir_y ** 2))
            n_dir_x = dir_x / dir_len
            n_dir_y = dir_y / dir_len

            self.start = ((player_x - (n_dir_x * 50)),
                          (player_y - (n_dir_y * 50)))
            image = pygame.transform.rotozoom(
                image, 180 + math.degrees(self.angle + 2.8),
                1).convert_alpha()

        surface.blit(image, (self.start[0] - image.get_width() // 2,
                             self.start[1] - image.get_height() // 2))


class Bow(Firearm):
    pass
    image = pygame.image.load('assets/bow.png')
    kind = "Bow"


class Gun(Firearm):
    pass
    image = pygame.image.load('assets/gun.png')
    kind = "Gun"

    def add_bullet(self, bullet_x, bullet_y, dir_x, dir_y, bullet_destination):
        self.bullets.append(bullet.Gunbullet(
            bullet_x, bullet_y, (dir_x, dir_y), bullet_destination))


class Rifle(Firearm):
    pass
    # this is mostly the same as above. Maybe fixable?
    image = pygame.image.load('assets/rifle2.png')
    kind = "Rifle"

    def add_bullet(self, bullet_x, bullet_y, dir_x, dir_y, bullet_destination):
        self.bullets.append(bullet.Rifflebullet(
            bullet_x, bullet_y, (dir_x, dir_y), bullet_destination))


class Cutting_Weapon(Weapon):
    # pass
    distance = 10
    in_use = False
    start = 0
    angle = 45
    hitting_angle = math.radians(0)
    image = pygame.image.load('assets/robot.png')
    pickaxe_image = pygame.image.load('assets/pickaxe.png')

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

        elif pygame.mouse.get_pressed()[2]:
            self.in_use = True
            image = self.pickaxe_image.copy()

        else:
            image = self.image.copy()

        image = pygame.transform.rotozoom(
            image, 180 + math.degrees(self.angle + math.degrees(5)),
            1).convert_alpha()

        surface.blit(image, (self.start[0] - image.get_width() // 2,
                             self.start[1] - image.get_height() // 2))


class Knife(Cutting_Weapon):
    pass
    kind = "Knife"
    image = pygame.image.load('assets/knife.png')
    image = pygame.transform.scale(image, (20, 20))


class Sword(Cutting_Weapon):
    pass
    kind = "Sword"
    image = pygame.image.load('assets/sword.png')
    image = pygame.transform.scale(image, (64, 64))


class Longsword(Cutting_Weapon):
    pass
    kind = "Longsword"
    image = pygame.image.load('assets/Longsword2.png')
    image = pygame.transform.scale(image, (128, 128))


class Lasersword(Cutting_Weapon):
    pass
    kind = "Lasersword"
    image = pygame.image.load('assets/laserSword.png')
    image = pygame.transform.scale(image, (40, 40))


class DefaultWeapon(Cutting_Weapon):
    pass
    kind = "DefaultWeapon"
