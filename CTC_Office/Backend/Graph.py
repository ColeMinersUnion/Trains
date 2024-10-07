from Node import Node    

class Graph:
    #I should make thie class iterable, but I don't know how and I'm behind schedule rn
    def __init__(self):
        self.graph = []

    def __str__(self):
        return f'{self.graph[1].line}'

    def addNode(self, n : Node):
        self.graph.insert(n.index, n)

    def getNode(self, n : int):
        return self.graph[n]
            
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
            for i in range(0, len(section) -1):
                block = self.graph[section[i].index - 1]
                if section_label == block.section:
                    block.pointsTo([block.index + 1])
        elif(dir == -1):
            for j in range(len(section)):
                block = self.graph[section[j].index - 1]
                if section_label == block.section:
                    block.pointsTo([block.index - 1])
        elif(dir == 0):
            for k in range(1, len(section)
                           ):
                block = self.graph[section[k].index - 1]
                if section_label == block.section:
                    block.pointsTo([block.index - 1, block.index + 1])
        else:
            return False
        return True


