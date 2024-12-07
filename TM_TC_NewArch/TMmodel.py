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
    emergency_brake_updated = Signal(bool) #Signal to communicate emergency brake status
    signal_failure = Signal(bool)   # Signal for signal failure
    engine_failure = Signal(bool)   # Signal for engine failure
    brake_failure = Signal(bool)    # Signal for brake failure
    speed_limits = Signal(list)     # speed limits for train controller
    
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
        self.emergencyBrakeStatus = False
        self.brakeFailureStatus = False
        self.signalFailureStatus = False
        self.engineFailureStatus = False
        self.routeInfo = routeInfo
        self.blockID = []
        self.blockLength = []
        self.speedLimit = []
        self.totalRouteDistance = 0
        self.totalDistanceTravelled = 0
        self.i = 0
        self.milestoneDistance = 0
        self.currentBeaconInfo = "null"
        self.parseRouteInfo()
        self.calcTotalMass()

    """ velocity calculation """
    @Slot(float)
    def set_power(self, power: float):

        self.calcTotalMass()
        
        if self.serviceBrakeStatus and (not self.brakeFailureStatus):

            if(self.vn > 0):
                self.an = (-1.2 / 8)
                self.vn += self.an
            else:
                self.an = 0
                self.vn = 0.0

        elif self.emergencyBrakeStatus:

            if(self.vn > 0):
                self.an = (-2.73 / 8)
                self.vn += self.an
            else:
                self.an = 0
                self.vn = 0.0

        else:
            """ Simulate the train's response to power. """
            if power <= 0:
                self.an = 0
                self.vn = 0
            else:
                if(power > self.maxPower):
                    power = self.maxPower

                if(self.vn <= 0):
                    self.an = (self.maxPower / (self.totalMass * self.maxSpeed))
                else: 
                    self.an = (power / (self.totalMass * self.vn))

                self.vn = self.vn_1 + (T/2) * (self.an + self.an_1)

            #print(self.vn)

            self.vn_1 = self.vn
            self.an_1 = self.an

        self.odometer()
        self.checkBlockChange()
        #print("power: ", power, "\tvelocity: ", self.vn, "\tacceleration: ", self.an)
        self.velocity_updated.emit(self.vn)
        self.acceleration_updated.emit(self.an)

    """ Update for passengers of train """
    @Slot()
    def updatePassengerCount(self):
        self.passengerCount += 8
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
        self.temperature_updated.emit(self.temperature)

    """ Toggle for cabin (interior) lights """
    @Slot()
    def toggleInteriorLights(self):
        self.intLightStatus = not self.intLightStatus
        self.intLights_updated.emit(self.intLightStatus)

    """ Toggle for headlights of train """
    @Slot()
    def toggleExteriorLights(self):
        self.extLightStatus = not self.extLightStatus
        self.extLights_updated.emit(self.extLightStatus)

    """ For toggling the left doors (True = Open)"""
    @Slot()
    def toggleLeftDoors(self):
        self.leftDoorStatus = not self.leftDoorStatus
        self.left_door_updated.emit(self.leftDoorStatus)

        """ For toggling the right doors (True = Open)"""
    @Slot()
    def toggleRightDoors(self):
        self.rightDoorStatus = not self.rightDoorStatus
        self.right_door_updated.emit(self.rightDoorStatus)

    """ For toggling the service brake (True = On)"""
    @Slot()
    def toggleServiceBrake(self):
        if(not self.brakeFailureStatus):
            self.serviceBrakeStatus = not self.serviceBrakeStatus
            self.service_brake_updated.emit(self.serviceBrakeStatus)

    """ For toggling the emergency brake """
    @Slot()
    def toggleEmergencyBrake(self):
        self.emergencyBrakeStatus = not self.emergencyBrakeStatus
        self.emergency_brake_updated.emit(self.emergencyBrakeStatus)

    """ Parsing the route information the train is initialized with """
    def parseRouteInfo(self):
        groupedRouteInfo = list(zip(*self.routeInfo))
        self.blockID = groupedRouteInfo[0]
        self.blockLength = groupedRouteInfo[1]
        self.speedLimit = groupedRouteInfo[2]

        #send speed limits to train controller here
        self.speed_limits.emit(self.speedLimit)

        self.milestoneDistance += self.blockLength[0]

    """ built in odometer, uses the distance travelled to calculate if the block changes """
    def odometer(self):
        self.totalDistanceTravelled += (T/2) * (self.vn + self.vn_1)

    def checkBlockChange(self):
        #print(self.totalDistanceTravelled)
        #print(self.milestoneDistance)
        if(self.milestoneDistance < self.totalDistanceTravelled):
            self.i += 1
            self.block_change.emit(self.blockID[self.i])
            self.milestoneDistance += self.blockLength[self.i]

    #@Slot(str)
    #def beaconIntake(self, beacon: str):
        

    """ Failure (Murphy) toggles are the next three slot functions here """
    @Slot()
    def toggleBrakeFailure(self):
        self.brakeFailureStatus = not self.brakeFailureStatus
        self.brake_failure.emit(self.brakeFailureStatus)

    @Slot()
    def toggleEngineFailure(self):
        self.engineFailureStatus = not self.engineFailureStatus
        self.engine_failure.emit(self.engineFailureStatus)

    @Slot()
    def toggleSignalFailure(self):
        self.signalFailureStatus = not self.signalFailureStatus
        self.signal_failure.emit(self.signalFailureStatus)