#used to store all routes
from Train import Train

#Not Singleton
class Schedule:
    def __init__(self, line: str = ""):
        self.trains = []
        self.line = line

    def addTrain(self, train: Train = None) -> bool:
        if(train != None):
            self.trains.append(train)
            return True
        return False
    
    def addStop(self, trainID: int, stop: str) -> bool:
        for t in self.trains:
            if t.id == trainID:
                t.schedule.addStop(stop)
                t.makeRoutes()
                break
        return True

    
    


    
    
