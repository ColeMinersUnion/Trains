from Node import Node    

class Graph:
    #I should make thie class iterable, but I don't know how and I'm behind schedule rn
    def __init__(self):
        self.graph = []

    def __str__(self):
        return f'{self.graph[1].line}'

    def addNode(self, n : Node)->None:
        self.graph.insert(n.index, n)

    def getNode(self, n : int)->Node:
        return self.graph[n]
            
    def getSection(self, section_label: str = "") -> list:
        section = []
        for block in self.graph:
            if(block.section == section_label):
                section.append(block)
        return section
    