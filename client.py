from network import Network
import main


class Client:

    def __init__(self):
        self.main()

    def main(self):
        running = True
        network = Network()
        self.p = network.get_p()
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
                self.update_game_state(network.send(self.get_game_state()))
            elif self.game.status == 2:
                self.game.options()

    def get_game_state(self):
        # Create and return a representation of the game state
        if self.p == 0:
            state = {
                "playerX": self.game.player.x,
                "playerY": self.game.player.y,
                "player2X": self.game.player2.x,
                "player2Y": self.game.player2.y,
                "mapList": [tile_tuple[1] for tile_tuple in self.game.player.tileTupleList]
            }
        else:
            state = {
                "playerX": self.game.player2.x,
                "playerY": self.game.player2.y,
                "player2X": self.game.player.x,
                "player2Y": self.game.player.y,
                "mapList": [tile_tuple[1] for tile_tuple in self.game.player.tileTupleList]
            }
        return state

    def update_game_state(self, state):
        # Update your local game state with the received state
        if self.p == 0:
            self.game.player.x = state["playerX"]
            self.game.player.y = state["playerY"]
            self.game.player2.x = state["player2X"]
            self.game.player2.y = state["player2Y"]
        else:
            self.game.player.x = state["player2X"]
            self.game.player.y = state["player2Y"]
            self.game.player2.x = state["playerX"]
            self.game.player2.y = state["playerY"]

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
                    self.game.player.tileTupleList[i] = (tile_rect, "stone_wall.png")
                elif new_tile_name == "wood.png":
                    self.game.map.update_tile(
                        tile_rect.x - self.game.offset_x,
                        tile_rect.y - self.game.offset_y,
                        'wood_wall.png'
                    )
                    self.game.player.tileTupleList[i] = (tile_rect, "wood_wall.png")
                else:
                    self.game.map.update_tile(
                        tile_rect.x - self.game.offset_x,
                        tile_rect.y - self.game.offset_y,
                        'background.png'
                    )
                    self.game.player.tileTupleList[i] = (tile_rect, "background.png")


client = Client()
