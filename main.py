import numpy as np
from helper_objects import cyllogger
import time
import math
from airbrake import airbrake
from helper_objects.cyllogger import cyllogger

# LAUNCH PARAMS
# ----------------------------------------------------------------------
TRGT_ALT_FT = 5000.0 
ALT_MAX_SPEED_FT_S = 700.0
MOTOR_BURN_TIME_S = 3.0
AB_ACTUATION_TIME_S = 10.0
# ----------------------------------------------------------------------

# Airbrakes
ab = airbrake()

# Logger
main_log = cyllogger("main")

def main():
    currSpeed = 0.0

    main_log.writeTo("Entering Detect launch Loop.")
    #Launch Phase
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
        except:
            # Let the loop keep going
            main_log.writeTo("Exception caught in AB Deployment loop, looping again")

    # Close the airbrakes upon exiting while loop
    ab.retract_airbrakes()
    main_log.writeTo("Timeout Occured, Retracting airbrakes and sleeping")
    time.sleep(300) # Keeps the airbrakes actively retracted for 5 minutes after apogee
    main_log.writeTo("Sleep complete, woohoo! I survived launch!")

class Calculations:
    def current_speed():
        alt_s1 = ab.get_altitude()
        alt_s2 = ab.get_altitude()
        accSpeed = 0.0
        altSpeed = (alt_s2-alt_s1)/0.02
        if altSpeed > ALT_MAX_SPEED_FT_S: #This can change so it makes sense just if its outside of bounds
            ab.retract_airbrakes()
            return 1.0
        else:
            return altSpeed
    
    def predicted_alt(alt,velocity): 
        m=30.25 #lbs 
        Cd=0.61 #CHANGE for each rocket!! 
        A= 0.2413 # ft^2 
        rho=0.062 #lbs/ft^3 at 2000ft 
        g=32.16789 #ft/s^2 
        Xc=(m/(rho*Cd*A)*math.log((m*g+0.5*rho*Cd*A*velocity**2)/(m*g)))+alt
        return Xc

if __name__ == "__main__":
    main()
