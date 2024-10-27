from Train import Train
from TrainSchedule import TrainSchedule
from Schedule import Schedule

#! Top level Backend object to be instantiated in the application. 
#? ALso should become a singleton when I learn how those work
class CTC_Office:
    _instance = None
    #Set switch manually in maintenance mode.
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CTC_Office, cls).__new__(cls)
            # Put any initialization here.
            cls.line = []              #Graph
            cls.Schedule = Schedule()  #Schedule
            cls.num_trains = 0         #int
            cls.nextID = 0
        return cls._instance
        
    def addBlueLine(cls):
        try:
            from GetBlue import Blue
            cls.line = Blue(broken=False)
            return True
        except:
            print("Blue Line Init Failed")
            return False
        
    def addGreenLine(cls):
        return True
    
    def addRedLine(cls):
        return True
    
    
    def breakTrack(cls, block_index : int = 0) -> bool:
        if(block_index == 0):
            #raise Exception("Cannot break the yard")
            return False
        elif(block_index >= len(cls.line.graph) or block_index < 0):
            #raise Exception(f'Block {block_index} does not exist')
            return False
        #Breaking a block
        #I know this looks ugly, i swear Graph will become iterable soon
        if(cls.line.graph[block_index].closed):
            return False
        else:
            cls.line.graph[block_index].closed = True
            return True
    
    def fixTrack(cls, block_index : int = 0) -> bool:
        if(block_index == 0):
            #raise Exception("Cannot break the yard")
            return False
        elif(block_index >= len(cls.line.graph) or block_index < 0):
            #raise Exception(f'Block {block_index} does not exist')
            return False
        #Breaking a block
        #I know this looks ugly, i swear Graph will become iterable soon
        if(cls.line.graph[block_index].closed):
            cls.line.graph[block_index].closed = False
            return True
        else:
            return False
        
    def addTrain(cls, stations: list = []) -> bool:
        if(stations == []):
            return False #Train isn't going anywhere
        #Add a schedule
        newTrainSchedule = TrainSchedule(cls.line, stations)
        newTrainSchedule.makeRoutes()
        #Make a train to wrap the schedule
        newTrain = Train(newTrainSchedule, cls.line, cls.nextID)
        cls.num_trains += 1
        cls.nextID += 1
        #add the train to the total schedule
        cls.Schedule.addTrain(newTrain)
        return True
    

        

        

    


        
    
