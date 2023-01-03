import telnetlib
import struct
import socket

class Connection:


    def init(self):
        self.tn=telnetlib.Telnet("192.168.0.4",23)
    
    def send_msp_packet(self):
        payload=struct.pack('<8H',1500,1500,1500,1500,1500,1500,1500,1500)
        checksum=0^len(payload)^200
        
        
       
        
        msp_packet='$M<{}{}{}{}'.format(len(payload),200,payload,checksum)


        self.tn.write(msp_packet)

   
   
    def checksum(payload):
        checksum=0

        for i in payload:
            checksum^=ord(i)
        return checksum
    
    
    def test():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("192.168.0.10", 5760))
        sock.send(b"\x24\x4d\x3c\x00\x00\x00\x00\x00")
        response = sock.recv(1024)
        print(response)
        sock.close()
                 
        

        
        

dummy=Connection()
dummy.send_msp_packet()
