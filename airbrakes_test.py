from airbrake import airbrake

ab = airbrake()
char = 'z'
choice = input("Welcome to the airbrake test function! What would you like? \n 1. Read from sensors\n 2. Servo Control\n")
if(choice == '1'):
    while(char != 'q'):
        char = input("a for accelerometer, b for barometer, m for magnitude of acceleration, d for launch detection, q to quit\n")
        if(char == 'a'):
            while True:
                print(ab.get_accel_mag())
        elif(char == 'b'):
            while True:
                print(ab.get_altitude())
        elif(char == 'm'):
            while True:
                print(str(ab.get_accel_mag()) + "\r")
        elif(char == 'd'):
            while True:
                print(str(ab.detect_launch()) + "\r")

elif(choice == '2'):
    while(char != 'q'):
        char = input("q for quit, o for open, c for close\n")
        if(char == 'o'):
            print("opening airbrakes\n")
            ab.deploy_airbrakes()
        elif(char == 'c'):
            print("closing airbrakes\n")
            ab.retract_airbrakes()