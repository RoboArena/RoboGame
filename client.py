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
        self.enemyRightMouse = False
        if self.p == 0:  # Position depends on player
            self.game = main.Game(playerpos=(500, 450),
                                  enemypos=(900, 450))
        else:
            self.game = main.Game(playerpos=(900, 450),
                                  enemypos=(500, 450))

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
        # Get the local game state to send it to the server
        if self.p == 0:  # in this case the enemy is player 1
            state = {
                "player0pos": (self.game.player.x / self.game.window_width,
                               self.game.player.y / self.game.window_height),
                "player1pos": (self.game.enemy.x / self.game.window_width,
                               self.game.enemy.y / self.game.window_height),
                "mapList": [tile_tuple[1] for tile_tuple in
                            self.game.player.tileTupleList],
                "player0RightMouse": self.PlayerRightMouse,
                "player1RightMouse": self.enemyRightMouse,
                "player0Health": self.game.player.energy,
                "player1Health": self.game.enemy.energy
            }
        else:  # in this case the enemy is player 0
            state = {
                "player0pos": (self.game.enemy.x / self.game.window_width,
                               self.game.enemy.y / self.game.window_height),
                "player1pos": (self.game.player.x / self.game.window_width,
                               self.game.player.y / self.game.window_height),
                "mapList": [tile_tuple[1] for tile_tuple in
                            self.game.player.tileTupleList],
                "player0RightMouse": self.enemyRightMouse,
                "player1RightMouse": self.PlayerRightMouse,
                "player0Health": self.game.enemy.healing,
                "player1Health": self.game.player.healing
            }
        return state

    def update_game_state(self, state):
        # Update your local game state with the received state
        if self.p == 0:  # in this case the enemy is player 1
            self.game.enemy.x = state["player1pos"][0] * self.game.window_width
            self.game.enemy.y = (state["player1pos"][1] *
                                 self.game.window_height)
            self.game.enemy.rect.center = (self.game.enemy.x,
                                           self.game.enemy.y)
            self.game.enemy.weapon.in_use = state["player1RightMouse"]
            self.game.enemy.weapon.update_weapon()
            self.game.player.energy = state["player0Health"]
        else:
            self.game.enemy.x = state["player0pos"][0] * self.game.window_width
            self.game.enemy.y = (state["player0pos"][1] *
                                 self.game.window_height)
            self.game.enemy.rect.center = (self.game.enemy.x,
                                           self.game.enemy.y)
            self.game.enemy.weapon.in_use = state["player0RightMouse"]
            self.game.enemy.weapon.update_weapon()
            self.game.player.energy = state["player1Health"]
            self.game.enemy.energy = state["player0Health"]

        # This part updates the map
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
