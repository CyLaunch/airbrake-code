
#----------------------------------------------------
# Main airbrake actuation loop
# @Authors Bstickney & bdpope
# CyLaunch 2023-24
#----------------------------------------------------

import numpy as np
import time
import math
from airbrake import airbrake
from helper_objects.cyllogger import cyllogger

# ----------------------------------------------------------------------
# LAUNCH PARAMS
# ----------------------------------------------------------------------
TRGT_ALT_FT = 5000.0 
ALT_MAX_SPEED_FT_S = 700.0
MOTOR_BURN_TIME_S = 4.0
AB_ACTUATION_TIME_S = 9.0
NS_TO_S = 0.000000001

# Airbrake object
ab = airbrake()

# Logger
main_log = cyllogger("main")

def main():
    currSpeed = 0.0

    #Launch Phase
    main_log.writeTo("Entering Detect launch Loop.")
    while ab.detect_launch() == False:
        time.sleep(0.25) 
        main_log.writeTo("Launch Not Detected.")
    main_log.writeTo("Launch Detected! Exiting Loop.")

    # Motor Burn
    main_log.writeTo("Entering motor burn sleep of {} Seconds".format(MOTOR_BURN_TIME_S))
    time.sleep(MOTOR_BURN_TIME_S)
    main_log.writeTo("Exiting motor burn sleep.")
    
    # Coasting to apogee
    main_log.writeTo("Entering Aibrake actuation loop. Will timeout in {} seconds".format(AB_ACTUATION_TIME_S))
    timeout = time.time() + AB_ACTUATION_TIME_S
    while timeout >= time.time(): # In total 13 seconds after launch
        try:
            currSpeed = Calculations.current_speed()
            total_alt = Calculations.predicted_alt(ab.get_altitude(),currSpeed)
            main_log.writeTo("Predicted Alt: {}ft.".format(total_alt))
            if total_alt >= TRGT_ALT_FT:
                main_log.writeTo("Target altitude exceeded! Deploying airbrakes.")
                ab.deploy_airbrakes()
                main_log.writeTo("Airbrakes deployed.")
            else: 
                ab.retract_airbrakes()
                main_log.writeTo("Airbrakes are retracted.")
        except Exception as e:
            main_log.writeTo(e.message)
            main_log.writeTo("Exception caught in AB Deployment loop, looping again")
            ab.retract_airbrakes()

    # Close the airbrakes upon exiting while loop
    ab.retract_airbrakes()
    main_log.writeTo("Timeout Occured, Retracting airbrakes and sleeping")

    # Keeps the airbrakes actively retracted for 5 minutes after apogee
    time.sleep(300) 
    main_log.writeTo("Sleep complete, woohoo! I survived launch!")

class Calculations:
    def current_speed():
        alt_s1 = ab.get_altitude()
        before_time_ns = time.time_ns()

        alt_s2 = ab.get_altitude()
        after_time_ns = time.time_ns()

        time_delta_s = (after_time_ns - before_time_ns) * NS_TO_S

        altSpeed = (alt_s2-alt_s1)/time_delta_s

        if altSpeed > ALT_MAX_SPEED_FT_S: #This can change so it makes sense just if its outside of bounds
            ab.retract_airbrakes() #TODO we should not be retracting here, it should be in main Brenner take a look
            return 1.0
        else:
            return altSpeed
    
    def predicted_alt(alt,velocity): 
        m=26.75 #lbs 
        Cd=0.53 #CHANGE for each rocket!! 
        A= 0.2413 # ft^2 
        rho=0.062 #lbs/ft^3 at 2000ft 
        g=32.16789 #ft/s^2 
        Xc=(m/(rho*Cd*A)*math.log((m*g+0.5*rho*Cd*A*velocity**2)/(m*g)))+alt
        return Xc

if __name__ == "__main__":
    main()
