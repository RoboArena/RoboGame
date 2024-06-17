import socket
from _thread import start_new_thread
from player import Player
import pickle
import main

server = ""
port = 5555

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket.bind((server, port))
    print(f"Server bound to {server} on port {port}")
except socket.error as e:
    print(f"Error binding to {server} on port {port}: {str(e)}")

socket.listen(2)
print("Waiting for a connection, Server Started")


def read_pos(str):
    try:
        pos = str.split(",")
        return float(pos[0]), float(pos[1])  # Parse as floats
    except:
        return 0.0, 0.0


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


pos = [(500, 450), (900, 450)]
""""
players = [Player(main.game, 0, 0, 50, 50, 50, 50, 50, 50, 50, 50),
           Player(main.game, 0, 100, 50, 50, 50, 50, 50, 50, 50, 50)]
"""


def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
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
