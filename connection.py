import socket
from protocol import protocol
import sys 

class connection:

    def __init__(self):
        self.host="192.168.4.1"
        self.port=23


    def create_Sock(self):
        try:
            sockID=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.timeout:
            print("Error while creating socket. \n Retrying...")
            self.create_Sock()
        except socket.error:
            print("Error while creating socket. \n Retrying...")
            self.create_Sock()
        
        return sockID
    
    

    def connectSock(self):
        print("CONNECTING TO PLUTO...")
        sockID=self.create_Sock()
        try:
            sockID.connect(self.host, self.port)
        except socket.timeout:
            print("Error while connecting to pluto. \n Retrying...")
            self.connectSock()
        except socket.InterruptedError:
            print("Error while connecting to pluto. \n Retrying...")
            self.connectSock()
        return sockID
        


    def multi_Sock(self):
        print("CONNECTING TO PLUTOS....")

        socket_list=list()
        for i in range(2):
            sock_app=self.connectSock()
            socket_list.append(sock_app)
        return socket_list
        
    







