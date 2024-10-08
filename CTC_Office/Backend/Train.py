#Used as the iterator along a route
from TrainSchedule import TrainSchedule
from Node import Node
from Graph import Graph
import time # I think I need this for the delays going between blocks

class Train:

    def __init__(self, schedule: TrainSchedule, line: Graph = None, id: int = 0, location: Node = None) -> None:
        self.id = id #* ID#
        self.location = location #* Node
        self.line = line #* Graph
        self.speed = 0.0 
        self.authority = 0.0
        self.Next_Stop = schedule.stations[1]
        self.schedule = schedule
        self.curr_route = 0
        self.curr_route_index = 0
    
    def move(self) -> bool:
        #The notion is that I can do like a while(move())
        #Sort of thing and in the loop id:      time.sleep(block_length/speed)

        if(self.location == self.schedule.routes[self.curr_route].end):
            if(self.curr_route + 1 < len(self.schedule.routes)):
                self.curr_route += 1
            else:
                return False #!Poof train should disappear
        else:
            try:
                self.location = self.line.graph[list(self.schedule.routes[self.curr_route].paths)[self.curr_route_index]]

                if(self.curr_route_index + 1 <= len(self.schedule.routes[self.curr_route].paths)):
                    self.curr_route_index += 1
            except:
                return False
            #!I really hope that works, I did not think this through enough
        return True

    def waitTime(self, speedUp: bool = False) -> float:
        #wait = self.location.block_length / self.location.speed_limit
        if(speedUp):
            return 0.36
        else:
            return 3.6
    
if(__name__ == '__main__'):
    #Making the route
    from GetBlue import Blue
    blue = Blue(broken=False)
    Thomas = TrainSchedule(blue)
    Thomas.addStop("Station B")
    Thomas.makeRoutes()

    James = Train(line=blue, schedule=Thomas, id=101)
    while(James.move()):
        print(str(James.location))
        time.sleep(James.waitTime(True))
    print("Train has reached it's destination")