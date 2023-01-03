import telnetlib
import struct


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
            
        


dummy=Connection()
dummy.send_msp_packet()
