import pygame
import sys


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


class Menu:
    def __init__(self, window, canvas, title, title_size,
                 title_pos, buttons, functions, title_color, bg_color):
        while True:
            canvas.fill(bg_color)

            MOUSE_POS = pygame.mouse.get_pos()

            TITLE_TEXT = get_font(title_size).render(title, True, title_color)
            TITLE_RECT = TITLE_TEXT.get_rect(center=title_pos)

            for b in buttons:
                b.changeColor(MOUSE_POS)
                b.update(canvas)

            canvas.blit(TITLE_TEXT, TITLE_RECT)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    i = -1
                    for b in buttons:
                        i += 1
                        if b.checkForInput(MOUSE_POS):
                            return functions[i]()
            window.blit(canvas, (0, 0))
            pygame.display.update()
