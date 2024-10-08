#used to store all routes
from Train import Train

#Singleton
class Schedule:
    def __init__(self):
        self.trains = []

    def addTrain(self, train: Train = None) -> bool:
        if(train != None):
            self.trains.append(train)
            return True
        return False
    
    


    
    
