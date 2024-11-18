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
        self.powerCheck = False
        self.nextStation = "N/A"
        self.leftDoorStatus = False
        self.rightDoorStatus = False
        self.lightStatus = False
        self.internalLightStatus = False
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
        self.currentSpeed = 0
        self.prevSpeed = 0
        self.beaconData = "empty"
        self.polarity = False
        self.temperature = 70 # in fahrenheit

    def lightToggle(self):
        self.lightStatus = not self.lightStatus

    def getExternalLightStatus(self):
        return self.lightStatus

    def internalLightToggle(self):
        self.internalLightStatus = not self.internalLightStatus

    def getInternalLightStatus(self):
        return self.internalLightStatus

    def leftDoorToggle(self):
        self.leftDoorStatus = not self.leftDoorStatus

    def getLeftDoorStatus(self):
        return self.leftDoorStatus

    def rightDoorToggle(self):
        self.rightDoorStatus = not self.rightDoorStatus

    def getRightDoorStatus(self):
        return self.rightDoorStatus

    def setNextStation(self, station):       
        self.nextStation = station

    def setPowerCommand(self, input):
        if(input > self.maxPower):
            self.powerCommand = self.maxPower
        else:
            self.powerCommand = input

        self.powerCheck = True

    def getPowerCommand(self):
        return self.powerCommand

    def servBrakeToggle(self):
        if self.brakeFailure:
            return
        self.serviceBrake = not self.serviceBrake

    def getServBrakeStatus(self):
        return self.serviceBrake

    def eBrakeToggle(self):
        self.emergencyBrake = not self.emergencyBrake

    def setTemp(self, input):
        self.temperature = input
    
    def addPassengers(self, input):
        self.currentCapacity = self.currentCapacity + input

    def getCurrentSpeed(self):
        return self.currentSpeed
    
    def setBeaconData(self, input):
        self.beaconData = input
    
    def getBeaconData(self):
        return self.beaconData
    
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
    
    def getTemp(self):
        return self.temperature

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
            self.acceleration = (self.powerCommand / (self.totalMass * self.currentSpeed))

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

    def avgDistance(self):
        distance = self.period * self.currentSpeed
        return distance