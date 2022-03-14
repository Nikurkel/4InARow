import socket

class Network:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # specify socket type
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)
        self.buffer = 2048 # receive up to x bytes from the socket
        self.player = self.connectToServer()

    def getPlayer(self):
        return self.player

    def connectToServer(self):
        try:
            self.sock.connect(self.addr) # send client address
            return self.sock.recv(self.buffer).decode() # server returns player number
        except:
            pass

    def send(self, data):
        try:
            self.sock.send(str.encode(data)) # any player input
            return self.sock.recv(self.buffer) # new game state
        except socket.error as e:
            print(e)