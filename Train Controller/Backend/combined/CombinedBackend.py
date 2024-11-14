#take in values
#calculate power from Kp and Ki, put input spots for these on engineer UI
#take inputs from testbench UI that allows for constant update?
#constantly update current temp, speed, power output, 
# backend.py
import time
import os  
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
class Train():
    doors_changed = pyqtSignal()
    def __init__(self):
        super().__init__()
	    
        self.commanded_speed = 0
        self.cs_driver = 0
        self.input_authority = "" #sent in from testbench, will be apended/also reps first one
        self.full_authority = "" #takes input_auth and adds to the end
        self.curr_authority = "" #shorter substring with past values deleted
        self.serviceBrake = False
        self.emergencyBrake = False
        self.currentSpeed = 0
        self.prevSpeed = 0
        self.power_output = 0 #send to TM
        #pwr_out for TM becomes power_output
        self.leftDoorStatus = False #0 for closed, 1 for open
        self.rightDoorStatus = False
        self.lights_status = False  #0 = off,  1 = on, these are INTERNAL LIGHTS
        self.temperature = 0
#no longer internal_temp , now just temperature
        self.headlights_status = False   #0 = off,  1 = on
        self.engineFailure = False
        self.signalFailure = False
        self.brakeFailure = False
        self.Kp = 0
        self.Ki = 0
        self.speed_limit = 0
#set change blocks and prev blocks to just block switcj
        self.block_switch = 0 #gets changed when we cross to a new block
        self.prev_block = 1 #needed?
        self.underground = 0
        self.maxPower = int(os.getenv("MAX_POWER", 120000)) # in watts
#replace mx_pwr with maxPower
#no more "mass", now is total mass, train mass, avgHumanMass
        self.maxCapacity = 222
        self.currentCapacity = 0
        self.maxSpeed = (70000 / 3600) #in m/s
        self.avgHumanMass = (150 * 4.44822 / 9.8) #in kg
        self.period = float(os.getenv("PERIOD", 0.1))
        self.polarity = False
        self.ek = 0
        self.uk = 0
        self.prev_ek = 0
        self.prev_uk = 0
        self.prev_pwr_out = 0
        self.prev_time = time.time()
        self.beaconData = "empty"
#beacon is now beaconData 
        self.trainMass = (81800 * 4.44822 / 9.8) #in kg
        self.totalMass = 0
        self.weight = 81800
        self.length = 105.64 #in feet
        self.acceleration = 0
        self.prevAcceleration = 0

#powercommand becomes power_output
        self.powerCheck = False
        self.nextStation = "N/A"
        
 #internallightsstaus becomes lightsstatus
        

        #distance to underground

    def set_commanded_speed(self, cs_sent, cs_driver, speed_limit):
        if (cs_driver == 0):
            self.commanded_speed = cs_sent
        elif (cs_driver > speed_limit):
            #error message to driver ui
            self.commanded_speed = cs_sent
        else: self.commanded_speed = cs_driver

    print("commended speed has been set")


#all authority related functions
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

            if (a == 0):
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
        #for now only opens left doors
        #make sure that power is 0 and brake is on
        self.serviceBrake =  True
        #open doors
        self.leftDoorStatus = True
        #self.doors_changed.emit()
        print ("at station! doors open")
        time.sleep(3.5) 
        print("pretend thats one minute")
        self.leftDoorToggle()
        #self.doors_changed.emit()
        print ("close doors!") 
        if (self.block_switch != self.prev_block):
            authority_list = self.curr_authority.split(';')
            authority_list.pop(0)
            self.curr_authority = ';'.join(authority_list)
            print("next authority")
            self.prev_block = self.change_blocks
        self.serviceBrake = False
#all brake related functions
    def toggle_service_brake(self):
         if self.brakeFailure:
            return
         self.serviceBrake = not self.serviceBrake
    def toggle_ebrake(self):
        self.emergencyBrake = not self.emergencyBrake
    def getServBrakeStatus(self):
        return self.serviceBrake
    def getEBrakeStatus(self):
        return self.emergencyBrake

#lights and doors getters and toggles

#headlights
    def hlToggle(self):
        self.headlights_status = not self.headlights_status

    def hlStatus(self):
        return self.headlights_status
#internal lights (lights)
    def internalLightToggle(self):
        self.lights_status = not self.lights_status

    def getInternalLightStatus(self):
        return self.lights_status
#left door
    def leftDoorToggle(self):
        self.leftDoorStatus = not self.leftDoorStatus

    def getLeftDoorStatus(self):
        return self.leftDoorStatus
