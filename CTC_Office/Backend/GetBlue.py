from Node import Node
from Graph import Graph

def Blue(broken : bool = False):
    BlueLine = Graph()
    #*Section A
    BlueLine.graph.append(Node(index=0, line="Blue", section="A", block_length=0, block_grade=0, speed_limit=50, infrastructure="Yard", elevation=0, cumulative_elevation=0, connections=[1]))
    BlueLine.graph.append(Node(index=1, line="Blue", section="A", block_length=50, block_grade=0, speed_limit=50, infrastructure="", elevation=0, cumulative_elevation=0, connections=[2]))
    BlueLine.graph.append(Node(index=2, line="Blue", section="A", block_length=50, block_grade=0, speed_limit=50, infrastructure="", elevation=0, cumulative_elevation=0, connections=[3]))
    BlueLine.graph.append(Node(index=3, line="Blue", section="A", block_length=50, block_grade=0, speed_limit=50, infrastructure="Railway Crossing", elevation=0, cumulative_elevation=0, connections=[4]))
    BlueLine.graph.append(Node(index=4, line="Blue", section="A", block_length=50, block_grade=0, speed_limit=50, infrastructure="", elevation=0, cumulative_elevation=0, connections=[5]))
    BlueLine.graph.append(Node(index=5, line="Blue", section="A", block_length=50, block_grade=0, speed_limit=50, infrastructure="Switch", elevation=0, cumulative_elevation=0, connections=[6, 12]))
    
    #*Section B
    BlueLine.graph.append(Node(index=6, line="Blue", section="B", block_length=50, block_grade=0, speed_limit=50, infrastructure="Switch, Light", elevation=0, cumulative_elevation=0, connections=[7]))
    BlueLine.graph.append(Node(index=7, line="Blue", section="B", block_length=50, block_grade=0, speed_limit=50, infrastructure="", elevation=0, cumulative_elevation=0, connections=[8]))
    BlueLine.graph.append(Node(index=8, line="Blue", section="B", block_length=50, block_grade=0, speed_limit=50, infrastructure="", elevation=0, cumulative_elevation=0, connections=[9]))
    BlueLine.graph.append(Node(index=9, line="Blue", section="B", block_length=50, block_grade=0, speed_limit=50, infrastructure="", elevation=0, cumulative_elevation=0, connections=[10]))
    BlueLine.graph.append(Node(index=10, line="Blue", section="B", block_length=50, block_grade=0, speed_limit=50, infrastructure="Transponder", elevation=0, cumulative_elevation=0, connections=[11]))
    BlueLine.graph.append(Node(index=11, line="Blue", section="B", block_length=50, block_grade=0, speed_limit=50, infrastructure="Station B", elevation=0, cumulative_elevation=0, connections=[0]))

    #*Section C
    BlueLine.graph.append(Node(index=12, line="Blue", section="C", block_length=50, block_grade=0, speed_limit=50, infrastructure="Switch, Light", elevation=0, cumulative_elevation=0, connections=[13]))
    BlueLine.graph.append(Node(index=13, line="Blue", section="C", block_length=50, block_grade=0, speed_limit=50, infrastructure="", elevation=0, cumulative_elevation=0, connections=[14]))
    BlueLine.graph.append(Node(index=14, line="Blue", section="C", block_length=50, block_grade=0, speed_limit=50, infrastructure="", elevation=0, cumulative_elevation=0, connections=[15]))
    BlueLine.graph.append(Node(index=15, line="Blue", section="C", block_length=50, block_grade=0, speed_limit=50, infrastructure="Transponder", elevation=0, cumulative_elevation=0, connections=[16]))
    BlueLine.graph.append(Node(index=16, line="Blue", section="C", block_length=50, block_grade=0, speed_limit=50, infrastructure="Station C", elevation=0, cumulative_elevation=0, connections=[0]))

    if(broken):
        BlueLine.graph[13].closed = True
    #! All blocks made. 
    return BlueLine

if(__name__ == '__main__'):
    blue = Blue()
    for i in blue.graph:
        print(str(i)) 





