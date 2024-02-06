#----------------------------------------------------
# Airbrakes object for reading from airbrake sensors
# and actuating the airbrake servo.
# 
# @Author bdpope
# CyLaunch 2023-24
#----------------------------------------------------
from helper_objects.barometer import barometer
from helper_objects.accelerometer import accelerometer
from helper_objects.cyllogger import cyllogger
from helper_objects.servo import servo

#----------------------------------------------------
# Constants
#----------------------------------------------------
airbrake_deployment_angle = 120 #120 is 3/4 in deployment
launch_detection_magnitude = 10

class airbrake:
    def __init__(self):
        self.logger = cyllogger("airbrakes")
        self.accelerometer = accelerometer()
        self.barometer = barometer()
        self.servo = servo(18) # Servo is on pin 18

    def deploy_airbrakes(self):
        self.servo.move(airbrake_deployment_angle)
    
    def retract_airbrakes(self):
        self.servo.move(0)

    #TODO Confirm the launch detection magnitude
    def detect_launch(self):
        if(self.accelerometer.accel_magnitude() > launch_detection_magnitude):
            return True
        else:
            return False

    def get_altitude(self):
        return self.barometer.get_altitude()

    def get_acceleration(self):
        return self.accelerometer.accel()