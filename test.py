import socket,time,math,sys


class protocol:
    def __init__(self) -> None:
        pass

    def evaluateCommand(self):
        print("evaluating")

class Pluto:
    MSP_FC_VERSION=3 
    MSP_RAW_IMU=102 
    MSP_RC = 105 
    MSP_ATTITUDE=108 
    MSP_ALTITUDE=109 
    MSP_ANALOG=110 
    MSP_SET_RAW_RC=200 
    MSP_ACC_CALIBRATION=205 
    MSP_MAG_CALIBRATION=206 
    MSP_SET_MOTOR=214 
    MSP_SET_ACC_TRIM=239 
    MSP_ACC_TRIM=240 
    MSP_EEPROM_WRITE = 250 
    MSP_SET_POS= 216 
    MSP_SET_COMMAND = 217  

    def __init__(self,TCP_IP):
        self.host="192.168.4.1"
        self.port=23
        self.TCP_IP=TCP_IP
        self.TCP_PORT=23
        self.BUFFER_SIZE = 1024
        headerArray=bytearray([36,77,60])
        self.valueArray=bytearray([])
        self.valueArray.extend(headerArray)
        self.valueArray.append(16)      #length of payload
        self.valueArray.append(200)     #MSP_RC_RAW 
        self.valueArray.extend([220,5])  #[200,5] = 1500 RC as [LSB, MSB]
        self.valueArray.extend([220,5])
        self.valueArray.extend([220,5])
        self.valueArray.extend([220,5])
        self.valueArray.extend([176,4])
        self.valueArray.extend([232,3])
        self.valueArray.extend([220,5])
        self.valueArray.extend([176,4])
        self.valueArray.append(234)
        self.Array=self.valueArray[:]
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.mySocket.connect((self.TCP_IP, self.TCP_PORT))
        except:
            print("some error in connecting")
        else:
            self.isConnected=True
            print("Connected!")

    def connectSock(self):
        print("CONNECTING TO PLUTO.....")
        try:
            sockID=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.TimeoutError:
            self.connectSock()
            
        except socket.InterruptedError:
            print("Interrupted..Trying again")
            self.connectSock()
        else:
            sockID.connect((self.host,self.port))
            print("connected")
        return sockID

    def disconnect(self):
        self.mySocket.close()

    #checksum  
    def checksum(self):
        self.CRCArray=self.Array[3:-1]
        self.CRCValue=0
        for d in self.CRCArray:
            self.CRCValue= self.CRCValue^d
        return self.CRCValue
    
    def getBytes(self,value):  # returns all rc commands as bytearray
        self.LSB=value % 256
        self.MSB=value//256
        return bytearray([self.LSB,self.MSB])

    def arm(self):           
        self.Array[19]=220
        self.Array[20]=5
        Val=self.checksum()
        self.Array[21]=Val
        self.sendPacket(self.Array)
    
    def disarm(self):
        self.Array[19]=176
        self.Array[20]=4
        Val=self.checksum()
        self.Array[21]=Val
        self.sendPacket(self.Array)
        
    def setThrottle(self,value):            
        arr=bytearray([])
        arr.extend(self.getBytes(value))
        self.Array[9]=arr[0]
        self.Array[10]=arr[1]
        Val=self.checksum()
        self.Array[21]=Val
        self.sendPacket(self.Array) 
    
    def setRoll(self,value):                  
        arr=bytearray([])
        arr.extend(self.getBytes(value))
        self.Array[5]=arr[0]
        self.Array[6]=arr[1]
        Val=self.checksum()
        self.Array[21]=Val
        self.sendPacket(self.Array)  
    
    def setPitch(self,value):                
        arr=bytearray([])
        arr.extend(self.getBytes(value))
        self.Array[7]=arr[0]
        self.Array[8]=arr[1]
        Val=self.checksum()
        self.Array[21]=Val
        self.sendPacket(self.Array)  

    def setYaw(self,value):              
        arr=bytearray([])
        arr.extend(self.getBytes(value))
        self.Array[11]=arr[0]
        self.Array[12]=arr[1]
        Val=self.checksum()
        self.Array[21]=Val
        self.sendPacket(self.Array) 

    def sendPacket(self,lValueArray):
        self.mySocket.sendall(lValueArray)

    def recieveResponse(self):
        return self.mySocket.recv(self.BUFFER_SIZE)
    
    def disconnect(self):
        self.mySocket.close()

    def multiSock(self):
        print("CONNECTING TO PLUTOS....")

        socket_list=list()
        for i in range(2):
            sock_app=self.connectSock()
            socket_list.append(sock_app)
        return socket_list

p1 = Pluto('192.168.4.1')
p1.connectSock()
p1.arm()
