import pygame
from network import Network
from player import Player
import main


class Client:

    def __init__(self):
        self.game = main.Game()
        self.window = self.game.window
        self.main()

    def main(self):
        running = True
        network = Network()
        startPos = network.get_pos() # Get the starting position for the Players from the server
        while running:
            if self.game.status == 0:
                self.game.main_menu()
            elif self.game.status == 1:
                self.game.play()
            elif self.game.status == 2:
                self.game.options()


client = Client()
