#----------------------------------------------------
# Barometer object featuring the BMP388
# @Author bdpope
# CyLaunch 2023-24
#----------------------------------------------------
import time
import board
import adafruit_bmp3xx

MT_TO_FT = 3.28084

class barometer:
    def __init__(self):
        i2c = board.I2C()
        self.bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
        self.bmp.pressure_oversampling = 8
        self.bmp.temperature_oversampling = 2

    # Returns the altitude in feet
    def get_altitude(self):
        return self.bmp.altitude * MT_TO_FT
