from Train import Train
from TrainSchedule import TrainSchedule
from Schedule import Schedule

#! Top level Backend object to be instantiated in the application. 
#? ALso should become a singleton when I learn how those work
class CTC_Office:
    def __init__(self):
        self.line = None            #Graph
        self.Schedule = Schedule()  #Schedule
        self.num_trains = 0         #int
        self.nextID = 0
        
    def addBlueLine(self):
        try:
            from GetBlue import Blue
            self.line = Blue(broken=False)
            return True
        except:
            print("Blue Line Init Failed")
            return False
    
    def breakTrack(self, block_index : int = 0) -> bool:
        if(block_index == 0):
            #raise Exception("Cannot break the yard")
            return False
        elif(block_index >= len(self.line.graph) or block_index < 0):
            #raise Exception(f'Block {block_index} does not exist')
            return False
        #Breaking a block
        #I know this looks ugly, i swear Graph will become iterable soon
        if(self.line.graph[block_index].closed):
            return False
        else:
            self.line.graph[block_index].closed = True
            return True
    
    def fixTrack(self, block_index : int = 0) -> bool:
        if(block_index == 0):
            #raise Exception("Cannot break the yard")
            return False
        elif(block_index >= len(self.line.graph) or block_index < 0):
            #raise Exception(f'Block {block_index} does not exist')
            return False
        #Breaking a block
        #I know this looks ugly, i swear Graph will become iterable soon
        if(self.line.graph[block_index].closed):
            self.line.graph[block_index].closed = False
            return True
        else:
            return False
        
    def addTrain(self, stations: list = []) -> bool:
        if(stations == []):
            return False #Train isn't going anywhere
        #Add a schedule
        newTrainSchedule = TrainSchedule(self.line, stations)
        newTrainSchedule.makeRoutes()
        #Make a train to wrap the schedule
        newTrain = Train(newTrainSchedule, self.line, self.nextID)
        self.num_trains += 1
        self.nextID += 1
        #add the train to the total schedule
        self.Schedule.addTrain(newTrain)
        return True
    

        

        

    


        
    
