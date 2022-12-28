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
        except socket.TimeoutError:
            self.connectSock()
            
        except socket.InterruptedError:
            print("Interrupted..Trying again")
            self.connectSock()
        
        try:
            sockID.connect((self.host,self.port))
        except socket.error:
            print("Connection error , Terminating program\n")
            sys.exit(1)
        except socket.gaierror:
            print("issue in address,Terminating program\n")
            sys.exit(1)

        return sockID
            
            
        
    def multiSock(self):
        print("CONNECTING TO PLUTOS....")

        socket_list=list()
        for i in range(2):
            sock_app=self.connectSock()
            socket_list.append(sock_app)
        return socket_list
        
    