#right door
    def rightDoorToggle(self):
        self.rightDoorStatus = not self.rightDoorStatus

    def getRightDoorStatus(self):
        return self.rightDoorStatus
    
    def set_currentSpeed(self, currentSpeed):
        #taken in from TM
        currentSpeed = self.speedCalculations()
        self.currentSpeed = currentSpeed
    
    def set_power_output(self):
        #make another function to send val to TM
        self.power_output = self.power_function(self.commanded_speed, self.currentSpeed, self.Kp, self.Ki)
        self.powerCheck = True

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
        self.beaconData  = beacon

    def get_commanded_speed(self):
        self.currentSpeed = self.speedCalculations()
        return self.commanded_speed

    def get_authority(self):
        return self.curr_authority.split(';')[0]
    
    
    def get_currentSpeed(self):
        print(f"current speed in backend of TC: {self.currentSpeed}")
        return self.currentSpeed
    
    def get_temp(self):
        return self.temperature
    
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
        return self.beaconData
    def set_Kp_Ki(self , Kp, Ki):
        self.Kp = Kp
        self.Ki = Ki
    def set_temp(self, temp):
        self.temperature = temp
    def get_Kp_Ki(self):
        return  self.Kp, self.Ki
    

    def update_testbench_status(self, commanded_speed, full_authority, brake_status,  currentSpeed, door_status, lights_status, temperature, headlights_status, speed_limit, beacon):
        self.set_commanded_speed(commanded_speed, 0, speed_limit)
        self.full_authority = full_authority
        #add to authority value
        self.serviceBrake = brake_status
        self.currentSpeed = currentSpeed
        self.power_function(commanded_speed, currentSpeed, self.Kp, self.Ki)
        self.leftDoorStatus = door_status
        self.lights_status = lights_status
        self.temperature = temperature
        self.headlights_status = headlights_status
        self.speed_limit = speed_limit
        self.beaconData = beacon
        
        #beacon data

    def get_testbench_status(self):
        """Return the current status of the testbench inputs"""
        return self.commanded_speed, self.full_authority, self.serviceBrake, self.currentSpeed, self.leftDoorStatus, self.lights_status, self.temperature,  self.headlights_status, self.speed_limit, self.beaconData

    
    
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
        #self.max_pwr = 70000
        #self.mass = 1000
        current_time = time.time()
        T = current_time - self.prev_time
        self.prev_time = current_time
        #call ek get 
        self.set_ek(commanded_speed, currentSpeed)
        ek = self.get_ek()
        self.set_prev_ek(ek)
        #get prev pwr 
        self.prev_pwr_out = self.get_prev_pwr_out()
        if (self.prev_pwr_out < self.maxPower):
            self.set_uk(self.prev_uk, ek, self.prev_ek, T)
        else: self.set_uk(self.prev_uk, ek, self.prev_ek, 0)
        uk = self.get_uk()
        #if prevpwr < pwrmax then send with all values to uk
        #if >= then send t as 0
        power_out = (Kp*ek) + (Ki*uk)
        if (power_out > self.maxPower):
            power_out = self.maxPower
        elif (power_out < 0):
            self.serviceBrake = True
            self.speedCalculations()
            power_out = 0
        print(f"pwr out: {power_out}")
        return power_out

        #if pcmd >= pmax, then send T value as 0

        #when defines, use getter to get commanded speed
    def setNextStation(self, station):       
        self.nextStation = station
#------------------------------------------------------------------------

    
    def addPassengers(self, input):
        self.currentCapacity = self.currentCapacity + input
    
    def changePolarity(self):
        self.polarity = not self.polarity

    def getPolarity(self):
        return self.polarity

    # Imperial conversions
    def getCurrentSpeedImperial(self):
        return self.currentSpeed * 2.237

    def getAccelerationImperial(self):
        return self.acceleration * 3.28084

    def getWeightImperial(self):
        self.totalMassCalc()
        return self.totalMass * 2.20462

    # System failure toggles
    def activateEngineFailure(self):
        self.engineFailure = not self.engineFailure

    def activateSignalFailure(self):
        self.signalFailure = not self.signalFailure

    def activateBrakeFailure(self):
        self.brakeFailure = not self.brakeFailure

    def totalMassCalc(self):
        self.totalMass = self.trainMass + (self.avgHumanMass * self.currentCapacity)

    # acceleration, power, and velocity calculation

    # calculation for acceleration
    def accelerationCalc(self):
        self.totalMassCalc()
        if(self.currentSpeed == 0):
            self.acceleration = (self.maxPower / (self.totalMass * self.maxSpeed))
        else: 
            self.acceleration = (self.power_output / (self.totalMass * self.currentSpeed))

    # calculation for speed
    def speedCalculations(self):
        
        # Emergency Brake Handling
        if self.emergencyBrake:
            self.acceleration = -2.73
            while self.currentSpeed > 0:

                if self.currentSpeed + self.acceleration < 0:
                    self.currentSpeed = 0
                else:
                    self.currentSpeed += self.acceleration
                time.sleep(1)

            self.acceleration = 0

        # Service Brake Handling
        elif self.serviceBrake:
            self.acceleration = -1.2
            while self.currentSpeed > 0:
                # Check for brake deactivation
                if not self.serviceBrake:
                    self.acceleration = 0
                    break

                if self.currentSpeed + self.acceleration < 0:
                    self.currentSpeed = 0
                else:
                    self.currentSpeed += self.acceleration
                time.sleep(1)

            self.acceleration = 0

        # Engine Failure Handling
        elif self.engineFailure:
            if not self.serviceBrake and not self.emergencyBrake:
                self.acceleration = -0.01
                while self.currentSpeed > 0:
                    # Check for engine failure
                    if not self.engineFailure:
                        self.acceleration = 0
                        break

                    self.currentSpeed += self.acceleration
                    time.sleep(1)

                self.acceleration = 0
                self.currentSpeed = 0

        else:
            
            if(self.powerCheck):
                self.prevAcceleration = self.acceleration
                self.accelerationCalc()

                self.prevSpeed = self.currentSpeed

                self.currentSpeed = self.prevSpeed + (self.period / 2) * (self.acceleration + self.prevAcceleration)

                print(self.getAccelerationImperial())
                self.powerCheck = False
                time.sleep(self.period)
        self.power_function(self.commanded_speed, self.currentSpeed, self.Kp, self.Ki)
        return  self.currentSpeed

