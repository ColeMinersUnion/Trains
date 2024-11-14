#Used for storing route information
from Node import Node
from Graph import Graph
from datetime import datetime, timedelta

class Route:
    def __init__(self, start : int, end : int, line : Graph):
        self.start = start
        self.end = end
        self.paths = []
        self.line = line

    def findRoute(self) -> list:
        print(len(self.line.graph))
        self.findPaths(self.line.graph[self.start], self.line.graph[self.end])
        routes = list(self.paths)
        """
        for i, r in enumerate(routes):
            print(f'Route: {i}')
            for block in r:
                print(str(block))
            print('---\n\n')
        """
        
        if(len(routes) == 0):
            raise Exception("Unable to find route")
        elif(len(routes) == 1):
            self.paths = routes[0]
            return routes[0]
        else:
            #* find quickest route
            #* should be pre sorted
            print(len(self.paths))
            self.paths = routes[0]
            return routes
        
    def findPaths(self, starting: Node, ending: Node):
        #* Need to account for visited nodes between n1 and n2 so I don't loop myself
        routeList = []
        self.almostDFS(starting, ending, set(), routeList)
        routeList = []
        allPaths = list[self.paths]
        print(len(self.paths))
        #allPaths.sort(key=len)

        return allPaths
    


    def almostDFS(self, starting: Node, ending: Node, currentPath: set, routeList: list):
        if(starting == ending):
            #? Did I reach my destination
            self.paths.append(currentPath) #* Add how I got to my destination to the set
            print(routeList)
            return #* End this train (hehe) of thought
        oldCurrentPath = list(currentPath)
        for i in starting.connections: #! Going through each of the connections to the
            if(not self.line.graph[i].closed):
                currentPath.add(i) 
                
            else:
                continue #! That path is closed, unable to path over it.
            #print(f'{starting.connections}: {list(oldCurrentPath)}')
            if oldCurrentPath == list(currentPath):
                #print("oops")
                continue
            else:
                routeList.append(i)
                self.almostDFS(self.line.graph[i], ending, currentPath, routeList)
            currentPath = set(oldCurrentPath)
        return
        
    def __str__(self):
        myStr = 'Route:'
        for block in self.paths:
            myStr += f' {str(block)}, '
        myStr += '\n---\n'
        return myStr

    def suggestedSpeed(self, start : datetime, end: datetime, route_index : int) -> tuple:
        #! For a given route, find the speed for the train to go through across a given route
        rt = self.paths[route_index] 
        FastestTime = 0

        for block in rt:
            #* k = 3.6 for conversion sake
            b = self.line.graph[block]
            FastestTime += 3.6 * b.block_length / b.speed_limit
            #! Seconds = Meters / (Km/Hr)

        #Could also do this in hours and adjusting the thingy ma bob
        Fast = timedelta(seconds=FastestTime)
        delta = end - start
        if(Fast < delta):
            return False, 1 #! Is that timing possible?, Value to scale speed limits by. 
        else:
            return True, delta.total_seconds()/Fast.total_seconds()
 
    def authority(self, route_index: int) -> float:
        rt = self.paths[route_index] 
        distance = 0
        for block in rt:
            distance += self.line.graph[block].block_length
        return distance
        
    #TODO make a function that takes a speed% to find the time of arrival along a route
        
if(__name__ == '__main__'):
    from GetGreen import Green
    green = Green()
    print(len(green.graph))
    ToStationP = Route(0, 2, green)
    route = ToStationP.findPaths(green.graph[0], green.graph[2])

    BackToYard = Route(1, 58, green)
    rt = BackToYard.findPaths(green.graph[1], green.graph[58])

    try:
        for i, r in enumerate(route):
            print(f'Pioneer {i}: {r}')
        for i, r in enumerate(rt):
            print(f'Yard {i}: {r}')
    except:
        print("The route is unable to be completed")

