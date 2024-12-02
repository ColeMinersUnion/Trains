# train_model/model.py
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot
import random, time
T = 0.125  #Period of control loop in seconds
class TrainModel(QObject):
    """ This signal is outgoing to the train controller """
    velocity_updated = Signal(float)  # Signal to send current velocity

    """ This signal is to indicate block change """
    block_change = Signal(int) # Signal to send block change to track model

    """ These signals are for Train Model backend to Train Model View """
    acceleration_updated = Signal(float) # Signal to send acceleration
    passengerCount_updated = Signal(int) # Signal to send passengers onboard
    total_mass_updated = Signal(float)   # Signal to send current mass of train
    temperature_updated = Signal(float)  # Signal to send current temperature
    intLights_updated = Signal(float)    # Signal to update cabin lights
    extLights_updated = Signal(bool)  # Signal to update the headlights
    left_door_updated = Signal(bool) #Signal to toggle left doors
    right_door_updated = Signal(bool) #Signal to toggle right doors
    service_brake_updated = Signal(bool) #Signal to toggle service brake
    
    def __init__(self, routeInfo):
        super().__init__()
        self.vn = 0.0
        self.vn_1 = 0.0
        self.an = 0.00
        self.an_1 = 0.0
        self.maxPower = 120000.0
        self.trainMass = (81800 * 4.44822 / 9.8)
        self.maxSpeed = 700000.0/3600.0
        self.extLightStatus = False
        self.intLightStatus = False
        self.passengerCount = 0
        self.avgHumanMass = (150 * 4.44822 / 9.8) #in kg
        self.totalMass = 0.0
        self.temperature = 65.0
        self.rightDoorStatus = False
        self.leftDoorStatus = False
        self.serviceBrakeStatus = False
        self.routeInfo = routeInfo
        self.blockID = []
        self.blockLength = []
        self.speedLimit = []
        self.totalRouteDistance = 0
        self.totalDistanceTravelled = 0
        self.i = 0
        self.milestoneDistance = 0
        self.parseRouteInfo()
        self.calcTotalMass()

    """ velocity calculation """
    @Slot(float)
    def set_power(self, power: float):

        self.calcTotalMass()
        if self.serviceBrakeStatus:
            self.an = -1.2

            while(self.vn > 0 and self.serviceBrakeStatus):
                self.vn += self.an
                time.sleep(1)

            self.vn = 0.0   
        else:
            """ Simulate the train's response to power. """
            if power <= 0:
                self.an = 0
            if(self.vn <= 0):
                self.an = (self.maxPower / (self.totalMass * self.maxSpeed))
            else: 
                self.an = (power / (self.totalMass * self.vn))
            
            self.vn = self.vn_1 + (T/2) * (self.an + self.an_1)

            self.vn_1 = self.vn
            self.an_1 = self.an

        self.odometer()
        self.checkBlockChange()
        #print("power: ", power, "\tvelocity: ", self.vn, "\tacceleration: ", self.an)
        self.velocity_updated.emit(self.vn)
        self.acceleration_updated.emit(self.an)

    """ Update for passengers of train """
    @Slot(int)
    def updatePassengerCount(self, num: int):
        self.passengerCount += num
        self.passengerCount_updated.emit(self.passengerCount)
        self.calcTotalMass()

    """ Update current mass of train """
    def calcTotalMass(self):
        self.totalMass = self.trainMass + (self.passengerCount * self.avgHumanMass)
        self.total_mass_updated.emit(self.totalMass)

    """ Change cabin temperature """
    @Slot(float)
    def setTemperature(self, temperature: float):
        self.temperature = temperature
        self.temperature_updated(self.temperature)

    """ Toggle for cabin (interior) lights """
    @Slot(bool)
    def toggleInteriorLights(self, input: bool):
        self.intLightStatus = input
        self.intLights_updated.emit(self.intLightStatus)

    """ Toggle for headlights of train """
    @Slot(bool)
    def toggleExteriorLights(self, input: bool):
        self.extLightStatus = input
        self.extLights_updated.emit(self.extLightStatus)

    """ For toggling the left doors (True = Open)"""
    @Slot(bool)
    def toggleLeftDoors(self, input: bool):
        self.leftDoorStatus = input
        self.left_door_updated.emit(self.leftDoorStatus)

        """ For toggling the right doors (True = Open)"""
    @Slot(bool)
    def toggleRightDoors(self, input: bool):
        self.rightDoorStatus = input
        self.right_door_updated.emit(self.rightDoorStatus)

    """ For toggling the service brake (True = On)"""
    @Slot(bool)
    def toggleServiceBrake(self, input: bool):
        self.serviceBrakeStatus = input
        self.service_brake_updated.emit(self.serviceBrakeStatus)

    def parseRouteInfo(self):
        groupedRouteInfo = list(zip(*self.routeInfo))
        self.blockID = groupedRouteInfo[0]
        self.blockLength = groupedRouteInfo[1]
        self.speedLimit = groupedRouteInfo[2]

        self.totalRouteDistance = sum(self.blockLength)

        self.milestoneDistance += self.blockLength[0]

    def odometer(self):
        self.totalDistanceTravelled += self.totalDistanceTravelled + (T/2) * (self.vn + self.vn_1)

    def checkBlockChange(self):
        if(self.milestoneDistance <= self.totalDistanceTravelled):
            self.i += 1
            self.block_change.emit(self.blockID[self.i])
            self.milestoneDistance += self.blockLength[self.i]
