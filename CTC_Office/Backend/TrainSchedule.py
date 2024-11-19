#from Node import Node
from Graph import Graph
from Route import Route
from Skiplist import Skiplist

class TrainSchedule:
    def __init__(self, line : Graph = None, stations : list = []) -> None:
        self.routes = []
        self.line = line
        self.stops = [] #! List of indices for making routes
        self.stations = ["Yard", "Pioneer"] #! List of stops in string formats
        if(stations != []):
            self.stations.extend(stations)
            self.findStops()

    #ALL STOPS
    def findStops(self) -> None:
        for s in self.stations:
            if(not self.findStop(s)): #!Runs the function and if it's false, throw and error
                raise Exception(f'{s} was not found in the {str(self.line)} line.')
        return
    
    #INDIVIDUAL STOP
    def findStop(self, stop: str) -> bool:
        for block in self.line.graph:
            if stop in block.infrastrucutre:
                
                self.stops.append(block.index)
                return True #* Stop was found
        return False #! stop was not found on the line

    
    def addStop(self, stop : str = "") -> bool:
        if(stop != ""):
            self.stations.append(stop) 
            self.findStops()
            return True
        else:
            return False



    def makeRoutes(self) -> None:
        #* Make pairs
        if(len(self.stops) < 2 and len(self.stations) < 1):
            raise Exception("Not enough info to make stops")
            return
        elif(len(self.stops) < 2):
            self.findStops()
            self.makeRoutes()
        else:
            oldStop = self.stops[0]
            for i in range(len(self.stops) - 1):
                nextStop = self.stops[i+1]
                newRoute = Route(oldStop, nextStop, self.line)
                try:
                    newRoute.findRoute()
                except:
                    print(f'Route {i} was unable to be made')
                    return
                self.routes.append(newRoute)
                oldStop = nextStop
            return
        
    def makeSkips(self) -> None:
        return #! This is a placeholder for now


if(__name__ == '__main__'):
    from GetGreen import Green
    green = Green()
    Thomas = TrainSchedule(green)
    Thomas.addStop("Station: Pioneer")
    Thomas.makeRoutes()
    for i, r in enumerate(Thomas.routes):
        print(f'Route {i}: {str(r)}')

            
