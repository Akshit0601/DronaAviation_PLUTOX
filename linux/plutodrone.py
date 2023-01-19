from telnetlib import Telnet
import time
import sys
import struct
from threading import *
# from keyboard import *
from keyboard_pyn import *
from height_aruco import *
# from HoverScriptPluto_2 import hover



last_button=None

class drone(Thread):

    global land_start
    land_start=False

    def __init__(self,last_button=None):
        super(drone,self).__init__()
        pass
        
    
       
    def make_in(self,command: int, byte_arr: bytes):

      cmd = struct.pack(f"<cBB{len(byte_arr)}s", b'<',len(byte_arr), command, byte_arr)

      crc = 0
      for c in cmd[1:]:
         crc ^= c
      crcb = bytes([crc])    
      return b"$M" + cmd + crcb

    def make_out(command:int,byte_arr:bytes):
      cmd = struct.pack(f"<cBBs", b'<',6, command, byte_arr)
      crc=0
      for c in cmd[1:]:
         crc^=c
      crcb=bytes([crc])
      return b"$M"+cmd+crcb

    def msp_attitude():
      payload=bytearray(6) 
      return drone.make_out(0x6c,payload)

    def msp_raw_imu():
      payload=bytearray(9)
      return drone.make_out(0x66,payload)

    def msp_altitude():
      payload=bytearray(2)
      return drone.make_out(0x6d,payload)

    def msp_set_raw_rc(self,roll=1500, pitch=1500, throttle=1000, yaw=1500, aux1=2100, aux2=900, aux3=1500, aux4=1500):
      payload = struct.pack("<8H", roll, pitch, throttle,yaw, aux1, aux2, aux3, aux4)
      return drone.make_in(self,0xc8, payload)

    
    def arm(self):
       return drone.msp_set_raw_rc(self,throttle=1000, aux4=1600)

    def box_arm(self):
       return drone.msp_set_raw_rc(self,throttle=1000, aux4=1500)


    def disarm(self):
       return drone.msp_set_raw_rc(self,aux4=900)

    def takeoff(self):
       return drone.make_in(self,0xd9, struct.pack("<H", 1))

    def land(self):
      return drone.make_in(self,0xd9, struct.pack("<H", 2))

    def button_pressed(self):
      global last_button
      last_button = input("Enter command: ")

    def f(self,var=True):
        return var

    def run(self):
        with Telnet('192.168.4.1', 23) as tn:
         throttle = 1000
         yaw = 1500
         pitch = 1500
         roll = 1500
         armed = None

         
         print("ready to take commands")
         last_button = obj2.last_button
         try:
             while True:
               last_button = keyboard.run(self)
               if last_button == "d":
                  armed = False

               elif last_button == "a":
                  tn.write(self.arm())
                  armed=True
               elif last_button == "x" and armed :
                  print('TAKEOFF START', end='\n', flush=True)             
                  
                  tn.write(self.takeoff())
                  armed = True
                  time.sleep(0.2)
                  hover.throttle_required(self)
                  throttle = 1500
                

               elif last_button == "y" and armed:
                  print('LAND START', end='\n', flush=True)
                  tn.write(self.land())
                  time.sleep(2)
                  throttle = 1400
                  armed = True


               if not armed:
                  tn.write(self.disarm())
                  print('DISARMED', end='\n', flush=True)
                  continue
               a=last_button
               
               tn.write(self.msp_set_raw_rc(roll=roll, pitch=pitch, throttle=int(throttle), yaw=yaw))
               time.sleep(0.2)
               print('throttle: {:4.2f}    roll: {:4}    pitch {:4}    yaw {:4}'.format(throttle, roll, pitch, yaw), end='\n', flush=True)
               last_button=a
               tn.write(self.msp_altitude())
               data=tn.read_very_eager()
               time.sleep(0.2)

         except KeyboardInterrupt:
            pass
            tn.write(self.disarm())

   
d1=drone()
obj2=keyboard()
obj2.start()
d1.start()

