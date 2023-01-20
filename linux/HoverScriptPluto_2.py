import time
#from getch import getch
from telnetlib import Telnet as tn
import sys
import struct
from threading import *
from height_aruco import *
from task_2 import drone
class hover:
    kp = 7.5 
    ki = 0
    kd = 4.3
    error = 1.0
    integral = 1.0
    derivative = 1.0
    output = 1.0
    setpoint = 50.0
    height_max=0

    throttle_min = 0
    throttle_max = 50
    height_min = 0

    slope = (throttle_max - throttle_min) / (height_max - height_min)
    intercept = throttle_min - slope * height_min

    def height_to_throttle(height):
        return hover.slope * height + hover.intercept

    #tello = Tello()
    #tello.connect()
    #time.sleep(0.5)
    #output = tello.get_battery()
    #print(output)

    
    #tello.takeoff()
    def throttle_required(self):
        integral = 0.0
        derivative = 0.0
        previous_error = 0.0

        desired_altitude_reached = False

        while not desired_altitude_reached :
            process_value = height.show_webcam(self)
            error = hover.setpoint - process_value
            integral = integral + error
            derivative = error - previous_error
            output = hover.kp * error + hover.ki * integral + hover.kd * derivative
            throttle = hover.height_to_throttle(int(output))
            output = max(hover.throttle_min, min(hover.throttle_max, throttle))
            tn.write(drone.msp_set_raw_rc(self,throttle=output))
            previous_error = error

            if abs(error) < 0.5:
                desired_altitude_reached = True
            time.sleep(0.1)
                

            #tello.move_up(int(output))
            #tello.send_rc_control(left_right_velocity=0,forward_backward_velocity=0,up_down_velocity=(int(output)),yaw_velocity=0)
            

        while desired_altitude_reached:
            current_height = height.show_webcam(self)
            throttle = hover.height_to_throttle(current_height)
            #tello.move_up(int(throttle))
            #tello.send_rc_control(left_right_velocity=0,forward_backward_velocity=0,up_down_velocity=(int(output)),yaw_velocity=0)
            previous_height = current_height

            time.sleep(0.5)
            
            if abs(current_height - previous_height) > 2:
                desired_altitude_reached = False
                break
        #key = getch()
        # if key == "q":
        #     tello.land()
