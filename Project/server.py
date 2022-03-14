#import sys
import socket
import json
from _thread import *
from data.game import Game
from data.load import Data

d = Data("data/properties.txt")

server = socket.gethostbyname(socket.gethostname()) # get local address
port = int(d.find("port"))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # specify socket type

try:
    sock.bind((server, port)) # bind socket to local address
except socket.error as e:
    print(str(e))

sock.listen(0) # enable socket
print("Server Started")
print(f"Server: {server}")
print(f"Port: {port}")
print("Waiting for connections")

games = {}
idCount = 0

def threaded_client(conn, player, gameId):
    global idCount
    conn.send(str.encode(str(player)))

    while True:
        try:
            data = conn.recv(2048).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                elif data != "get":
                    if data.isnumeric():
                        if int(data) in [1, 2, 3, 4, 5, 6, 7]:
                            game.move(player, int(data))
                        else:
                            print("Server can't handle number ", data)
                    else:
                        
                        text = data.split(',') 				# data = "message,Hello, my name is test"
                        if text[0] == 'message':			# text = ['message', 'Hello', ' my name is test']
                            text.pop(0)						# text = ['Hello', ' my name is test']
                            msg = ','.join(text)			# msg  = "Hello, my name is test"
                            game.newMsg(f"{player},{msg}") 	# newMsg("0,Hello, my name is test")

                            								# data = "command,/name 123,abc"
                        elif text[0] == 'command':			# text = ['command', '/name 123', 'abc']
                            print(text) # server shows input
                            if text[1] == '/close':	# ends thread
                                break
                            text.pop(0)						# text = ['/name 123', 'abc']
                            msg = ','.join(text)			# msg  = "/name 123,abc"
                            game.newCmd(f"{player},{msg}")	# newCmd(0,/name 123,abc)
                        else:
                            print("Server can't handle data input ", data)
                conn.sendall(bytes(json.dumps(game.__dict__),encoding="utf-8")) # send game Instance as json
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        print("Closing Game", gameId)
        del games[gameId]
    except:
        pass
    idCount -= 1
    conn.close()

while True:
    conn, addr = sock.accept() # waits for incomming connections
    print("Connected to:", addr)
    idCount += 1
    player = 0
    gameId = (idCount - 1)//2 # 2 players per gameId
    if idCount % 2 == 1:
        print("Creating a new game...")
        games[gameId] = Game(gameId)
        print("Player 1 joined")
    else:
        player = 1
        print("Player 2 joined")
        games[gameId].ready = True
        
    start_new_thread(threaded_client, (conn, player, gameId))
