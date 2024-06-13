import socket
from _thread import start_new_thread
from player import Player
import pickle
import main

server = "10.0.13.213"
port = 5555

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket.bind((server, port))
except socket.error as e:
    str(e)

socket.listen(2)
print("Waiting for a connection, Server Started")

""""
players = [Player(main.game, 0, 0, 50, 50, 50, 50, 50, 50, 50, 50),
           Player(main.game, 0, 100, 50, 50, 50, 50, 50, 50, 50, 50)]
"""


def threaded_client(conn, player):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))
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
