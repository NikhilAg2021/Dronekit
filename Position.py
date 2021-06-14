from dronekit import LocationGlobalRelative, VehicleMode, connect

vehicle=connect('127.0.0.1:14550',wait_ready=True)


def Position():
    vehicle.mode = VehicleMode("GUIDED")

    # Set the target location in global-relative frame
    a_location = LocationGlobalRelative(-35.35985995, 149.14994320, 90)
    vehicle.simple_goto(a_location)

    # Set groundspeed using `simple_goto()` parameter
    vehicle.simple_goto(a_location, groundspeed=10)

Position()