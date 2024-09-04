import socket
from _thread import start_new_thread
import pickle
from main import Game


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 5555


class Server:
    def __init__(self, server):
        """ socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        port = 5555 """

        # socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            socket.bind((server, port))
            print(f"Server bound to {server} on port {port}")
        except socket.error as e:
            print(f"Error binding to {server} on port {port}: {str(e)}")

        socket.listen(2)
        print("Waiting for a connection, Server Started")
        game = Game(playerpos=(500, 450),
                    enemypos=(900, 450))
        players = [game.player, game.enemy]
        game_state = {
            "player0pos": (game.player.x, game.player.y),
            "player1pos": (game.enemy.x, game.enemy.y),
            "mapChange": [],
            "player0RightMouse": False,
            "player1RightMouse": False,
            "player0Damage": game.player.damage,
            "player1Damage": game.enemy.damage,
            "player0Energy": game.player.energy,
            "player1Energy": game.enemy.energy,
            "player0Weapon": game.player.weapon,
            "player1Weapon": game.enemy.weapon,
            "player0Mousepos": (0, 0),
            "player1Mousepos": (0, 0)
        }


        def threaded_client(conn, player):
            conn.send(pickle.dumps(player))
            reply = ""
            while True:
                try:
                    data = pickle.loads(conn.recv(2048))
                    players[player] = data

                    if not data:
                        print("Disconnected")
                        break
                    else:
                        if player == 0:
                            # Update game state with received data
                            game_state["player0pos"] = data["player0pos"]
                            game_state["player1Damage"] = data["player1Damage"]
                            game_state["player0RightMouse"] = data["player0RightMouse"]
                            game_state["player0Energy"] = data["player0Energy"]
                            game_state["player0Weapon"] = data["player0Weapon"]
                            game_state["player0Mousepos"] = data["player0Mousepos"]
                        else:
                            game_state["player1pos"] = data["player1pos"]
                            game_state["player0Damage"] = data["player0Damage"]
                            game_state["player1RightMouse"] = data["player1RightMouse"]
                            game_state["player1Energy"] = data["player1Energy"]
                            game_state["player1Weapon"] = data["player1Weapon"]
                            game_state["player1Mousepos"] = data["player1Mousepos"]
                        reply = game_state
                    game_state["mapChange"].extend(data["mapChange"])
                    conn.sendall(pickle.dumps(reply))

                except Exception as e:
                    print("Error:", e)
                    break

            print("Lost connection")
            conn.close()


        currentPlayer = 0
        while True:
            conn, addr = socket.accept()
            print("Connected to:", addr)

            start_new_thread(threaded_client, (conn, currentPlayer))
            currentPlayer += 1
