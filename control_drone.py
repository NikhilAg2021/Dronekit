#To use Pygame to control the copter
import pygame
import sys

#Importing dronekit modules
from dronekit import VehicleMode, connect
import time
from pymavlink import mavutil

#Using Tkinter to control the copter
import tkinter as tk

pygame.init()

vehicle=connect('127.0.0.1:14550',wait_ready=True)

# Function to Arm and TakeOff
def arm_and_takeoff(altitude):
    while not vehicle.is_armable:
        print("[INFO] Waiting to Initialize...")
        time.sleep(1)
   
    print("[INFO] Arming Motors")

    vehicle.mode=VehicleMode("GUIDED")
    vehicle.armed=True

    while not vehicle.armed:
        print("[INFO] Waiting To Arm...")
        time.sleep(1)

    print("[IFO] Taking Off...")
    vehicle.simple_takeoff(altitude)

    while True:
        print('[INFO] Altitude {}'.format(vehicle.location.global_relative_frame.alt))
        if vehicle.location.global_relative_frame.alt >= 0.95* altitude:
            print("[INFO] Target Altitude Reached.")
            break
        time.sleep(1)

#Velocity Function defined for the movement of the drone
def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled) !!!READ FROM RIGHT!!!
        0, 0, 0, # Positions (not used)
        velocity_x, velocity_y, velocity_z, # Velocity in m/s
        0, 0, 0, #Acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)


    # send command to vehicle on 1 Hz cycle
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

#KEY Function to check which button pressed using TKinter
def key(event):
    if event.char==event.keysym:  #IF its a standard key
        if event.keysym=='r':
            print('R pressed---- RETURNING HOME!!!')
            vehicle.mode=VehicleMode("RTL")
        if event.keysym=='t':
            print('T pressed---- Prepare for Take-Off!!!')
            arm_and_takeoff(50)
        if event.keysym=='w':
            send_ned_velocity(5,0,0,1)
        if event.keysym=='a':
            send_ned_velocity(0,-5,0,1)
        if event.keysym=='s':
            send_ned_velocity(-5,0,0,1)
        if event.keysym=='d':
            send_ned_velocity(0,5,0,1)
    else: #-- non standard keys
        if event.keysym == 'Up':
            send_ned_velocity(5,0,0,1)
        if event.keysym == 'Down':
            send_ned_velocity(-5,0,0,1)
        if event.keysym == 'Left':
            send_ned_velocity(0,-5,0,1)  
        if event.keysym == 'Right':
            send_ned_velocity(0,5,0,1)

#KEY Function to check which button pressed using PyGame
'''
def key(event):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False
        
        print("Press 't' to TakeOff: ")
        if event.key == ord('t'):
            arm_and_takeoff(50)        

        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False
           
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                send_ned_velocity(0,5,0,1)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                send_ned_velocity(0,-5,0,1)
            if event.key == pygame.K_UP or event.key == ord('w'):
                send_ned_velocity(5,0,0,1)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                send_ned_velocity(-5,0,0,1)
            if event.key == ord('r'):
                print("R Pressed--- Returning Home ")
                vehicle.mode=VehicleMode("RTL")
'''


#Main Function to call the other classes
root=tk.Tk()
print("Control the Drone from the Keyboard ")
print(" Press t to takeoff")
print("Press 'w','a','s','d' or the arrow keys to control the drone")
print("Press 'r' to Return Home ")
root.bind_all('<Key>', key) 
root.mainloop()



    
    


                
