import random
import time
import threading

class Game:
    def __init__(self, id):
        self.id = id
        self.wins = [0,0]
        self.ready = False
        self.nextPlayer = random.randint(1,2)
        self.state = [([0]*7) for i in range(5)]
        self.chat = ['2,The Chat starts here', '2,type /help for commands']
        self.debug = False # testing
        self.waitBetweenRounds = 3
        self.roundDone = False
        self.userNames = ["Player 1", "Player 2"]
        self.colors = { "player1_1":    (50,50,150),
                        "player2_1":    (150,50,50),
                        "player1_2":    (150,150,150),
                        "player2_2":    (150,150,150)}

    def move(self, player, number):
        if self.debug:
            print(f"player {player} trys a move at x = {number - 1}")
        if not self.roundDone:
            if player + 1 == self.nextPlayer:
                for e in reversed(self.state):
                    if e[number - 1] == 0:
                        print(f"player {player} makes move at x = {number - 1}")
                        e[number - 1] = self.nextPlayer
                        if self.nextPlayer == 1:
                            self.nextPlayer = 2
                        else:
                            self.nextPlayer = 1
                        break
                self.checkState()

    def checkState(self):
        if self.debug:
            print("checking State")
        for player in range(1,3):
            if self.checkHorizontals(player):
                self.winner(player)
                break
            elif self.checkVerticals(player):
                self.winner(player)
                break
            elif self.checkDiagonals(player):
                self.winner(player)
                break
        if self.checkNoMoreMoves():
            self.winner(-1)

    def checkHorizontals(self, player):
        if self.debug:
            print("checking Horizontals, Player", player)
        for x in range(len(self.state[0]) - 3):
            for y in range(len(self.state)):
                if self.state[y][x] == player and self.state[y][x + 1] == player and self.state[y][x + 2] == player and self.state[y][x + 3] == player:
                    self.state[y][x] = player + 2
                    self.state[y][x + 1] = player + 2
                    self.state[y][x + 2] = player + 2
                    self.state[y][x + 3] = player + 2
                    return True
        return False

    def checkVerticals(self, player):
        if self.debug:
            print("checking Verticals, Player", player)
        for x in range(len(self.state[0])):
            for y in range(len(self.state) - 3):
                if self.state[y][x] == player and self.state[y + 1][x] == player and self.state[y + 2][x] == player and self.state[y + 3][x] == player:
                    self.state[y][x] = player + 2 
                    self.state[y + 1][x] = player + 2 
                    self.state[y + 2][x] = player + 2
                    self.state[y + 3][x] = player + 2
                    return True
        return False

    def checkDiagonals(self, player):
        if self.debug:
            print("checking Diagonals, Player", player)
        for x in range(len(self.state[0])):
            for y in range(len(self.state) - 3):
                if x >= 3:
                    if self.state[y][x] == player and self.state[y + 1][x - 1] == player and self.state[y + 2][x - 2] == player and self.state[y + 3][x - 3] == player:
                        self.state[y][x] = player + 2 
                        self.state[y + 1][x - 1] = player + 2 
                        self.state[y + 2][x - 2] = player + 2
                        self.state[y + 3][x - 3] = player + 2
                        return True
                if x <= 3:
                    if self.state[y][x] == player and self.state[y + 1][x + 1] == player and self.state[y + 2][x + 2] == player and self.state[y + 3][x + 3] == player:
                        self.state[y][x] = player + 2 
                        self.state[y + 1][x + 1] = player + 2 
                        self.state[y + 2][x + 2] = player + 2
                        self.state[y + 3][x + 3] = player + 2
                        return True
        return False

    def checkNoMoreMoves(self):
        if self.debug:
            print("checking for possible moves")
        for a in self.state[0]:
            if a == 0:
                return False
        return True

    def winner(self, player):
        if self.debug:
            print(self.state[0])
            print(self.state[1])
            print(self.state[2])
            print(self.state[3])
            print(self.state[4])
        if player == -1:
            print("no winner")
        else:
            print(f"winner is Player {player}")
            self.wins[player - 1] += 1
        self.roundDone = True
        self.newMsg(f"2,game restarts in {self.waitBetweenRounds} seconds")
        timer = threading.Timer(self.waitBetweenRounds, self.restart)
        timer.start()

    def restart(self):
        nxt = random.randint(1, 2)
        self.newMsg(f"{nxt - 1},Player {nxt} starts")
        self.nextPlayer = nxt
        self.state = [([0] * 7) for i in range(5)]
        self.roundDone = False

    def newMsg(self, msg):
        self.chat.append(msg)

    def newCmd(self, msg):
        self.chat.append(f"{msg[0]},{msg[2:]}")
        if msg[3:] == "reset wins":
            self.wins = [0,0]
            self.chat.append(f"2,Player {int(msg[0]) + 1} has reset the wins")
        elif msg[3:] == "reset state":
            self.newMsg(f"2,game restarts in {self.waitBetweenRounds} seconds")
            timer = threading.Timer(self.waitBetweenRounds, self.restart)
            timer.start()
        elif msg[3:] == "reset chat":
            self.chat = []
            self.chat.append(f"2,Player {int(msg[0]) + 1} has reset the chat")
        elif msg[3:7] == "say ":
            self.chat.append(f"2,Player {int(msg[0]) + 1} {msg[7:]}")
        elif msg[3:7] == "roll":
            if msg[8:].isnumeric() and int(msg[8:]) > 0:
                self.chat.append(f"2,Player {int(msg[0]) + 1} rolls {random.randint(1, int(msg[8:]))} (custom)")
            else:
                self.chat.append(f"2,Player {int(msg[0]) + 1} rolls {random.randint(1,6)} (normal)")
        elif msg[3:9] == "delay " and msg[9:].isnumeric():
            self.chat.append(f"2,Player {int(msg[0]) + 1} has set delay to {msg[9:]} s")
            self.waitBetweenRounds = int(msg[9:])
        elif msg[3:] == "help":
            self.chat.append("2,/help | server commands")
            self.chat.append("2,/help 2 | client commands")
            self.chat.append("2,/reset wins | wins = 0 - 0")
            self.chat.append("2,/reset state | reset board")
            self.chat.append("2,/reset chat | reset chat")
            self.chat.append("2,/say x | Sys: Player x (text)")
            self.chat.append("2,/roll | random 1 - 6")
            self.chat.append("2,/roll x | random 1 - x (number)")
            self.chat.append("2,/delay x | x sec between rounds")
            self.chat.append("2,/name x | username = x")
            self.chat.append("2,/close | close game")
        elif msg[3:] == "help 2":
            self.chat.append("2,//color Element Hex-Value")
            self.chat.append("2,Element: me1, me2, text,")
            self.chat.append("2,background, buttons, chat")
            self.chat.append("2,Hex-Value: 000000 - ffffff")
            self.chat.append("2,//save x| save theme x (name)")
            self.chat.append("2,//load x | load theme x (name)")
            self.chat.append("2,//themes | list your themes")
            self.chat.append("2,//scale x | width = x (pixels)")
            self.chat.append("2,//ping | roundtrip time to server (ms)")
        elif msg[3:14] == "color this ":
            c1 = msg[14:20]
            c2 = msg[21:27]
            if msg[0] == "0":
                self.colors["player1_1"] = tuple(int(c1[i:i + 2], 16) for i in (0, 2, 4)) # rgb hex -> tuple
                self.colors["player1_2"] = tuple(int(c2[i:i + 2], 16) for i in (0, 2, 4))
            elif msg[0] == "1":
                self.colors["player2_1"] = tuple(int(c1[i:i + 2], 16) for i in (0, 2, 4))
                self.colors["player2_2"] = tuple(int(c2[i:i + 2], 16) for i in (0, 2, 4))
        elif msg[3:8] == "name ":
            self.userNames[int(msg[0])] = msg[8:]
        else:
            self.chat.append(f"2,Command {msg} not found")
