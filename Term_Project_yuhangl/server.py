import socket
from _thread import *
import sys
import random
import time
import datetime
import pickle
import pygame

# refer from: https://techwithtim.net/tutorials/python-online-game-tutorial/\
# connecting-multiple-clients/
# and made changes

# initialize the parameters of the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.gethostname()
port = 3333
seed = random.randint(5, 15)
# build server
try:
    s.bind((server, port))
except socket.error as e:
    str(e)
# initialize the number of clients
s.listen(2)
print("Server already started, waiting for a connection.")
# 0 represents not pressed, 1 represents pressed
# "UP, DOWN, LEFT, RIGHT, SPACE, z, x, c, w, s, a, d, m, j, k, l"
def readOrder(order):
    order = order.split(",")
    return list(map(int, order))
# convert list to string
def makeString(result):
    string = ""
    string = "" + str(result[0])
    for i in range(len(result)-1):
        string = string + ","
        string = string + str(result[i+1])
    return string

def makeOrder(order):
    return makeString(order)
# initialize an order, no keys are pressed
order = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
data = [[order, [], [], [], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [], [], [], [], \
        [], [0, 0], [], 13, 13, 0, 0], [order, [], [], [], [], [], [], [], [], \
        [], [], [0, 0], [], 13, 13, 0, 0]]

def threadedClient(conn, player):
    # nonlocal currentPlayer
    # player = player//2
    print(player)
    reply = [0, 0, 0, 0]
    reply = pickle.dumps(reply)
    while currentPlayer < 2:
        conn.sendall(reply)
        a = conn.recv(4096)
    # conn.send(pickle.dumps(data[0]+[seed, 0]))
    if player == 0:
        reply = pickle.dumps(data[1] + [player])
        conn.send(reply)
        receivedData = conn.recv(4096)
        conn.send(reply)
    elif player == 1:
        reply = pickle.dumps(data[0] + [player])
        conn.send(reply)
        receivedData = conn.recv(4096)
        conn.send(reply)
    reply = ""
    count = 0
    while True:
        try:
            receivedData = conn.recv(4096)
            receivedData = pickle.loads(receivedData)
            if player == 0:
                data[0] = receivedData
            elif player == 1:
                data[1] = receivedData
            if not data:
                print("Disconnected")
                break
            else:
                if player == 0:
                    reply = pickle.dumps(data[1] + [player])
                elif player == 1:
                    reply = pickle.dumps(data[0] + [player])
            conn.sendall(reply)
            count += 1
            print("Received: ")
            print(receivedData)
            print("Send: ")
            print(reply)
            print("Data in Server:")
            print(data)
            print(count, datetime.datetime.now())
        except:
            break
    print("Lost connection")
    # currentPlayer -= 1
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    print("before:")
    print(currentPlayer)
    currentPlayer = currentPlayer % 2
    print("after:")
    print(currentPlayer)
    start_new_thread(threadedClient, (conn, currentPlayer))
    currentPlayer += 1
