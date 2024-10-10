#take in values
#calculate power from Kp and Ki, put input spots for these on engineer UI
#take inputs from testbench UI that allows for constant update?
#constantly update current temp, speed, power output, 
# backend.py
import os
class Backend:
    def __init__(self):
        self.commanded_speed = 0
        self.authority = 0
        self.brake_status = False
        self.suggested_speed = 0
        self.current_speed = 0
        self.power_output = 0
        self.door_status = False #0 = closed,  1 = open
        self.lights_status = False  #0 = off,  1 = on
        self.internal_temperature = 0
        self.headlights_status = False   #0 = off,  1 = on
        self.Kp = 0
        self.Ki = 0
        self.speed_limit = 0
        #distance to underground


    def set_testbench_inputs(self, commanded_speed, authority, brake_status, suggested_speed, current_speed, power_output, door_status, lights_status, internal_temperature, headlights_status, speed_limit):

        """Set inputs for the testbench."""
        self.commanded_speed = commanded_speed
        self.authority = authority
        self.brake_status = brake_status
        self.suggested_speed = suggested_speed
        self.current_speed = current_speed
        self.power_output = power_output
        self.door_status = door_status
        self.lights_status = lights_status
        self.internal_temperature = internal_temperature
        self.headlights_status = headlights_status
        self.speed_limit =  speed_limit
        #distance to tunnel


    def update_testbench_status(self, commanded_speed, authority, brake_status, suggested_speed,  current_speed, power_output, door_status, lights_status, internal_temperature, headlights_status, speed_limit):
        self.commanded_speed = commanded_speed
        self.authority = authority
        self.brake_status = brake_status 
        self.suggested_speed = suggested_speed
        self.current_speed = current_speed
        self.power_output = power_output
        self.door_status = door_status
        self.lights_status = lights_status
        self.internal_temperature = internal_temperature
        self.headlights_status = headlights_status
        self.speed_limit = speed_limit
        #beacon data

    def get_testbench_status(self):
        """Return the current status of the testbench inputs"""
        return self.commanded_speed, self.authority, self.brake_status, self.suggested_speed, self.current_speed, self.power_output, self.door_status, self.lights_status, self.internal_temperature,  self.headlights_status, self.speed_limit

    
    def set_Kp_Ki(self , Kp, Ki):
        self.Kp = Kp
        self.Ki = Ki

    def get_Kp_Ki(self):
        return  self.Kp, self.Ki
    
    def calculate_braking_dist(self):
        #here is where the braking distance will be calculated,  for now it is just a placeholder
        return 0.0
    
    def safe_speed(self):
        #function that makes sure the current speed is not greater then the speed limit. 
        if (self.commanded_speed >  self.speed_limit):
            self.commanded_speed = self.speed_limit
        return self.commanded_speed
    def stopping_distance(self):
        if (self.brake_status == False):
            if (self.authority <= 10): #choose value that gives train enough time
                #set brake status 
                self.brake_status = True
        return self.brake_status
    def decode_beacons(self):
        #function that decodes the beacons and returns:
        #authority just to make sure it matches
        #distance to underground 
        return self.authority
    
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

    def get_status(self):
        """Returns a status report with calculated values."""
        brake_force = self.calculate_brake_force()
        stop_distance = self.calculate_safe_stop_distance()
        return {
            "Speed": self.commanded_speed,
            "Authority": self.authority,
            "Brake Status": self.brake_status,
            "Brake Force": brake_force,
            "Safe Stop Distance": stop_distance

        }
