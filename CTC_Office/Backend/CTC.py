from Train import Train
from TrainSchedule import TrainSchedule
from Schedule import Schedule
from ScheduleParser import readSchedule
from Route import Route
from Skiplist import Skiplist
from Default import greenSkips

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
            cls.Schedule["Blue"] = Schedule("Blue")
            return True
        except:
            print("Blue Line Init Failed")
            return False
        
    def addGreenLine(cls):
        try:
            from GetGreen import Green
            cls.line["Green"] = Green()
            cls.Schedule["Green"] = Schedule("Green")
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
        
    def deprecatedAddTrain(cls, line: str, stations: list = []) -> bool:
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

    def addTrain(cls, line: str, stations: list = []) -> str:
        #list of indices
        
        if(stations == []):
            return False
        if(line == "Green"):
            cls.skips = Skiplist(cls.line["Green"], greenSkips())
        else:
            return False
        #Add a schedule
        temp = 0
        rtList = []
        for i, x in enumerate(stations):
            rt = cls.skips.skipRoute(temp, x)
            temp = x + 1
            rtList.append(Route(rt[0], rt[len(rt)-1], cls.line["Green"]))
            rtList[i].paths = rt
        returnRt = [*(cls.skips.skipRoute(temp, 20)), 0]
        print(returnRt)
        backHome = Route(returnRt[0], returnRt[len(returnRt)-1], cls.line["Green"])
        backHome.paths = returnRt
        rtList.append(backHome)

        Thomas = TrainSchedule(cls.line["Green"])
        Thomas.routes = rtList
        James = Train(line=cls.line["Green"], schedule=Thomas, id=cls.nextID, location=cls.line["Green"].graph[0])
        cls.num_trains += 1
        cls.nextID += 1
        cls.Schedule["Green"].addTrain(James)
        return James.stringAuth()

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
        #this is one off and idk from where it gets misaligned
        for i, b in enumerate(states):
            #!i = block index, b block state
            if b:
                isBroken = True
                for t in cls.Schedule[line].trains:
                    print(f"Train is at block: {i}")
                    print(f"Train Location: {t.location.connections}")
                    if i == t.location.index:
                        isBroken = False
                        continue
                    if i in t.location.connections:
                        t.location = cls.line[line].graph[i]
                        isBroken = False
                        #print("Train Moved!")
                if isBroken:
                    cls.line[line].closed = True
                    #raise Exception(f"Track {i} declared broken")
                    print(f"Track {i} declared broken")


                             
        

    


        
    
