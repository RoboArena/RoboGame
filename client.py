import pygame
from network import Network
from player import Player
import main


class Client:

    def __init__(self):
        self.main()

    def read_pos(self, pos_str):
        try:
            pos = pos_str.split(",")
            if len(pos) < 2:
                raise ValueError("Received incomplete position data")
            return float(pos[0]), float(pos[1])  # Parse as floats
        except ValueError as e:
            print(f"Error parsing position: {e}")
            return 0.0, 0.0  # Return a default position or handle accordingly

    def make_pos(self, tup):
        return str(tup[0]) + "," + str(tup[1])

    def main(self):
        running = True
        network = Network()
        startPos = self.read_pos(network.get_pos())  # Get the starting position for the Players from the server
        self.game = main.Game(start_pos=startPos)  # Create the game object
        self.window = self.game.window
        
        while running:
            if self.game.status == 0:
                self.game.main_menu()
            elif self.game.status == 1:
                self.game.play()
                p2_pos = self.read_pos(network.send(self.make_pos((self.game.player.x, self.game.player.y))))
                self.game.player2.x = p2_pos[0]
                self.game.player2.y = p2_pos[1]
                
            elif self.game.status == 2:
                self.game.options()


client = Client()
