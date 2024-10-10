import time
import math
import os

class trainModel:

    def __init__(self):
        self.trainMass = (81800 * 4.44822 / 9.8) #in kg
        self.totalMass = 0
        self.weight = 81800
        self.length = 105.64 #in feet
        self.acceleration = 0
        self.prevAcceleration = 0
        self.powerCommand = 0
        self.Kp = 50
        self.Ki = 10
        self.nextStation = "N/A"
        self.authority = 0
        self.doorStatus = False
        self.lightStatus = False
        self.engineFailure = False
        self.signalFailure = False
        self.brakeFailure = False
        self.maxCapacity = 222
        self.currentCapacity = 0
        self.maxSpeed = (70000 / 3600) #in m/s
        self.avgHumanMass = (150 * 4.44822 / 9.8) #in kg
        self.maxPower = int(os.getenv("MAX_POWER", 120000)) # in watts
        self.serviceBrake = False
        self.emergencyBrake = False
        self.period = float(os.getenv("PERIOD", 0.1))
        self.prevSignal = 0
        self.prevError = 0
        self.currentSpeed = 0
        self.prevSpeed = 0
        self.goalSpeed = 0
        self.error = 0
        self.temperature = 70 # in fahrenheit

    # Setters and getters
    def setGoalSpeed(self, input):
        if self.signalFailure:
            return
        
        input = input * 0.44704
        
        if(input > self.maxSpeed):
            self.goalSpeed = self.maxSpeed
        else:
            self.goalSpeed = input

    def lightToggle(self):
        self.lightStatus = not self.lightStatus

    def doorToggle(self):
        self.doorStatus = not self.doorStatus

    def setNextStation(self, station):
        if self.signalFailure:
            return
        
        self.nextStation = station

    def servBrakeToggle(self):
        if self.brakeFailure:
            return
        self.serviceBrake = not self.serviceBrake

    def eBrakeToggle(self):
        if self.brakeFailure:
            return
        self.emergencyBrake = not self.emergencyBrake

    def setCommandSpeed(self, input):
        if self.signalFailure:
            print("Signal Faiure ACTIVE")
            return
        self.commandSpeed = input

    def setAuthority(self, input):
        if self.signalFailure:
            print("Signal Faiure ACTIVE")
            return
        self.authority = input

    def setTemp(self, input):
        self.temperature = input
    
    def addPassengers(self, input):
        self.currentCapacity = self.currentCapacity + input

    def getCurrentSpeed(self):
        return self.currentSpeed

    # Imperial conversions
    def getCurrentSpeedImperial(self):
        return self.currentSpeed * 2.237

    def getGoalSpeedImperial(self):
        self.setGoalSpeed(self.goalSpeed)
        return self.goalSpeed * 2.237

    def getAccelerationImperial(self):
        return self.acceleration * 3.28084

    def getWeightImperial(self):
        self.totalMassCalc()
        return self.totalMass * 2.20462
    
    def getLength(self):
        return self.length
    
    def getTemp(self):
        return self.temperature

    # System failure toggles
    def activateEngineFailure(self):
        self.engineFailure = not self.engineFailure

    def activateSignalFailure(self):
        self.signalFailure = not self.signalFailure

    def activateBrakeFailure(self):
        self.brakeFailure = not self.brakeFailure
        # Print statement for debugging

    def totalMassCalc(self):
        self.totalMass = self.trainMass + (self.avgHumanMass * self.currentCapacity)

    # acceleration, power, and velocity calculation

    def setGains(self, Ki, Kp):
        self.Kp = Kp
        self.Ki = Ki

    # calculation for command power
    def commandPowerCalc(self):
        if(self.powerCommand < self.maxPower):
            signal = self.prevSignal + ((self.period / 2) * (self.error + self.prevError))
        else:
            signal = self.prevSignal

        self.powerCommand = (self.Kp * self.error) + (self.Ki * signal)

        self.prevSignal = signal

    # calculation for acceleration
    def accelerationCalc(self):
        self.totalMassCalc()
        if(self.currentSpeed == 0):
            self.acceleration = (self.maxPower / (self.totalMass * self.maxSpeed))
        else: 
            self.acceleration = (self.powerCommand / (self.totalMass * self.currentSpeed))

    # calculation for speed
    def speedCalculations(self):
        tolerance = float(os.getenv("TOLERANCE", 0.01))
        
        while True:
            # Emergency Brake Handling
            if self.emergencyBrake:
                self.acceleration = -2.73
                while self.currentSpeed > 0:

                    if not self.emergencyBrake:
                        self.acceleration = 0
                        break

                    if self.currentSpeed + self.acceleration < 0:
                        self.currentSpeed = 0
                    else:
                        self.currentSpeed += self.acceleration
                    time.sleep(1)
                    self.goalSpeed = self.currentSpeed

                self.acceleration = 0
                break

            # Service Brake Handling
            elif self.serviceBrake:
                self.acceleration = -1.2
                while self.currentSpeed > 0:

                    if not self.serviceBrake:
                        self.acceleration = 0
                        break

                    if self.currentSpeed + self.acceleration < 0:
                        self.currentSpeed = 0
                    else:
                        self.currentSpeed += self.acceleration
                    time.sleep(1)
                    self.goalSpeed = self.currentSpeed

                self.acceleration = 0
                break

            # Engine Failure Handling
            elif self.engineFailure:
                if not self.serviceBrake and not self.emergencyBrake:
                    self.acceleration = -0.01
                    while self.currentSpeed > 0:

                        if not self.engineFailure:
                            self.acceleration = 0
                            break

                        self.currentSpeed += self.acceleration
                        time.sleep(1)

                    self.acceleration = 0
                    self.currentSpeed = 0

            else:
                if(self.goalSpeed > self.maxSpeed):
                    self.goalSpeed = self.maxSpeed
                
                if abs(self.goalSpeed - self.currentSpeed) <= tolerance:
                    break

                self.prevError = self.error
                self.error = self.goalSpeed - self.currentSpeed
                self.commandPowerCalc()

                self.prevAcceleration = self.acceleration
                self.accelerationCalc()

                self.prevSpeed = self.currentSpeed

                self.currentSpeed = self.prevSpeed + (self.period / 2) * (self.acceleration + self.prevAcceleration)

                #print(self.getAccelerationImperial())
                time.sleep(self.period)

    # used to check if service brake needs to turn on
    def authorityCalc(self):
        distanceToZero = ((self.currentSpeed) ** 2) /(2 * 1.2)

        if(distanceToZero > self.authority):
            if(self.serviceBrake == False):
                self.servBrakeToggle(self)
            
            while(self.currentSpeed != 0):
                self.currentSpeed = self.currentSpeed - 1.2
                time.sleep(1)