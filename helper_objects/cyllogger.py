#----------------------------------------------------
# CyLogger object, simplifies timestamping and 
# writing to logs. Creates a timestamped logfile with
# timestamped entries. Closes the logger upon removal
# @Author bdpope
# CyLaunch 2023-24
#----------------------------------------------------

from datetime import datetime
import os
LOGS_DIR = "/home/cylaunch/logs/"
class cyllogger:
    def __init__(self, name):
        self.filePath = LOGS_DIR + name + datetime.now().strftime("--%Y-%m-%d--%H-%M-%S") + ".txt"
        try:
           self.fd = os.open(self.filePath, os.O_CREAT | os.O_NONBLOCK | os.O_APPEND)
        except:
            os.mkdir("/home/cylaunch/logs/")
            self.fd = os.open(self.filePath, os.O_CREAT | os.O_NONBLOCK | os.O_APPEND)
    
    def writeTo(self, message):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        os.write( self.fd, "[" + current_time + "] " + str(message) + "\n")
    
    def __del__(self):
        os.close(self.fd)