#take in values
#calculate power from Kp and Ki, put input spots for these on engineer UI
#take inputs from testbench UI that allows for constant update?
#constantly update current temp, speed, power output, 
# backend.py
import time
import os  
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
class Backend(QObject):
    doors_changed = pyqtSignal()
    def __init__(self):
        super().__init__()
        #define output signals for:
        #brake command
        #power output
        
        #lights
        #headlights

        #input signals for 
        #commanded speed
        #beacon data
        #status?doors/lights/hls

        
        self.commanded_speed = 0
        self.cs_driver = 0
        self.input_authority = "" #sent in from testbench, will be apended/also reps first one
        self.full_authority = "" #takes input_auth and adds to the end
        self.curr_authority = "" #shorter substring with past values deleted
        self.brake_status = False
        self.currentSpeed = 0
        self.power_output = 0 #send to TM
        self.door_status = False #0 = closed,  1 = open
        self.lights_status = False  #0 = off,  1 = on
        self.internal_temperature = 0
        self.headlights_status = False   #0 = off,  1 = on
        self.Kp = 0
        self.Ki = 0
        self.speed_limit = 0
        self.change_blocks = 0
        self.prev_block = 1
        self.underground = 0
        self.max_pwr = 70000 #in watts, constant
        self.mass = 10 #change number when given
        self.ek = 0
        self.uk = 0
        self.prev_ek = 0
        self.prev_uk = 0
        self.prev_time = time.time()
        self.prev_pwr_out = 0
        self.block_switch = 0 #gets changed when we cross to a new block
        self.beacon = ""

        #distance to underground

    def set_commanded_speed(self, cs_sent, cs_driver, speed_limit):
        if (cs_driver == 0):
            self.commanded_speed = cs_sent
        elif (cs_driver > speed_limit):
            #error message to driver ui
            self.commanded_speed = cs_sent
        else: self.commanded_speed = cs_driver
    print("commended speed has been set")

    def add_to_authority(self, input_authority, full_authority, curr_authority):
        #if input isnt 0 and isnt current full, then add it
        if (input_authority != "" and input_authority != full_authority):
            self.full_authority = full_authority + input_authority
            self.curr_authority = curr_authority + input_authority
            print("added to authority")
    
    def next_authority(self, curr_authority, change_blocks, prev_block):
        if (change_blocks != prev_block):
            authority_list = curr_authority.split(';')
            authority_list.pop(0)
            self.curr_authority = ';'.join(authority_list)
            print("next authority")
            self.prev_block = change_blocks

            a = int(self.curr_authority.split(';')[0])
            print(f"int value for curr auth: {a}")

            if (a  == 0):
                self.at_station()
            if (int(self.curr_authority.split(';')[0]) <= 50):
                self.commanded_speed = 0
                self.brake_status  = True
        
            #send only first val?

    def set_original_authority(self, full_authority):
        self.full_authority = full_authority
        self.curr_authority = full_authority
        

        #i have "offical" authority array, then current array that starts with current val 
        #read in from preloaded string (string, sep by semicolons ;)
        #if im at the last value then im done!
        #if i get sent a new one, add it to the end of mine 
        #delete first value from current authority string
        #update current authority array 
        #read first value and set authoryt to that
        
        #for testing, testbench submits it first once, if its 0 then ignore, set my current string to empty and have any new input added to the end
        #doors only open when theres no more authority in updated authority array
        #if authority is 0 and theres not emergency thing then call a functuon that opens doors for 60 sec then closes
        #get authority length from subtracting

    def at_station(self):
        #make sure that power is 0 and brake is on
        self.brake_status =  True
        #open doors
        self.set_door_status(True)
        self.doors_changed.emit()
        print ("at station! doors open")
        time.sleep(3.5) 
        print("pretend thats one minute")
        self.set_door_status(False)
        self.doors_changed.emit()
        print ("close doors!")
        if (self.change_blocks != self.prev_block):
            authority_list = self.curr_authority.split(';')
            authority_list.pop(0)
            self.curr_authority = ';'.join(authority_list)
            print("next authority")
            self.prev_block = self.change_blocks
        self.brake_status = False
    
    def set_brake_status(self, brake_driver, brake_status):
        if (brake_driver == 1):
            self.brake_status = True
        elif (brake_status == 1):
            self.brake_status = True
        else:  self.brake_status = False
    

    def set_currentSpeed(self, currentSpeed):
        #taken in from TM
        self.currentSpeed = currentSpeed
    
    def set_lights(self, lights_status):
        #driver override avail
        self.lights_status = lights_status
    
    def set_power_output(self):
        #make another function to send val to TM
        self.power_output = self.power_function(self.commanded_speed, self.currentSpeed, self.Kp, self.Ki)


    def set_door_status(self, status):
        self.door_status = status
    
    def set_headlights_status(self, headlights_status):
        #set to 1 if underground = 1
        self.headlights_status = headlights_status

    def set_ek(self, commanded_speed, currentSpeed):
        self.ek = commanded_speed - currentSpeed

    def set_prev_ek(self, ek):
        self.prev_ek = ek

    def set_prev_uk(self, uk):
        self.prev_uk = uk

    def set_uk(self, prev_uk, ek, prev_ek,T ):
        #will work if T is 0 for pcmd < pmax
        self.uk = prev_uk + ((T/2)*(ek -  prev_ek))

    def set_prev_pwr_out(self, pwr):
        self.prev_pwr_out = pwr

    def set_beacon(self, beacon):
        self.beacon  = beacon


    def get_commanded_speed(self):
        return self.commanded_speed

    def get_authority(self):
        return self.curr_authority.split(';')[0]
    
    def get_brake(self):
        #get brake value from stopping_distance?
        return self.brake_status
    
    def get_currentSpeed(self):
        print(f"current speed in backend of TC: {self.currentSpeed}")
        return self.currentSpeed
    
    def get_internal_temp(self):
        return self.internal_temperature
    
    def get_lights(self):
        return self.lights_status
    
    def get_power_output(self):
        return self.power_output
    
    def get_doors(self):
        return self.door_status
    
    def get_hl(self):
        return self.headlights_status
    
    def get_speed_limit(self):
        return self.speed_limit

    def get_ek(self):
        return self.ek
    def get_uk(self):
        return self.uk
    def get_prev_ek(self):
        return self.prev_ek
    def get_prev_uk(self):
        return self.prev_uk
    def get_prev_pwr_out(self):
        return self.prev_pwr_out 
    def get_beacon(self):
        return self.beacon
    

    def update_testbench_status(self, commanded_speed, full_authority, brake_status,  currentSpeed, door_status, lights_status, internal_temperature, headlights_status, speed_limit, beacon):
        self.commanded_speed = commanded_speed
        self.full_authority = full_authority
        #add to authority value
        self.brake_status = brake_status 
        self.currentSpeed = currentSpeed
        self.power_function(commanded_speed, currentSpeed, self.Kp, self.Ki)
        self.door_status = door_status
        self.lights_status = lights_status
        self.internal_temperature = internal_temperature
        self.headlights_status = headlights_status
        self.speed_limit = speed_limit
        self.beacon = beacon
        
        #beacon data

    def get_testbench_status(self):
        """Return the current status of the testbench inputs"""
        return self.commanded_speed, self.full_authority, self.brake_status, self.currentSpeed, self.door_status, self.lights_status, self.internal_temperature,  self.headlights_status, self.speed_limit, self.beacon

    
    def set_Kp_Ki(self , Kp, Ki):
        self.Kp = Kp
        self.Ki = Ki

    def get_Kp_Ki(self):
        return  self.Kp, self.Ki
    
    
    def safe_speed(self):
        #function that makes sure the current speed is not greater then the speed limit. 
        if (self.commanded_speed >  self.speed_limit):
            self.commanded_speed = self.speed_limit
        return self.commanded_speed
    
    
    def decode_beacons(self, beacon):
        #decode
        #assuming the following format:
        #first value is how many blocks until next stop 
        #could do arrays of that size and load in, or just have as vectors>
        #assume seperated by semicolons, with full things seperated by ??
        #n = #first val, everything until first [
        #underground = [n] #array with size n
        #name = "" #station name
        #speed_limits = [n] #array with size n
        #authorities = [n]
        #doors = [4]

        #for now, assume just brought in as inputs 
        return 0


    def underground_status(self):
        #if the distance to underground = 0
        #turn on headlights
        
        #subtract distance to underground from authority
        #if value = 0, turn on headlights

        return 0.0
    
    def calculate_brake_force(self):
        """Example calculation based on brake status and speed."""
        if self.brake_status:
            return self.commanded_speed * 0.5  # Sample logic: brake force is proportional to speed
        return 0  # No braking

    def calculate_safe_stop_distance(self):
        """Calculate the safe stopping distance based on speed and authority."""
        return (self.commanded_speed ** 2) / (2 * self.authority) if self.authority != 0 else float('inf')


    def power_function(self, commanded_speed, currentSpeed, Kp, Ki):
        self.max_pwr = 70000
        self.mass = 1000
        current_time = time.time()
        T = current_time - self.prev_time
        self.prev_time = current_time
        #call ek get 
        self.set_ek(commanded_speed, currentSpeed)
        ek = self.get_ek()
        self.set_prev_ek(ek)

        #get prev pwr 
        self.prev_pwr_out = self.get_prev_pwr_out()
        if (self.prev_pwr_out < self.max_pwr):
            self.set_uk(self.prev_uk, ek, self.prev_ek, T)
        else: self.set_uk(self.prev_uk, ek, self.prev_ek, 0)
        uk = self.get_uk()
        #if prevpwr < pwrmax then send with all values to uk
        #if >= then send t as 0
        power_out = (Kp*ek) + (Ki*uk)
        if (power_out < 0):
            self.brake_status = True
            power_out = 0
        print(f"pwr out: {power_out}")
        return power_out

        #if pcmd >= pmax, then send T value as 0

        #when defines, use getter to get commanded speed

