import socket
import pickle

# refer from: https://techwithtim.net/tutorials/python-online-game-tutorial/
# sending-receiving-information/
# and made changes
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostname()
        self.port = 3333
        self.addr = (self.server, self.port)
        self.order = self.connect()
    
    def getOrder(self):
        return self.order

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(4096))
        except:
            pass
    
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            a = self.client.recv(4096)
            return pickle.loads(a)
        except socket.error as e:
            print(e)