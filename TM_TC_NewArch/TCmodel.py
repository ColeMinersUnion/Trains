# train_controller/model.py
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot, QTimer
import os

T = 0.125  # Period of control loop in seconds
P_MAX = 120000  # Maximum power output

class TCmodel(QObject):
    power_command = Signal(float)  # Signal to send power command
    ebrake_change = Signal(bool)  # Signal to send emergency brake change to TM
    internal_ebrake_signal = Signal(bool)  # Signal to send emergency brake change to TC view
    headlights_change = Signal(bool)
    lights_signal = Signal(bool)
    left_doors_signal = Signal(bool)
    right_doors_signal = Signal(bool)
    update_current_speed_signal = Signal(float)
    sbrake_change = Signal(bool)
    authority_display = Signal(float)


    def __init__(self):
        super().__init__()
        self.ek = 0
        self.uk = 0
        self.prev_ek = 0
        self.prev_uk = 0
        self.prev_pwr_out = 0
        self.commandedSpeed = 0
        self.currentSpeed = 0
        self.atStation = 0
        self.speedlimits = []
        self.dist = 0
        self.current_speed_limit = 0
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
        self.stopped_by_wayside = 0
        self.approaching = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_countdown)

    @Slot (float)
    def update_acceleration(self, a):
        self.acceleration = a
    
    def timer_countdown(self):
        if self.timer_countdown_value > 0:
            self.timer_countdown_value -= 1
            print(f"Time remaining: {self.timer_countdown_value} seconds")
        else:
            self.timer.stop()  # Stop the timer when it reaches zero
            print("Timer finished.")

    def set_full_authority(self, auth):
        self.full_authority = auth
        #self.calculate_current_authority()
        self.curr_authority = float(self.full_authority.split(';')[0])
        self.curr_dist = self.curr_authority
        print(f"Full authority: {self.full_authority}")
        print(f"Current authority: {self.curr_authority}")
        self.authority_display.emit(self.curr_authority)

    @Slot(float)
    def set_commanded_speed(self, commandedSpeed):
        """ Set the setpoint speed. """
        self.commandedSpeed = commandedSpeed

    @Slot(float)
    def set_current_speed(self, currentSpeed):
        """ Set the current velocity. """
        self.currentSpeed = currentSpeed
        self.update_current_speed_signal.emit(self.currentSpeed)
        print(f"current speed: {self.currentSpeed} m/s")

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

        if (self.approaching >= 1):
            self.pwr = 0
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

    
    @Slot (int)
    def block_switch(self):
        #set current distance to station to next value in authority string
        authority_list = self.full_authority.split(';')
        authority_list.pop(0)
        self.full_authority = ';'.join(authority_list)
        self.curr_authority = float(self.full_authority.split(';')[0])
        self.curr_dist = self.curr_authority
        self.authority_display.emit(float(self.curr_authority))
        #update speed limit
        #self.speedlimits.pop(0)
        #self.current_speed_limit = self.speedlimits[0]
        #print (f"block switched, new speed limit: {self.current_speed_limit}")
        #check underground

    @Slot (list)
    def set_speed_limits(self, speed_limits):
        #take in speed limits
        #define current speed limit value
        self.speedlimits = speed_limits
        print(f"speed limits: {self.speedlimits}")
        self.current_speed_limit = self.speedlimits[0]

    def stopping_dist(self):
        if (self.acceleration == 0):
            self.dist = 1
        else:
           self.dist = (self.currentSpeed*self.currentSpeed)/(2*self.service_brake_deceleration)
           print(f"stopping distance: {self.dist}")
        if (self.curr_dist <= self.dist):
            self.approaching = self.approaching + 1
            print("added to val")
            if (self.approaching == 1):
                self.cut_power_and_enable_brake()
            if (self.approaching >= 2):
                self.dist = 1
                self.pwr = 0
                self.sbrake = True
    
    @Slot (bool)
    def wayside_stop(self, go_nogo):
        #check if wayside stop is enabled
        if (go_nogo == 1):
            self.cut_power_and_enable_brake()
            self.stopped_by_wayside = 1
        else:
            if (self.stopped_by_wayside == 1):
                self.sbrake = 0
                self.commandedSpeed = self.current_speed_limit

    def distance_traveled(self):
        delta_d = self.currentSpeed*T + (0.5*self.acceleration*T*T)
        return delta_d
    
    def dist_from_station(self):
        """ Calculate the distance from the station based on current speed and deceleration. """
        self.curr_dist = self.curr_dist - float(self.distance_traveled())
        if (self.curr_dist < 0):
            self.curr_dist = 0
            self.atStation = self.atStation + 1
            self.station()
        else:
            print(f"Current distance from station: {self.curr_dist:.2f} meters")


    def cut_power_and_enable_brake(self):
        """ Cut power and enable the service brake. """
        self.pwr = 0
        self.sbrake = True #emit signal to try and enable service brake, wait for it back
        self.sbrake_change.emit(self.sbrake)
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
        #emit signal for display
        self.authority_display.emit(self.curr_authority)


        if self.curr_authority <= float(self.full_authority.split(';')[1]):
            authority_list = self.full_authority.split(';')
            authority_list.pop(0)
            self.full_authority = ';'.join(authority_list)

            if float(self.full_authority.split(';')[1]) < float(self.full_authority.split(';')[2]):
                self.curr_authority = 0  # Placeholder for approaching a station
    def station(self):
        #at a station
        if (self.atStation == 1):
            if (self.currentSpeed > 0):
                self.pwr = 0
                self.sbrake = True
                self.set_ebrake_from_driver(True)
                #whatever else to stop immediatly
            else:
                #open correct doors
                #start timer for 60 seconds
                self.left_doors_signal.emit(True)
                self.right_doors_signal.emit(True)
                self.timer_countdown_value = 60  # Set countdown to 60 seconds
                self.timer.start(1000)  # Start the timer with 1-second intervals
                print("Timer started for 60 seconds.")
                #finish station logic
                #emit signal to add passengers?
                #add 25 to auth or some other way to figure that out...maybe go back and redo that authority value
        else:
            self.atStation = 0

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
