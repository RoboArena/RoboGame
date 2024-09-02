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
        print("You are player", self.p)

        while running:
            if self.game.status == 0:
                self.game.main_menu()
            elif self.game.status == 1:
                self.game.play()
                if pygame.mouse.get_pressed()[0]:
                    self.PlayerRightMouse = True
                else:
                    self.PlayerRightMouse = False
            elif self.game.status == 2:
                self.game.options()
            elif self.game.status == 3:
                self.game.lost_screen()
            elif self.game.status == 4:
                self.game.win_screen()
            self.update_game_state(network.send(self.get_game_state()))

    def get_game_state(self):
        # Get the local game state to send it to the server
        if self.p == 0:  # in this case the enemy is player 1
            state = {
                "player0pos": (self.game.player.x / self.game.window_width,
                               self.game.player.y / self.game.window_height),
                "player1pos": (self.game.enemy.x / self.game.window_width,
                               self.game.enemy.y / self.game.window_height),
                "mapChange0": self.getMapChange(),
                "mapChange1": (),
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
                "mapChange0": (),
                "mapChange1": self.getMapChange(),
                "player0RightMouse": self.enemyRightMouse,
                "player1RightMouse": self.PlayerRightMouse,
                "player0Health": self.game.enemy.energy,
                "player1Health": self.game.player.energy
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
            self.updateLocalMap(state["mapChange1"])
            if (state["player0Health"] <= 0):
                self.game.status = 3
            if (state["player1Health"] <= 0):
                self.game.status = 4
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
            self.updateLocalMap(state["mapChange0"])
            if (state["player0Health"] <= 0):
                self.game.status = 4
            if (state["player1Health"] <= 0):
                self.game.status = 3

    def updateLocalMap(self, mapChange):
        # This part updates the map
        for j, tile_change in mapChange:
            if tile_change != self.game.player.tileTupleList[j][1]:
                new_tile_name = tile_change
                tile_rect = self.game.player.tileTupleList[j][0]

                self.game.map.update_tile(
                    tile_rect.x - self.game.offset_x,
                    tile_rect.y - self.game.offset_y,
                    new_tile_name
                )
                self.game.player.tileTupleList[j] = (tile_rect,
                                                     new_tile_name)

    def getMapChange(self):
        # Get the tiles that have changed
        mapChange = []
        for i, tile in enumerate(self.game.player.tileTupleList):
            if self.game.enemy.tileTupleList[i][1] != tile[1]:
                mapChange.append((i, tile[1]))
        return mapChange


client = Client()
