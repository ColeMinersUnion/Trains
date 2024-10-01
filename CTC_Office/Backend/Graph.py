import Node    

class Graph:
    def __init__(self):
        self.graph = []

    def addNode(self, n : Node):
        self.graph.insert(n.index - 1, n)

    
    def findPaths(self, starting: Node, ending: Node):
        #* Need to account for visited nodes between n1 and n2 so I don't loop myself
        paths = set()
        
        self.almostDFS(starting, ending, set(), paths)

        allPaths = list[paths]
        allPaths.sort(key=len)

        return allPaths
    
    def almostDFS(self, starting: Node, ending: Node, currentPath: set, allPaths: set):
        if(starting == ending):
            #? Did I reach my destination
            allPaths.add(currentPath) #* Add how I got to my destination to the set
            return True #* End this train (hehe) of thought
        for i in starting.connections: #! Going through each of the connections to the
            oldCurrentPath = currentPath
            currentPath.add(self.graph[i])
            if oldCurrentPath == currentPath:
                continue
            else:
                return self.almostDFS(self.graph[i], ending, currentPath, allPaths)