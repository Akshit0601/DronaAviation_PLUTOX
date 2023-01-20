import pynput
from threading import *





class keyboard(Thread): 
     # creating a class with methods to recieve keyboard inputs

    def __init__(self):
        super(keyboard,self).__init__()
        self.last_button = None

        pass
    
    def on_press(key,self):
        try:
         
            self.last_button = key.char
            
            
        except AttributeError:
            print("error with keyboard input")

    def on_release(key):
        if key == pynput.keyboard.Key.esc:
            return False   
    
    def run(self):
        with pynput.keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
            listener.join()
    
