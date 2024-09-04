import pygame
import sys


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


pygame.init()

clock = pygame.time.Clock()

# Get the current display information
display_info = pygame.display.Info()
window_width = display_info.current_w
window_height = display_info.current_h

# it will display on screen
window = pygame.display.set_mode((window_width, window_height))

# set font
font = get_font(75)
user_text = ''

# create rectangle
input_rect = pygame.Rect(window_width/2, window_height/2, 140, 70)

# color_active stores color which
# gets active when input box is clicked by user
color_active = pygame.Color('White')

# color_passive store color which is
# color of input box.
color_passive = pygame.Color('#d7fcd4')
color = color_passive

active = False

while True:
    for event in pygame.event.get():
        # if user types QUIT then the screen will close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            # Check for backspace
            if event.key == pygame.K_BACKSPACE:

                # get text input from 0 to -1 i.e. end.
                user_text = user_text[:-1]
            # Unicode standard is used for string
            # formation
            else:
                user_text += event.unicode

    # it will set background color of screen
    window.fill("#252525")

    if active:
        color = color_active
    else:
        color = color_passive

    # draw rectangle and argument passed which should
    # be on screen
    pygame.draw.rect(window, color, input_rect)

    text_surface = font.render(user_text, True, "#b68f40")

    # render at position stated in arguments
    window.blit(text_surface, (input_rect.x+5, input_rect.y+5))

    # set width of textfield so that text cannot get
    # outside of user's text input
    input_rect.w = max(100, text_surface.get_width()+10)

    # display.flip() will update only a portion of the
    # screen to updated, not full area
    pygame.display.flip()

    # clock.tick(60) means that for every second at most
    # 60 frames should be passed.
    clock.tick(60)
