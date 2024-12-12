# train_controller/model.py
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot, QTimer
import os, time as timer

T = 0.125  # Period of control loop in seconds 
P_MAX = 120000  # Maximum power output

class TCmodel(QObject):
    power_command = Signal(float)  # Signal to send power command
    ebrake_change = Signal(bool)  # Signal to send emergency brake change to TM
    internal_ebrake_signal = Signal(bool)  
    #meep meep check on ebrake signals, make sure it does NOT need approval
    internal_sbrake = Signal()
    internal_hl = Signal(bool)
    internal_left_doors = Signal(bool)
    internal_right_doors = Signal(bool)
    internal_lights = Signal(bool)
    headlights_change = Signal(bool)
    lights_signal = Signal(bool)
    left_doors_signal = Signal(bool)
    right_doors_signal = Signal(bool)
    update_current_speed_signal = Signal(float)
    sbrake_change = Signal()
    authority_display = Signal(float)
    speed_limit = Signal(float)
    train_at_yard = Signal()
    gonogo_display = Signal(bool)


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
        self.leaving_station = 0
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
        self.blockID = 0
        self.prev_ID = 0
        self.maxSpeed = 70000 / 3600  # in m/s
        self.maxPower = int(os.getenv("MAX_POWER", 120000))  # in watts
        self.left_doors = False
        self.right_doors = False
        self.headlights = True
        self.lights = False
        self.underground = False
        self.service_brake_deceleration = 1.2  # m/s^2
        self.stopped_by_wayside = 0
        self.approaching = 0
        self.blocks = 0

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.on_timer_timeout)

    @Slot (float)
    def update_acceleration(self, a):
        self.acceleration = a

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
        if (self.stopped_by_wayside == 1):
            self.commanded_speed = 0
        else:
            self.commandedSpeed = commandedSpeed

    @Slot(float)
    def set_current_speed(self, currentSpeed):
        """ Set the current velocity. """
        self.currentSpeed = currentSpeed
        self.update_current_speed_signal.emit(self.currentSpeed)
        #print(f"current speed: {self.currentSpeed} m/s")

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
        #print(f"ek: {self.ek}")

    def set_uk(self):
        """ Update control variable uk. """
        self.uk = self.prev_uk + ((self.a / 2) * (self.ek - self.prev_ek))
        self.prev_uk = self.uk

    @Slot()
    def pid_tick(self):
        """ Perform a PID control loop iteration. """
        self.control_law(self.commandedSpeed, self.currentSpeed)
        self.update_distance()

        if (self.approaching >= 1):
            self.pwr = 0
        self.power_command.emit(self.pwr)
        self.authority_display.emit(self.curr_authority)


    def control_law(self, commandedSpeed, currentSpeed):
        """ PID control law implementation. """
        self.set_ek(commandedSpeed, currentSpeed)
        self.a = T if self.prev_pwr_out < self.maxPower else 0
        self.set_uk()

        self.pwr = (self.Kp * self.ek) + (self.Ki * self.uk)
        self.pwr = min(max(self.pwr, 0), self.maxPower)  # Clamp power between 0 and maxPower

        # Check if the train needs to stop
        if self.pwr < 0:
            self.sbrake_ask(True)
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
    def block_switch(self, id):
        #set current distance to station to next value in authority string
        self.blocks = self.blocks + 1
        self.blockID = id
        print(f" Block ID: {self.blockID}")
        if (self.blockID != self.prev_ID):
            self.next_authority_value()
            self.curr_dist = self.curr_authority
            self.authority_display.emit(float(self.curr_authority))
            self.prev_ID = self.blockID
            #update speed limit
            try:
                self.speedlimits.pop(0)
                self.current_speed_limit = self.speedlimits[0]*0.277778
                print (f"block switched, new speed limit: {self.current_speed_limit}")
                self.speed_limit.emit(self.current_speed_limit)
            except IndexError:
                print("No more speed limits, train is at station")
                self.train_at_yard.emit()
            #check underground
    def next_authority_value(self):
        authority_list = self.full_authority.split(';')
        authority_list.pop(0)
        self.full_authority = ';'.join(authority_list)
        self.curr_authority = float(self.full_authority.split(';')[0])
        print(f"new authority value : {self.curr_authority}")

    @Slot (list)
    def set_speed_limits(self, sl):
        #take in speed limits
        #define current speed limit value
        self.speedlimits = sl
        print(f"speed limits: {self.speedlimits}")
        self.current_speed_limit = self.speedlimits[0]*0.277778

    def stopping_dist(self):
        if (self.acceleration == 0):
            self.dist = 1
        else:
           self.dist = (self.currentSpeed*self.currentSpeed)/(2*self.service_brake_deceleration)
           #print(f"stopping distance: {self.dist}")
        if (self.curr_dist <= self.dist):
            self.approaching = self.approaching + 1
            #print("added to val")
            if (self.approaching == 1):
                self.cut_power_and_enable_brake()
            if (self.approaching >= 2):
                self.dist = 1 #is this needed
                self.pwr = 0
                self.sbrake_ask(True)
    
    @Slot (list)
    def wayside_stop(self, input):
        go_nogo = input[self.blockID]
        print(f"wayside stop: {go_nogo}")
        self.gonogo_display.emit(go_nogo)
        #check if wayside stop is enabled
        if (go_nogo == False):
            self.cut_power_and_enable_brake()
            self.stopped_by_wayside = 1
        else:
            self.sbrake_ask(False)
            self.set_commanded_speed(self.current_speed_limit)
            self.stopped_by_wayside = 0

    def distance_traveled(self):
        delta_d = self.currentSpeed*T + (0.5*self.acceleration*T*T)
        #print(f"current acceleration: {self.acceleration} m/s^2")
        return delta_d
    @Slot ()
    def sbrake_slot(self):
        self.sbrake = not self.sbrake
    

    def dist_from_station(self):
        """ Calculate the distance from the station based on current speed and deceleration. """
        self.curr_dist = self.curr_dist - float(self.distance_traveled())
        if (self.curr_dist <= 0 and self.currentSpeed <= 0.2 and self.leaving_station == False):
            #self.curr_dist = 0
            self.atStation = self.atStation + 1
        elif(self.leaving_station == True):
            self.atStation = 0
            self.leaving_station = False
        #else:
            #print(f"Current distance from station: {self.curr_dist:.2f} meters")
            #print(f"commanded speed: {self.commandedSpeed:.2f} m/s")
            #print(f"pwr output : {self.pwr:.2f} W")
        self.station()

    def cut_power_and_enable_brake(self):
        """ Cut power and enable the service brake. """
        self.pwr = 0
        self.set_commanded_speed(0)
        self.sbrake_ask(True)
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
        #print(f"Current Authority: {self.curr_authority}")
        #emit signal for display
        self.authority_display.emit(self.curr_authority)


        if self.curr_authority <= float(self.full_authority.split(';')[1]):
            authority_list = self.full_authority.split(';')
            authority_list.pop(0)
            self.full_authority = ';'.join(authority_list)

            if float(self.full_authority.split(';')[1]) < float(self.full_authority.split(';')[2]):
                self.curr_authority = 0  # Placeholder for approaching a station
        #print (f"Current Authority: {self.curr_authority}")

    def station(self):
        #at a station
        #print(f"station value: {self.atStation}")
        if (self.atStation == 1):
            if (self.currentSpeed > 0):
                self.pwr = 0
                self.sbrake_ask(True)
                self.set_commanded_speed(0)
                self.set_ebrake_from_driver(True)
                self.atStation = 0 #maybeeee
                #whatever else to stop immediatly
            #open correct doors
            #start timer for 60 seconds
            if (self.currentSpeed <= 0):
                self.currentSpeed = 0
                self.left_doors_signal.emit(True)
                self.right_doors_signal.emit(True)
                #sleep for 60 seconds
                print("stopped at station, Timer started for 60 seconds.")
                self.timer.start(10000) #not 60 seconds yet, put 60000 for 60 sec
        elif (self.leaving_station == True):
            self.sbrake_ask(False)
            self.set_commanded_speed(self.current_speed_limit)

    def on_timer_timeout(self):
        self.atStation = -1 #no longer at station, can resume
        self.set_commanded_speed(self.current_speed_limit)
        self.leaving_station = True
        self.sbrake_ask(False)
        self.approaching = 0
        self.left_doors_signal.emit(False)
        self.right_doors_signal.emit(False)
        print("timer done, doors closed")
        self.curr_dist = self.curr_authority + float(self.full_authority.split(';')[1])
        #print(f"at station: {self.atStation}, current speed: {self.currentSpeed}, approaching: {self.approaching}, leaving : {self.leaving_station}, curr authority : {self.curr_authority}, pwr command: {self.pwr}, commanded speed: {self.commandedSpeed}")



    def toggle_underground(self):
        """ Toggle underground mode and update headlights. """
        self.underground = not self.underground
        self.headlights = self.underground
        self.headlights_change.emit(self.headlights)

    def toggle_left_doors(self):
        """ Toggle the state of the left doors. """
        #self.left_doors = not self.left_doors
        self.left_doors_signal.emit(self.left_doors)

    def toggle_right_doors(self):
        """ Toggle the state of the right doors. """
        #self.right_doors = not self.right_doors
        self.right_doors_signal.emit(self.right_doors)

    def toggle_lights(self):
        """ Toggle the state of the lights. """
        #self.lights = not self.lights
        self.lights_signal.emit(self.lights) 

    def sbrake_ask(self, sb):
        if (self.sbrake != sb):
            self.sbrake_change.emit()

    @Slot (bool)
    def left_doors_slot(self, ld):
        self.left_doors = ld
        self.internal_left_doors.emit(self.left_doors)
    @Slot (bool)
    def right_doors_slot(self, rd):
        self.right_doors = rd
        self.internal_right_doors.emit(self.right_doors)
    @Slot (bool)
    def lights_slot(self, lights):
        self.lights = lights
        self.internal_lights.emit(self.lights)
    @Slot (bool)
    def headlights_slot(self, hl):
        self.headlights = hl
        self.internal_hl.emit(self.headlights)

#meep meep 
    @Slot (bool)
    def sbrake_slot(self, sb):
        self.sbrake = sb
        self.internal_sbrake.emit()
