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
            
    def getSection(self, section_label: str = "") -> list:
        section = []
        for block in self.graph:
            if(block.section == section_label):
                section.append(block)
        return section
    
    #! IMPORTANT 
    #* when dir = -1, the section is reversed
    #* when dir = 1, the section is forward
    #* when dir = 0, the section is bidirectional
    def setSectionDirection(self, section_label: str = "", dir: int = 0) -> bool:
        section = self.getSection(section_label)
        if len(section) == 0:
            return False
        
        if(dir == 1):
            for i in range(1, len(section) -1):
                block = self.graph[section[i].index - 1]
                if section_label == block.section:
                    block.pointsTo([i + 1])
                else:
                    continue
        elif(dir == -1):
            for j in range(1, len(section) -1):
                block = self.graph[section[j].index - 1]
                if section_label == block.section:
                    block.pointsTo([i - 1])
                else:
                    continue
        elif(dir == 0):
            for j in range(1, len(section) -1):
                block = self.graph[section[j].index - 1]
                if section_label == block.section:
                    block.pointsTo([i - 1, i + 1])
                else:
                    continue
        else:
            return False
            
        return True


