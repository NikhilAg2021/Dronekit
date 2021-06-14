from dronekit import LocationGlobalRelative, VehicleMode, connect

vehicle=connect('127.0.0.1:14550',wait_ready=True)

# Set mode to guided - this is optional as the goto method will change the mode if needed.
def home():

    vehicle.mode = VehicleMode("GUIDED")

    # Set the target location in global-relative frame
    a_location = LocationGlobalRelative(-35.363261838062115, 149.16523726155145 , 90) #Holds the co-ordinates of the HOME
    vehicle.simple_goto(a_location)

    # Set groundspeed using `simple_goto()` parameter
    vehicle.simple_goto(a_location, groundspeed=10)

home()