import time
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from CombinedBackend import Train
from Testbench  import TestbenchUI
from CommandCenter import CommandCenter
#from TrainModelClass import trainModel
from TrainModelApp import MetricsTab, MainWindow
class combined:
    
    #currentSpeed_signal = pyqtSignal(float)
    def  __init__(self):
        super().__init__()
        self.CC = CommandCenter()
        self.backend =  Train()
        self.train = Train()
        self.testbench = TestbenchUI(self.backend)
        self.main_window =  MainWindow()
        self.metrics = MetricsTab(self.train)
        #self.currentSpeed_signal.connect(self.backend.set_currentSpeed)
        self.metrics.currentSpeed_updated.connect(self.power_loop)


    #compile all inputs, send thru update testbench status?
    def update_values(self):
        currspeed = self.metrics.Train.getCurrentSpeedImperial() #current speed from TM
        full_authority = self.backend.get_authority() #auth from backend
        brake_status = self.train.getServBrakeStatus()
        commandedspeed = self.backend.get_commanded_speed()
        door_status = self.train.leftDoorStatus #change so theres both door thingsb 
        lights_status = self.train.getInternalLightStatus
        temp = self.train.get_temp()
        headlights = self.train.hlStatus()
        speed_limit = self.backend.get_speed_limit() #speed limit from backed
        beacon = self.backend.get_beacon()
        print(f"values updated in combined, current speed: {currspeed}, door status: {door_status}")
        #self.currentSpeed_signal.emit(currspeed)
        self.testbench.submit_from_TM(commandedspeed, full_authority, brake_status, currspeed,  door_status, lights_status, temp, headlights, speed_limit, beacon)

    def power_loop(self, speed):

        #should trigger when a commanded speed is set
        #TM calculates current speed, updates backend
        #output signal saying current speed has been updated
        #signal connects to power function
        #TC power function called, TC generates power command
        #TC emits signal saying power command has been geberated
        #TC sends power command to TM, where testbench input would go
        #
        #currentSpeed = self.train.getCurrentSpeedImperial()

        self.backend.set_currentSpeed(speed)
        self.CC.update_values()
        print(f"update speed in combined, current speed: {speed}")
        self.update_values()
        power_command  = self.backend.get_power_output()
        self.train.set_power_output()
        print(f"updated power command in combined, power being sent: {power_command}")

def main():
    app = QApplication(sys.argv)
    combined_instance = combined()
    combined_instance.CC.show()
    combined_instance.main_window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()