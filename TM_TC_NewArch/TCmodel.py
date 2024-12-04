# train_controller/model.py
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot
import os

T = 0.125  # Period of control loop in seconds
P_MAX = 120000  # Maximum power output

class TCmodel(QObject):
    power_command = Signal(float)  # Signal to send power command
    update_auth = Signal(str)  # Signal to update authentication status
    ebrake_change = Signal(bool)  # Signal to send emergency brake change to TM
    internal_ebrake_signal = Signal(bool)  # Signal to send emergency brake change to TC view
    headlights_change = Signal(bool)
    lights_signal = Signal(bool)
    left_doors_signal = Signal(bool)
    right_doors_signal = Signal(bool)
    update_current_speed_signal = Signal(float)

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
        self.full_authority = ""  # Full string for authority
        self.curr_authority = 0 #next value in string
        self.curr_dist = 0 #value that gets subtracted from and counts down
        self.block_length = 0
        self.maxSpeed = 70000 / 3600  # in m/s
        self.maxPower = int(os.getenv("MAX_POWER", 120000))  # in watts
        self.left_doors = False
        self.right_doors = False
        self.headlights = False
        self.lights = False
        self.underground = False
        self.service_brake_deceleration = 1.2  # m/s^2

    def set_full_authority(self, auth):
        self.full_authority = auth
        #self.calculate_current_authority()
        self.curr_authority = float(self.full_authority.split(';')[0])
        self.curr_dist = self.curr_authority
        print(f"Full authority: {self.full_authority}")
        print(f"Current authority: {self.curr_authority}")
        self.update_auth.emit(auth)  # Emit signal to update UI

    @Slot(float)
    def set_commanded_speed(self, commandedSpeed):
        """ Set the setpoint speed. """
        self.commandedSpeed = commandedSpeed

    @Slot(float)
    def set_current_speed(self, currentSpeed):
        """ Set the current velocity. """
        self.currentSpeed = currentSpeed
        self.update_current_speed_signal.emit(self.currentSpeed)

    @Slot(bool)
    def set_ebrake(self, ebrake):
        """ Set emergency brake state. """
        self.ebrake = ebrake
        self.internal_ebrake_signal.emit(ebrake)

    @Slot(bool)
    def set_ebrake_from_driver(self, ebrake):
        """ Set emergency brake state from driver input. """
        self.ebrake = ebrake
        self.ebrake_change.emit(ebrake)

    @Slot(float)
    def set_Kp(self, kp):
        self.Kp = kp
        print(f"Kp: {self.Kp}")

    @Slot(float)
    def set_Ki(self, ki):
        self.Ki = ki
        print(f"Ki: {self.Ki}")

    def set_ek(self, commandedSpeed, currentSpeed):
        self.ek = commandedSpeed - currentSpeed

    def set_uk(self):
        """ Update control variable uk. """
        self.uk = self.prev_uk + ((self.a / 2) * (self.ek - self.prev_ek))

    @Slot()
    def pid_tick(self):
        """ Perform a PID control loop iteration. """
        self.control_law(self.commandedSpeed, self.currentSpeed)
        self.update_distance()
        self.power_command.emit(self.pwr)

    def control_law(self, commandedSpeed, currentSpeed):
        """ PID control law implementation. """
        self.set_ek(commandedSpeed, currentSpeed)
        self.a = T if self.prev_pwr_out < self.maxPower else 0
        self.set_uk()

        self.pwr = (self.Kp * self.ek) + (self.Ki * self.uk)
        self.pwr = min(max(self.pwr, 0), self.maxPower)  # Clamp power between 0 and maxPower

        # Check if the train needs to stop
        if self.pwr < 0:
            self.sbrake = True
            self.pwr = 0

        # Calculate the distance from the station based on the current speed and stopping distance
        

    def update_distance(self):
        #calculate delta d
        self.distance_traveled()
        #update current distance from station
        self.dist_from_station()
        #check for block change, replace value with new one if necessary
        #calculate stopping distance
        self.stopping_dist()
        #check if it matches current distance from train (stopping distance should be GREATER or equal )
        #if matches, cut power and enable brake
    #@Slot ()
    #def block_switch(self):
        #set current distance to station to next value in authority string
        #pop authority string
    def stopping_dist(self):
        if (self.acceleration <= 1):
            dist = 1
        else:
            dist = (self.currentSpeed*self.currentSpeed)/(2*self.acceleration)
        if (self.curr_dist <= dist):
            self.cut_power_and_enable_brake
            print("cut power and enabled brake")

    def distance_traveled(self):
        delta_d = self.currentSpeed*T + (0.5*self.acceleration*T*T)
        return delta_d
    
    def dist_from_station(self):
        """ Calculate the distance from the station based on current speed and deceleration. """
        self.curr_dist = self.curr_dist - self.distance_traveled()
        if (self.curr_dist < 0):
            self.curr_dist = 0
        print(f"Current distance from station: {self.curr_dist} meters")

    def cut_power_and_enable_brake(self):
        """ Cut power and enable the service brake. """
        self.pwr = 0
        self.sbrake = True
        print("Power cut and service brake enabled.")

    #def set_block_length(self):
     #   """ Set the block length based on authority values. """
      #  auth_list = self.full_authority.split(';')
      #  if len(auth_list) < 1:
      #      self.block_length = 10  # Default value
      #  else:
      #      self.block_length = int(auth_list[0]) if int(auth_list[1]) < int(auth_list[2]) else int(auth_list[0]) - int(auth_list[1])

    def calculate_current_authority(self):
        """ Calculate the current authority based on speed and acceleration. """
        self.curr_authority = self.currentSpeed * T + (0.5 * self.acceleration * T * T)
        print(f"Current Authority: {self.curr_authority}")

        if self.curr_authority <= float(self.full_authority.split(';')[1]):
            authority_list = self.full_authority.split(';')
            authority_list.pop(0)
            self.full_authority = ';'.join(authority_list)

            if int(self.full_authority.split(';')[1]) < int(self.full_authority.split(';')[2]):
                self.curr_authority = 0  # Placeholder for approaching a station


    def toggle_underground(self):
        """ Toggle underground mode and update headlights. """
        self.underground = not self.underground
        self.headlights = self.underground
        self.headlights_change.emit(self.headlights)

    def toggle_left_doors(self):
        """ Toggle the state of the left doors. """
        self.left_doors = not self.left_doors
        self.left_doors_signal.emit(self.left_doors)

    def toggle_right_doors(self):
        """ Toggle the state of the right doors. """
        self.right_doors = not self.right_doors
        self.right_doors_signal.emit(self.right_doors)

    def toggle_lights(self):
        """ Toggle the state of the lights. """
        self.lights = not self.lights
        self.lights_signal.emit(self.lights)
