from Train import Train
from TrainSchedule import TrainSchedule
from Schedule import Schedule
from ScheduleParser import readSchedule

#! Top level Backend object to be instantiated in the application. 
#? ALso should become a singleton when I learn how those work
class CTC_Office:
    _instance = None
    #Set switch manually in maintenance mode.
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CTC_Office, cls).__new__(cls)
            # Put any initialization here.
            cls.line = {}              #Graph
            cls.Schedule = {}  #Schedule
            cls.num_trains = 0         #int
            cls.nextID = 0
        return cls._instance
        
    def addBlueLine(cls):
        try:
            from GetBlue import Blue
            cls.line["Blue"] = Blue(broken=False)
            return True
        except:
            print("Blue Line Init Failed")
            return False
        
    def addGreenLine(cls):
        try:
            from GetGreen import Green
            cls.line["Green"] = Green()
            return True
        except:
            print("Green Line Init Failed")
            return False
    
    def addRedLine(cls):
        return True
    
    def uploadSchedule(cls, fn):
        TrainList = readSchedule(fn)
        for t in TrainList:
            tempSchedule = TrainSchedule(t["Line"], t["Stations"])
            tempSchedule.makeRoutes()
            tempTrain = Train(tempSchedule, t["Line"], cls.nextID)
            cls.num_trains += 1
            cls.nextID += 1
            cls.Schedule[t["Line"]].addTrain(tempTrain)
        return True
    
    def addTrainSchedule(cls, TrainList: list):
        for t in TrainList:
            tempSchedule = TrainSchedule(t["Line"], t["Stations"])
            tempSchedule.makeRoutes()
            tempTrain = Train(tempSchedule, t["Line"], cls.nextID)
            cls.num_trains += 1
            cls.nextID += 1
            cls.Schedule[t["Line"]].addTrain(tempTrain)
        return True

    def breakTrack(cls, line: str, block_index : int = 0) -> bool:
        if(block_index == 0):
            #raise Exception("Cannot break the yard")
            return False
        elif(block_index >= len(cls.line[line].graph) or block_index < 0):
            #raise Exception(f'Block {block_index} does not exist')
            return False
        #Breaking a block
        #I know this looks ugly, i swear Graph will become iterable soon
        if(cls.line[line].graph[block_index].maintenance):
            return False
        else:
            cls.line[line].graph[block_index].maintenance = True
            return True
    
    def fixTrack(cls, line: str, block_index : int = 0) -> bool:
        if(block_index == 0):
            #raise Exception("Cannot break the yard")
            return False
        elif(block_index >= len(cls.line[line].graph) or block_index < 0):
            #raise Exception(f'Block {block_index} does not exist')
            return False
        #Breaking a block
        #I know this looks ugly, i swear Graph will become iterable soon
        if(cls.line[line].graph[block_index].maintenance):
            cls.line[line].graph[block_index].maintenance = False
            return True
        else:
            return False
        
    def addTrain(cls, line: str, stations: list = []) -> bool:
        if(stations == []):
            return False #Train isn't going anywhere
        #Add a schedule
        newTrainSchedule = TrainSchedule(cls.line[line], stations)
        newTrainSchedule.makeRoutes()
        #Make a train to wrap the schedule
        newTrain = Train(newTrainSchedule, line, cls.nextID)
        cls.num_trains += 1
        cls.nextID += 1
        #add the train to the total schedule
        cls.Schedule[line].addTrain(newTrain)
        return True

    def addStop(cls, trainID: int, stations: list = [])->bool:
        if stations == []:
            return False
        
        for s in cls.Schedule:
            for t in cls.Schedule[t].trains:
                if t.id == trainID:
                    for s in stations:
                        t.schedule.append(s)
                    t.makeRoutes()
                    return True
        return False
    
    def setSwitchState(cls, line: str, blockID: int):
        if 'switch' in cls.line[line].graph[blockID].infrastructure:
            return True
        
    def updateTrack(cls, line: str, states: list):
        #*Check to see if occupancies are trains or breakdowns
        for i, b in enumerate(states):
            #!i = block index, b block state
            if b:
                isBroken = True
                for t in cls.Schedule[line]:
                    if i in t.location.connections:
                        t.location = cls.line[line].graph[i]
                        isBroken = False
                if isBroken:
                    cls.line[line].closed = True


                                
        

    


        
    
