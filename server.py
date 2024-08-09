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
game = Game()
players = [game.player, game.player2]
game_state = {
    "playerX": game.player.x,
    "playerY": game.player.y,
    "player2X": game.player2.x,
    "player2Y": game.player2.y,
    "mapList": [tile_tuple[1] for tile_tuple in game.player.tileTupleList],
    "playerRightMouse": False,
    "player2RightMouse": False,
    "playerHealth": game.player.healing,
    "player2Health": game.player2.healing
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
                game_state["playerRightMouse"] = data["playerRightMouse"]
                game_state["player2RightMouse"] = data["player2RightMouse"]
                if player == 0:
                    # Update game state with received data
                    game_state["playerX"] = data["playerX"]
                    game_state["playerY"] = data["playerY"]
                    game_state["player2Health"] = data["player2Health"]
                else:
                    game_state["player2X"] = data["player2X"]
                    game_state["player2Y"] = data["player2Y"]
                    game_state["playerHealth"] = data["playerHealth"]
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
