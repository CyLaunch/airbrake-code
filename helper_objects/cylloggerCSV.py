#----------------------------------------------------
# CyLogger object, simplifies timestamping and 
# writing to logs. Creates a timestamped logfile .csv excel file with
# timestamped entries. Closes the logger upon removal.
# @Authors Marcus Miller & Bryan Pope
# CyLaunch 2023-24
#----------------------------------------------------

from datetime import datetime
import os
import csv
LOGS_DIR = "/home/cylaunch/logs/"
class cyllogger:
    def __init__(self, name):
        try:
            self.logfile = open(LOGS_DIR + name + datetime.now().strftime("--%Y-%m-%d--%H-%M-%S") + ".csv", "w")   
        except:
            os.mkdir(LOGS_DIR)
            self.logfile = open(LOGS_DIR + name + datetime.now().strftime("--%Y-%m-%d--%H-%M-%S") + ".csv", "w")
    
    def writeTo(self, message):
        writer = csv.writer(self.logfile, delimiter='', quotechar='', quoting=csv.QUOTE_MINIMAL)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        writer.writerow("[" + current_time + "] " + message + "\n")
    
    def __del__(self):
        self.logfile.close()