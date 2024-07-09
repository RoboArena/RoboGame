import pygame


class Button:
    def __init__(self, image, pos, text_input,
                 font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and \
           position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and \
           position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input,
                                         True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input,
                                         True, self.base_color)

    def displayButton(self, window):
        window.blit(self.image, self.rect)

    # repetition, delete later
    def get_font(size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)

    def displayInfoRect(self, fontSize, text, pos, align='center'):
        info_font = get_font(fontSize)
        info_text = info_font.render(text, True, "White")
        info_rect = info_text.get_rect()

        if align == 'center':
            info_rect.center = pos
        elif align == 'topleft':
            info_rect.topleft = pos
        elif align == 'topright':
            info_rect.topright = pos

    def displayWeaponButton(self, window, weapon): #nur display button nehmen?
        self.displayInfoRect(35, str(weapon.wood_cost) + str(weapon.stone_cost) + str(weapon.kind),
                                 (50, 100), 'topleft')