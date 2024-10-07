#Used for storing route information
from Node import Node
from Graph import Graph

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
        for i, r in enumerate(routes):
            print(f'Route: {i}')
            for block in r:
                print(str(block))
            print('---\n\n')
        

        
        if(len(routes) == 0):
            raise Exception("Error in track config. Non circular track.")
        elif(len(routes) == 1):
            self.paths = routes[0]
            return routes[0]
        else:
            #* find quickest route
            #* should be pre sorted
            print(len(self.paths))
            self.paths = routes[0]
            return routes[0]
        
    def findPaths(self, starting: Node, ending: Node):
        #* Need to account for visited nodes between n1 and n2 so I don't loop myself
        
        self.almostDFS(starting, ending, set())

        allPaths = list[self.paths]
        #allPaths.sort(key=len)

        return allPaths
    
    def almostDFS(self, starting: Node, ending: Node, currentPath: set):
        if(starting == ending):
            #? Did I reach my destination
            self.paths.append(currentPath) #* Add how I got to my destination to the set
            return #* End this train (hehe) of thought
        oldCurrentPath = sorted(list(currentPath))
        for i in starting.connections: #! Going through each of the connections to the
            currentPath.add(i)
            #print(f'{starting.connections}: {list(oldCurrentPath)}')
            if oldCurrentPath == sorted(list(currentPath)):
                #print("oops")
                continue
            else:
                self.almostDFS(self.line.graph[i], ending, currentPath)
            currentPath = set(oldCurrentPath)
        return
        
    def __str__(self):
        myStr = 'Route:'
        for block in self.paths:
            myStr += f' {str(block)}, '
        myStr += '\n---\n'
        return myStr

        
        
if(__name__ == '__main__'):
    from GetBlue import Blue
    blue = Blue()
    print(len(blue.graph))
    ToStationB = Route(0, 16, blue)
    route = ToStationB.findRoute()
    print(str(route))

