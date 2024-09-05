from network import Network
import subprocess
import main
import pygame
import re
import sys


class Client:

    def __init__(self):
        self.start()

    def start(self):
        self.game = main.Game(playerpos=(500, 450),
                              enemypos=(900, 450))
        offline = True
        while offline:
            if self.game.status == 8:
                self.game.start_screen()
            if self.game.status == 6:
                self.start_server()
                self.start_multiplayer(self.get_local_ip())
                offline = False
            if self.game.status == 7:
                self.start_multiplayer(self.game.Join_screen())
                offline = False
            if self.game.status == 0:
                self.game.main_menu()
            elif self.game.status == 1:
                self.game.play()
                self.game.player.mousepos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    self.PlayerRightMouse = True
                else:
                    self.PlayerRightMouse = False
            elif self.game.status == 2:
                self.game.options()
            elif self.game.status == 3:
                self.game.game_over(winner=False)
            elif self.game.status == 4:
                self.game.game_over(winner=True)

    def get_local_ip(self):
        try:
            print("Getting local IP address...")
            if sys.platform == "win32":
                # Run ipconfig on Windows
                result = subprocess.run(["ipconfig"], capture_output=True,
                                        text=True)
                output = result.stdout
                # Use regex to find the IPv4 address
                ip_pattern = re.compile(r"IPv4-Adresse[ .]*:[ ]*([\d.]+)")
                match = ip_pattern.search(output)
                if match:
                    return match.group(1)

                ip_pattern = re.compile(r"IPv4 Address(?:[ .]*): ([\d.]+)")
                match = ip_pattern.search(output)
                if match:
                    return match.group(1)

            elif sys.platform == "linux" or sys.platform == "darwin":
                # Run ifconfig on Linux/macOS
                result = subprocess.run(["ifconfig"], capture_output=True,
                                        text=True)
                output = result.stdout

                # Use regex to find the IPv4 address
                ip_pattern = re.compile(r"inet (\d+\.\d+\.\d+\.\d+)")
                matches = ip_pattern.findall(output)
                for ip in matches:
                    # Filter out loopback address and return first match
                    if not ip.startswith("127."):
                        return ip

        except Exception as e:
            print(f"Error getting local IP: {e}")

        return None

    def start_server(self):
        # Command to run your server script in a separate command line window
        command = ["python", "server.py"]

        # Open a new terminal window and run the command (this works on Windws)
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def start_multiplayer(self, ip):
        running = True
        network = Network(ip)
        self.p = network.get_p()
        self.PlayerRightMouse = False
        self.enemyRightMouse = False
        if self.p == 0:  # Position depends on player
            self.game = main.Game(playerpos=(500, 450),
                                  enemypos=(900, 450))
            self.game.status = 0
        else:
            self.game = main.Game(playerpos=(900, 450),
                                  enemypos=(500, 450))
            self.game.status = 0
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
                self.game.game_over(winner=False)
            elif self.game.status == 4:
                self.game.game_over(winner=True)
            self.update_game_state(network.send(self.get_game_state()))

            if (self.game.player.health <= 0):
                self.game.status = 3
            if (self.game.enemy.health <= 0):
                self.game.status = 4

    def get_game_state(self):
        # Get the local game state to send it to the server
        if self.p == 0:  # in this case the enemy is player 1
            state = {
                "player0pos": (self.game.player.x / self.game.window_width,
                               self.game.player.y / self.game.window_height),
                "player1pos": (self.game.enemy.x / self.game.window_width,
                               self.game.enemy.y / self.game.window_height),
                "mapChange": self.getMapChange(),
                "player0RightMouse": self.PlayerRightMouse,
                "player1RightMouse": self.enemyRightMouse,
                "player1Damage": self.game.enemy.damage,
                "player0Energy": self.game.player.energy,
                "player0Weapon": self.game.player.weapon,
                "player0Mousepos": (pygame.mouse.get_pos()[0] /
                                    self.game.window_width,
                                    pygame.mouse.get_pos()[1] /
                                    self.game.window_height)
            }
        else:  # in this case the enemy is player 0
            state = {
                "player0pos": (self.game.enemy.x / self.game.window_width,
                               self.game.enemy.y / self.game.window_height),
                "player1pos": (self.game.player.x / self.game.window_width,
                               self.game.player.y / self.game.window_height),
                "mapChange": self.getMapChange(),
                "player0RightMouse": self.enemyRightMouse,
                "player1RightMouse": self.PlayerRightMouse,
                "player0Damage": self.game.enemy.damage,
                "player1Energy": self.game.player.energy,
                "player1Weapon": self.game.player.weapon,
                "player1Mousepos": (pygame.mouse.get_pos()[0] /
                                    self.game.window_width,
                                    pygame.mouse.get_pos()[1] /
                                    self.game.window_height)
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
            self.game.enemy.damage = state["player1Damage"]
            self.game.player.damage = state["player0Damage"]
            self.game.enemy.energy = state["player1Energy"]
            self.game.enemy.weapon = state["player1Weapon"]
            self.game.enemy.mousepos = (state["player1Mousepos"][0] *
                                        self.game.window_width,
                                        state["player1Mousepos"][1] *
                                        self.game.window_height)
        else:
            self.game.enemy.x = state["player0pos"][0] * self.game.window_width
            self.game.enemy.y = (state["player0pos"][1] *
                                 self.game.window_height)
            self.game.enemy.rect.center = (self.game.enemy.x,
                                           self.game.enemy.y)
            self.game.enemy.weapon.in_use = state["player0RightMouse"]
            self.game.enemy.weapon.update_weapon()
            self.game.enemy.damage = state["player0Damage"]
            self.game.player.damage = state["player1Damage"]
            self.game.enemy.energy = state["player0Energy"]
            self.game.enemy.weapon = state["player0Weapon"]
            self.game.enemy.mousepos = (state["player0Mousepos"][0] *
                                        self.game.window_width,
                                        state["player0Mousepos"][1] *
                                        self.game.window_height)
        self.game.player.mousepos = pygame.mouse.get_pos()
        self.game.enemy.health = (self.game.enemy.energy -
                                  self.game.enemy.damage)
        self.game.player.health = (self.game.player.energy -
                                   self.game.player.damage)
        # This part updates the map
        # print("from server: " + str(state["mapChange"]))
        for j, tile_change in state["mapChange"]:
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
                self.game.enemy.tileTupleList = self.game.player.tileTupleList

    def getMapChange(self):
        # Get the tiles that have changed
        mapChange = []
        for i, tile in enumerate(self.game.player.tileTupleList):
            if self.game.enemy.tileTupleList[i][1] != tile[1]:
                mapChange.append((i, tile[1]))
        return mapChange


client = Client()
