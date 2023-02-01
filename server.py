import socket
from _thread import *

import pygame

from MultiGame import configuration
from ball import Ball

pos = {"playerPosition1": (100, 200), "playerPosition2": (900, 200), "ballPosition": (500, 250), "points": (0, 0)}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create INET, STREAM socket

try:
    server.bind(
        (configuration.server, configuration.port))  # assigns an IP address and port number to a socket instance.
except socket.error as e:
    str(e)

server.listen(2)  # listens to a certain number of calls
print("Waiting for a connectionection, Server Started")


def read_pos(data):
    data = eval(data)

    return data


def make_pos(player, ball_position, points):
    data = {"playerPosition": player, "ballPosition": ball_position, "points": points}

    return data


def thread_client(connection, player):
    points_player1 = 0
    points_player2 = 0
    delay = 0

    connection.send(str.encode(str(make_pos(pos[player], pos['ballPosition'], pos['points']))))  # sends start positions
    print("started")

    while True:
        try:
            data = read_pos(connection.recv(2048).decode())

            ball.check_collision(data, pos["ballPosition"])

            if delay <= 0:
                if pos["ballPosition"][0] == 0:
                    points_player1 += 1
                    delay = 20

                if pos["ballPosition"][0] == 955:
                    points_player2 += 1
                    delay = 20
            delay -= 1

            pos["points"] = (points_player1, points_player2)

            if player == "playerPosition1":
                pos["playerPosition1"] = data['position']
                connection.sendall(
                    str.encode(str(make_pos(pos["playerPosition2"], pos['ballPosition'], pos['points']))))
            else:
                pos["playerPosition2"] = data['position']
                connection.sendall(
                    str.encode(str(make_pos(pos["playerPosition1"], pos['ballPosition'], pos['points']))))
        except:
            break
    print("Lost connectione")
    connection.close()


ball = Ball()
clock = pygame.time.Clock()
while True:

    # accept the call. The socket must be associated with an address and listen for connections.
    # The return value is a pair (connection, address), where connection is a new socket object that can be used to send
    # and receive data on the connection,# and address is the address associated with the socket at the other end of the connection.
    connection, addr = server.accept()

    print("connected to: ", str(addr))
    if configuration.number_of_players == 0:
        start_new_thread(thread_client, (connection, 'playerPosition1'))
    else:
        start_new_thread(thread_client, (connection, 'playerPosition2'))

    configuration.number_of_players += 1
    if configuration.number_of_players == 2:
        break

while True:
    clock.tick(60)
    (pos["ballPosition"]) = ball.movement()
