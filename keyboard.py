import msvcrt
from threading import *
last_button=None
class keyboard(Thread): # creating a class with methods to recieve keyboard inputs

    def __init__(self):
     super(keyboard,self).__init__()
     pass
    def run(self):
        
     while True:
         if msvcrt.kbhit(): 
             bkey=msvcrt.getch() # returns the key value that is pressed in bytes
             key=bkey.decode() 
             return key

         else:
             key=last_button
            
             return key