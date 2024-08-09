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

    def update_weapon(self):
        for x in range(len(self.bullets)):
            self.bullets[x-1].updateBullet()
            if not self.bullets[x-1].valid:
                self.bullets.pop(x-1)
                break

    def add_bullet(self, bullet_x, bullet_y, dir_x, dir_y, bullet_destination):
        self.bullets.append(bullet.Arrow(
            bullet_x, bullet_y, (dir_x, dir_y), bullet_destination))

    def draw_weapon(self, player_x, player_y, dir_x, dir_y, surface):
        bullet_destination = (player_x - dir_x, player_y - dir_y)
        self.angle = 360 - math.atan2(dir_y, dir_x)
        for x in range(len(self.bullets)):
            self.bullets[x-1].drawBullet(surface, self.angle)

        if pygame.mouse.get_pressed()[0]:
            bullet_x = player_x
            bullet_y = player_y
            self.add_bullet(
                bullet_x, bullet_y, dir_x, dir_y, bullet_destination)

        dir_len = math.sqrt((dir_x ** 2) + (dir_y ** 2))
        n_dir_x = dir_x / dir_len
        n_dir_y = dir_y / dir_len

        self.start = ((player_x - (n_dir_x * 50)),
                      (player_y - (n_dir_y * 50)))

        image = self.image.copy()
        image = pygame.transform.rotozoom(
                image, 180 + math.degrees(self.angle + 2.8),
                1).convert_alpha()
        surface.blit(image, (self.start[0] - image.get_width() // 2,
                             self.start[1] - image.get_height() // 2))


class Bow(Firearm):
    pass
    image = pygame.image.load('assets/bow.png')
    image = pygame.transform.scale(image, (30, 30))
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
    def __init__(self):
        super().__init__()
        self.distance = 10
        self.in_use = False
        self.start = (0, 0)
        self.angle = 45
        self.hitting_angle = math.radians(0)
        self.image = pygame.image.load('assets/robot.png')
        self.length = 0
        self.swordpoint = (0, 0)
        self.force = 1  # Default force, can be overridden by subclasses

    def update_weapon(self):
        if self.in_use:
            self.angle += self.hitting_angle
            self.hitting_angle += math.radians(15)
            if self.hitting_angle >= math.radians(45):
                self.in_use = False
                self.hitting_angle = 0

    def draw_weapon(self, player_x, player_y, dir_x, dir_y, surface):
        # normalize direction
        dir_len = math.sqrt((dir_x ** 2) + (dir_y ** 2))
        n_dir_x = dir_x / dir_len
        n_dir_y = dir_y / dir_len

        if not self.in_use:
            self.start = ((player_x - (n_dir_x * 50)),
                          (player_y - (n_dir_y * 50)))

            self.angle = 360 - math.atan2(dir_y, dir_x)

        if pygame.mouse.get_pressed()[0]:
            self.in_use = True
        image = self.image.copy()
        image = pygame.transform.rotozoom(
            image, 180 + math.degrees(self.angle + math.degrees(5)),
            1).convert_alpha()
        self.swordpoint = (player_x - n_dir_x*self.length,
                           player_y - n_dir_y*self.length)
        pygame.draw.circle(surface, "black",
                           self.swordpoint, 4)
        surface.blit(image, (self.start[0] - image.get_width() // 2,
                             self.start[1] - image.get_height() // 2))


class Knife(Cutting_Weapon):
    def __init__(self):
        super().__init__()  # Call the base class constructor
        self.kind = "Knife"
        self.image = pygame.image.load('assets/knife.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.length = 40
        self.force = 1


class Sword(Cutting_Weapon):
    def __init__(self):
        super().__init__()  # Call the base class constructor
        self.kind = "Sword"
        self.image = pygame.image.load('assets/sword.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.length = 64
        self.force = 5  # Set specific force for Sword


class Longsword(Cutting_Weapon):
    def __init__(self):
        super().__init__()  # Call the base class constructor
        self.kind = "Longsword"
        self.image = pygame.image.load('assets/Longsword2.png')
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.length = 128
        self.force = 8  # Set specific force for Longsword


class Lasersword(Cutting_Weapon):
    def __init__(self):
        super().__init__()  # Call the base class constructor
        self.kind = "Lasersword"
        self.image = pygame.image.load('assets/laserSword.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.length = 60
        self.force = 10  # Set specific force for Lasersword


class DefaultWeapon(Cutting_Weapon):
    pass
    kind = "DefaultWeapon"
