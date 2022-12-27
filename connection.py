import socket
from protocol import protocol
import sys 

class connection:

    def __init__(self,host,port):
        self.host=host
        self.port=port


    def connectSock(self):
        print("CONNECTING TO PLUTO.....")
        try:
            sockID=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.timeout:
            self.connectSock()
            
        except socket.InterruptedError:
            print("Interrupted..Trying again")
            self.connectSock()
        else:
            sockID.connect((self.host,self.port))

        
        return sockID


    def multiSock(self):
        print("CONNECTING TO PLUTOS....")

        socket_list=list()
        for i in range(2):
            sock_app=self.connectSock()
            socket_list.append(sock_app)
        return socket_list
        
    







