import pygame,sys 
import player
from spritesheet import Spritesheet
from tiles import TileMap
from button import Button

def get_font(size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)

class Game:
    

    def __init__(self) -> None:
        pygame.init()
        self.window_witdh = 1000
        self.window_height = 1000
        self.canvas = pygame.Surface((self.window_witdh,
                                      self.window_height))
        self.window = pygame.display.set_mode((self.window_witdh,
                                               self.window_height))
        
        # Background image:
        # self.BG = pygame.image.load("assets/Background.png")
        spritesheet = Spritesheet('Tiles50.png')
        self.map = TileMap('RoboArena.csv', spritesheet)
        self.clock = pygame.time.Clock()
        self.player = player.Player(self, 500, 500)
        self.main_menu()
    
    def main_menu(self):
        while True:
            #We could use a background image here:
            #self.window.blit(self.BG, (0, 0))

            # Fills the entire screen with dark grey
            self.window.fill((25, 25, 25))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(500, 150))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(500, 350), 
                                text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(500, 500), 
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(500, 650), 
                                text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.window.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.window)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
    
    def options(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.window.fill("white")

            OPTIONS_TEXT = get_font(45).render("OPTIONS screen.", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(500, 260))
            self.window.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_BACK = Button(image=None, pos=(500, 460), 
                                text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                    running = False

            self.delta_time = self.clock.tick(60)/1000

            # Fills the entire screen with dark grey
            self.canvas.fill((25, 25, 25))

            # draw the tilemap
            self.map.draw_map(self.canvas)

            # draw the player
            self.player.update()
            self.player.draw()

            # display the canvas on the window
            self.window.blit(self.canvas, (0, 0))

            pygame.display.update()

        


game = Game()
