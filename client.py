from network import Network
import main
import pygame


class Client:

    def __init__(self):
        self.main()

    def main(self):
        running = True
        network = Network()
        self.p = network.get_p()
        self.PlayerRightMouse = False
        self.Player2RightMouse = False
        if self.p == 0:
            self.game = main.Game()  # Create the game object
        else:
            self.game = main.Game()
            changePlayer = self.game.player
            self.game.player = self.game.player2
            self.game.player2 = changePlayer

        while running:
            if self.game.status == 0:
                self.game.main_menu()
            elif self.game.status == 1:
                self.game.play()
                if pygame.mouse.get_pressed()[0]:
                    self.PlayerRightMouse = True
                else:
                    self.PlayerRightMouse = False
                self.update_game_state(network.send(self.get_game_state()))
            elif self.game.status == 2:
                self.game.options()

    def get_game_state(self):
        # Create and return a representation of the game state
        if self.p == 0:
            state = {
                "playerX": self.game.player.x/self.game.window_width, 
                "playerY": self.game.player.y/self.game.window_height,
                "player2X": self.game.player2.x / self.game.window_width,
                "player2Y": self.game.player2.y / self.game.window_height,
                "mapList": [tile_tuple[1] for tile_tuple in
                            self.game.player.tileTupleList],
                "playerRightMouse": self.PlayerRightMouse,
                "player2RightMouse": self.Player2RightMouse
            }
        else:
            state = {
                "playerX": self.game.player2.x / self.game.window_width,
                "playerY": self.game.player2.y / self.game.window_height,
                "player2X": self.game.player.x / self.game.window_width,
                "player2Y": self.game.player.y / self.game.window_height,
                "mapList": [tile_tuple[1] for tile_tuple in
                            self.game.player.tileTupleList],
                "playerRightMouse": self.Player2RightMouse,
                "player2RightMouse": self.PlayerRightMouse
            }
        return state

    def update_game_state(self, state):
        # Update your local game state with the received state
        if self.p == 0:
            self.game.player2.x = state["player2X"] * self.game.window_width
            self.game.player2.y = state["player2Y"] * self.game.window_height
            self.game.player2.rect.center = (self.game.player2.x,
                                             self.game.player2.y)
            self.game.player2.weapon.in_use = state["player2RightMouse"]
            self.game.player2.weapon.update_weapon()
            self.game.player.weapon.in_use = state["playerRightMouse"]
            self.game.player.weapon.update_weapon()
        else:
            self.game.player.x = state["player2X"] * self.game.window_width
            self.game.player.y = state["player2Y"] * self.game.window_height
            self.game.player.rect.center = (self.game.player.x,
                                            self.game.player.y)
            self.game.player2.x = state["playerX"] * self.game.window_width
            self.game.player2.y = state["playerY"] * self.game.window_height
            self.game.player2.rect.center = (self.game.player2.x,
                                             self.game.player2.y)
            self.game.player2.weapon.in_use = state["playerRightMouse"]
            self.game.player2.weapon.update_weapon()
            self.game.player.weapon.in_use = state["player2RightMouse"]
            self.game.player.weapon.update_weapon()

        for i, tile_tuple in enumerate(self.game.player.tileTupleList):
            if tile_tuple[1] != state["mapList"][i]:
                new_tile_name = state["mapList"][i]
                tile_rect = tile_tuple[0]

                if new_tile_name == "stone.png":
                    self.game.map.update_tile(
                        tile_rect.x - self.game.offset_x,
                        tile_rect.y - self.game.offset_y,
                        'stone_wall.png'
                    )
                    self.game.player.tileTupleList[i] = (tile_rect,
                                                         "stone_wall.png")
                elif new_tile_name == "wood.png":
                    self.game.map.update_tile(
                        tile_rect.x - self.game.offset_x,
                        tile_rect.y - self.game.offset_y,
                        'wood_wall.png'
                    )
                    self.game.player.tileTupleList[i] = (tile_rect,
                                                         "wood_wall.png")
                else:
                    self.game.map.update_tile(
                        tile_rect.x - self.game.offset_x,
                        tile_rect.y - self.game.offset_y,
                        'background.png'
                    )
                    self.game.player.tileTupleList[i] = (tile_rect,
                                                         "background.png")


client = Client()
