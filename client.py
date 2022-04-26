import socket

import sys

class Client:
    if len(sys.argv) > 1:
        CLIENT_IP = sys.argv[1]
        CLIENT_PORT = int(sys.argv[2])
    else:
        CLIENT_IP = 'localhost'
        CLIENT_PORT = 5555
    
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = self.CLIENT_IP # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
                                    # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
                                    # ipv4 address. This feild will be the same for all your clients.
        
        #self.host = '25.10.205.39'
        self.port = self.CLIENT_PORT
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        
        return self.client.recv(2048).decode()
    
    def client(self):
        return self.client
    
    def getID(self):
        return self.id

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
