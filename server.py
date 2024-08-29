import socket
from _thread import start_new_thread
import pickle
from main import Game

# server = ""  # Public IP
server = "192.168.56.1"  # Local IP Matthias
port = 5555

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    "mapList": [tile_tuple[1] for tile_tuple in game.player.tileTupleList],
    "player0RightMouse": False,
    "player1RightMouse": False,
    "player0Health": game.player.energy,
    "player1Health": game.enemy.energy
    # "playerWeapon": game.player.weapon
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
                    game_state["player1Health"] = data["player1Health"]
                    game_state["player0RightMouse"] = data["player0RightMouse"]
                    # game_state["playerWeapon"] = data["playerWeapon"]
                else:
                    game_state["player1pos"] = data["player1pos"]
                    game_state["player0Health"] = data["player0Health"]
                    game_state["player1RightMouse"] = data["player1RightMouse"]
                reply = game_state
                # print("Received: ", data)
                # print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
            game_state["mapList"] = data["mapList"]
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