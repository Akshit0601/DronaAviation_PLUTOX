import socket
from protocol import protocol
import sys


class Connection:
    def __init__(self):
        self.host = "192.168.4.1"
        self.port = 23

    def connectSock(self):

        print("CONNECTING TO PLUTO.....")

        sockID = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sockID.connect((self.host, self.port))
        except socket.timeout:
            sockID.connect((self.host, self.port))
        except InterruptedError:
            sockID.connect((self.host, self.port))
        except socket.error as err:
            print("couldn't connect with socket-server %s \n Terminating program" % err)
            sys.exit(1)
            
        sockID.setblocking(False)
        return sockID

    def multiSock(self):
        print("CONNECTING TO PLUTOS....")

        socket_list = list()
        for i in range(2):
            sock_app = self.connectSock()
            socket_list.append(sock_app)
        return socket_list
