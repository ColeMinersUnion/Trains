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
        if(len(self.schedule.routes) == 0 ):
            print("No Routes")
            return False
        #if(self.location == self.schedule.routes[self.curr_route].end):
        #    if(self.curr_route + 1 <= len(self.schedule.routes)):
        #        self.curr_route += 1
        #        self.Next_Stop = self.schedule.stations[self.curr_route + 1]
        #    else:
        #        print("Train has made it back to the station")
        #        return False #!Poof train should disappear
        else:
            try:
            
                #print(self.schedule.routes[self.curr_route].paths[self.curr_route_index])
            #print("H")
                self.location = self.line.graph[self.schedule.routes[self.curr_route].paths[self.curr_route_index]]

                if(self.curr_route_index + 1 <= len(self.schedule.routes[self.curr_route].paths)):
                    self.curr_route_index += 1
            except:
            #    print("IDK")
                return False
            #!I really hope that works, I did not think this through enough
        return True

    def waitTime(self, speedUp: bool = False) -> float:
        #wait = self.location.block_length / self.location.speed_limit
        if(speedUp):
            return 0.36
        else:
            return 3.6
        
    def speedy(self):
        try:
            return self.location.speed_limit
        except:
            return 0
    
    def auth(self):
        try:
            self.authority = 0
            for i in self.schedule.routes[self.curr_route].paths[self.curr_route_index : ]:
                self.authority += self.line.graph[i].block_length
            return self.authority
        except:
            return 0
    
if(__name__ == '__main__'):
    #Making the route
    from GetGreen import Green
    green = Green()
    from Default import greenDefault
    Thomas = TrainSchedule(green)
    I, O = greenDefault()
    from Route import Route
    Incoming = Route(63, 2, green)
    Incoming.paths = I
    print(I)
    print(Incoming.paths[0])
    Outgoing = Route(1, 58, green)
    Outgoing.paths = O
    Thomas.routes = [Incoming, Outgoing]

    James = Train(line=green, schedule=Thomas, id=101, location=green.graph[0])
    print(James.schedule.routes[1].paths)
    
    while(James.move()):
        print(str(James.location))
        time.sleep(James.waitTime(True))
    

    print("Train has reached Pioneer Station")
    time.sleep(1)
    James.curr_route += 1
    James.curr_route_index = 0
    while(James.move()):
        print(str(James.location))
        time.sleep(James.waitTime(True))
    print("Train has reached the yard")