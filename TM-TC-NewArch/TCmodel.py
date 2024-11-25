# train_controller/model.py
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot
import os
import sys
from PyQt6.QtWidgets import QApplication

T = 0.125  #Period of control loop in seconds
P_MAX = 120000  #Maximum power output
class TCmodel(QObject):
    power_command = Signal(float)  # Signal to send power command

    def __init__(self):
        super().__init__()
        self.ek = 0
        self.uk = 0
        self.prev_ek = 0
        self.prev_uk = 0
        self.prev_pwr_out = 0
        self.commandedSpeed = 0
        self.currentSpeed = 0
        self.ebrake = False
        self.sbrake = False
        self.pwr = 0
        self.Kp = 0
        self.Ki = 0
        self.a = 0
        self.acceleration = 0
        self.full_authority = "" #full string to append to
        self.curr_authority = 0
        self.maxSpeed = (70000 / 3600) #in m/s
        self.maxPower = int(os.getenv("MAX_POWER", 120000)) # in watts
    
    @Slot(float)
    def set_commanded_speed(self, commandedSpeed):
        """ Set the setpoint speed. """
        self.commandedSpeed = commandedSpeed
    @Slot(float)
    def set_current_speed(self, currentSpeed):
        """ Set the current velocity. """
        self.currentSpeed = currentSpeed
    @Slot(bool)
    def set_ebrake(self, ebrake):
        """ Set the emergency brake flag. """
        self.ebrake = ebrake
        print (f"ebrake has been set to:{ebrake}")
        #add signal here later
    

    def set_ek(self, commandedSpeed, currentSpeed):
        self.ek = commandedSpeed - currentSpeed
        #print(f"ek: {self.ek}")

    def set_uk(self):
        #will work if T is 0 for pcmd < pmax
        self.uk = self.prev_uk + ((self.a/2)*(self.ek -  self.prev_ek))
        #print(f"uk: {self.uk}")
        
    @Slot()
    def pid_tick(self):
        """ Perform a PID control loop iteration. """
        #call PID function
        self.control_law(self.commandedSpeed, self.currentSpeed)
        #emit power command
        self.power_command.emit(self.pwr)

    def control_law(self, commandedSpeed, currentSpeed):
        #PID function
        #self.max_pwr = 70000
        #self.mass = 1000
        #use global T for period

        #call ek get 
        self.set_ek(commandedSpeed, currentSpeed)
        if (self.prev_pwr_out < self.maxPower):
            self.a = T
        else: self.a = 0
        self.set_uk()


        #if prevpwr < pwrmax then send with all values to uk
        #if >= then send t as 0
        self.pwr = (self.Kp*self.ek) + (self.Ki*self.uk)
        if (self.pwr > self.maxPower):
            self.pwr = self.maxPower
        elif (self.pwr < 0):
            self.sbrake = True
            self.pwr = 0

        #if pcmd >= pmax, then send T value as 0
    
    def calculate_current_authority(self):
        #distance equation
        self.curr_authority = self.currentSpeed + (0.5*self.acceleration*T*T)
        #display current authority
        if (self.curr_authority <= self.full_authority.split(';')[1]):
            #emit signal to change block
            #emit signal that authority has been changed 
            authority_list = self.full_authority.split(';')
            authority_list.pop(0)
            self.full_authority = ';'.join(authority_list)

            #figure out if im near a station, ex 150;100;50;25;200
            if (int(self.full_authority.split(';')[1]) < int(self.full_authority.split(';')[2])):
                #approaching a station
                # 
                self.curr_authority = 0 #placeholder
