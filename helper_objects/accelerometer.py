#----------------------------------------------------
# Accelerometer object for the ICM20649
# @Author Marcus Miller
# CyLaunch 2023-24
#----------------------------------------------------

import time
import board
import adafruit_icm20x
import math

class accelerometer:

    def __init__(self):
        self.i2c = board.I2C()  
        self.icm = adafruit_icm20x.ICM20649(self.i2c)

    def gyro(self):
        return self.icm.gyro
        
    # Returns a touple of the x, y, & z accelerations
    def accel(self):
        return self.icm.acceleration

    # Returns the maginitude of the X, Y, & Z
    # Accelerations in meters
    def accel_magnitude(self):
        data = self.accel()
        # This gives me gravity at around 19 m/s wtf
        return (math.sqrt(((data[0]**2) + (data[1]**2) + (data[2]**2)))) / 2

        
    
         

## Example
# a = accelerometer()

# for i in range(a.iterations):
#     print("Gyro value is:", a.gyro())
#     print("Accelerometer value is:", a.accel())
#     time.sleep(1)