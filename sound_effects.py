import pygame

pygame.mixer.init()

take_damage = pygame.mixer.Sound('sounds/take_damage.wav')

# sword draw I used for testing, but it could potentially be used anyway
sword_draw = pygame.mixer.Sound('sounds/drawsword.mp3')

sword_equip = pygame.mixer.Sound('sounds/sword_equip.wav')
long_sword_equip = pygame.mixer.Sound('sounds/long_sword_equip.wav')
lasersword_equip = pygame.mixer.Sound('sounds/lasersword_equip.wav')

button_main = pygame.mixer.Sound('sounds/button_main.wav')
options_menu_button = pygame.mixer.Sound('sounds/options_menu_buttons.wav')

pickaxe_break = pygame.mixer.Sound('sounds/pickaxe_break.wav')

handgun_equip = pygame.mixer.Sound('sounds/handgun_equip.wav')
handgun_shoot = pygame.mixer.Sound('sounds/rifle.wav')

rifle_equip = pygame.mixer.Sound('sounds/rifle_equip.wav')
rifle_shoot = pygame.mixer.Sound('sounds/gun.wav')

bow_equip = pygame.mixer.Sound('sounds/bow_equip.wav')
bow_shoot = pygame.mixer.Sound('sounds/bow_shoot.wav')

upgrade_healing_speed = pygame.mixer.Sound('sounds/upgrade_healing.wav')

# se.sword_draw.play()
