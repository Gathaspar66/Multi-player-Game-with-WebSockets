import socket

from MultiGame import configuration


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.AF_INET określa, że korzystamy z adresacji IPv4, socket.SOCK_STREAM to gniazdo przesyłające dane strumieniowo
        self.server = configuration.server
        self.port = configuration.port
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr) #Połącz się ze zdalnym gniazdem pod tym adresem.
            return self.client.recv(2048).decode()#Odbierz dane z gniazda.
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))# Wyślij dane na server
            return self.client.recv(2048).decode()#Odbierz dane z gniazda.
        except socket.error as e:
            print(e)