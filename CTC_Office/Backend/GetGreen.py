from Graph import Graph, Node
#I know it's long. I don't care. It was easier to hard code this than struggle with the excel file.
def getGreen() -> Graph:
    Greenline = Graph()
    #?Section A
    Greenline.graph.append(Node(index=0, line="Green", section="A", block_length=0, block_grade=0, speed_limit=50, infrastructure="Yard", elevation=0, cumulative_elevation=0, connections=[63])) #!I may run into issues where I'm routing through the yard. 
    Greenline.graph.append(Node(index=1, line="Green", section="A", block_length=100, block_grade=0.5, speed_limit=45, infrastructure="Switch", elevation=0.5, cumulative_elevation=0.5, connections=[13]))
    Greenline.graph.append(Node(index=2, line="Green", section="A", block_length=100, block_grade=1, speed_limit=45, infrastructure="Station: Pioneer", elevation=1, cumulative_elevation=1.5, connections=[1]))
    Greenline.graph.append(Node(index=3, line="Green", section="A", block_length=100, block_grade=1.5, speed_limit=45, infrastructure="", elevation=1.5, cumulative_elevation=3, connections=[2]))
    
    #?Section B
    Greenline.graph.append(Node(index=4, line="Green", section="B", block_length=100, block_grade=2, speed_limit=45, infrastructure="", elevation=2, cumulative_elevation=5, connections=[3]))
    Greenline.graph.append(Node(index=5, line="Green", section="B", block_length=100, block_grade=3, speed_limit=45, infrastructure="", elevation=3, cumulative_elevation=8, connections=[4]))
    Greenline.graph.append(Node(index=6, line="Green", section="B", block_length=100, block_grade=4, speed_limit=45, infrastructure="", elevation=4, cumulative_elevation=12, connections=[5]))
    
    #?Section C
    Greenline.graph.append(Node(index=7, line="Green", section="C", block_length=100, block_grade=5, speed_limit=45, infrastructure="", elevation=5, cumulative_elevation=17, connections=[6]))
    Greenline.graph.append(Node(index=8, line="Green", section="C", block_length=100, block_grade=0, speed_limit=45, infrastructure="", elevation=0, cumulative_elevation=17, connections=[7]))
    Greenline.graph.append(Node(index=9, line="Green", section="C", block_length=100, block_grade=-5, speed_limit=45, infrastructure="Station: Edgebrook", elevation=-5, cumulative_elevation=12, connections=[8]))
    Greenline.graph.append(Node(index=10, line="Green", section="C", block_length=100, block_grade=-4.5, speed_limit=45, infrastructure="", elevation=-4.5, cumulative_elevation=7.5, connections=[9]))
    Greenline.graph.append(Node(index=11, line="Green", section="C", block_length=100, block_grade=-4, speed_limit=45, infrastructure="", elevation=-4, cumulative_elevation=3.5, connections=[10]))
    Greenline.graph.append(Node(index=12, line="Green", section="C", block_length=100, block_grade=-3, speed_limit=45, infrastructure="Switch", elevation=-3, cumulative_elevation=0.5, connections=[11]))
    
    #?Secion D
    #! Section D is bidirectional
    Greenline.graph.append(Node(index=13, line="Green", section="D", block_length=150, block_grade=0, speed_limit=45, infrastructure="Switch", elevation=0, cumulative_elevation=0.5, connections=[12, 1, 14]))
    Greenline.graph.append(Node(index=14, line="Green", section="D", block_length=150, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[13, 15]))
    Greenline.graph.append(Node(index=15, line="Green", section="D", block_length=150, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[14, 16]))
    Greenline.graph.append(Node(index=16, line="Green", section="D", block_length=150, block_grade=0, speed_limit=70, infrastructure="Station: D", elevation=0, cumulative_elevation=0.5, connections=[15, 17]))
    
    #?Section E
    #! Section E is also bidirectional
    Greenline.graph.append(Node(index=17, line="Green", section="E", block_length=150, block_grade=0, speed_limit=60, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[16, 18]))
    Greenline.graph.append(Node(index=18, line="Green", section="E", block_length=150, block_grade=0, speed_limit=60, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[17, 19]))
    Greenline.graph.append(Node(index=19, line="Green", section="E", block_length=150, block_grade=0, speed_limit=60, infrastructure="Railway Crossing", elevation=0, cumulative_elevation=0.5, connections=[18, 20]))
    Greenline.graph.append(Node(index=20, line="Green", section="E", block_length=150, block_grade=0, speed_limit=60, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[19, 21]))

    #?Section F
    #! Section F should be the last bidirectional track on this line
    Greenline.graph.append(Node(index=21, line="Green", section="F", block_length=300, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[20, 22]))
    Greenline.graph.append(Node(index=22, line="Green", section="F", block_length=300, block_grade=0, speed_limit=70, infrastructure="Station: Whited", elevation=0, cumulative_elevation=0.5, connections=[21, 23]))
    Greenline.graph.append(Node(index=23, line="Green", section="F", block_length=300, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[22, 24]))
    Greenline.graph.append(Node(index=24, line="Green", section="F", block_length=300, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[23, 25]))
    Greenline.graph.append(Node(index=25, line="Green", section="F", block_length=200, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[24, 26]))
    Greenline.graph.append(Node(index=26, line="Green", section="F", block_length=100, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[25, 27]))
    Greenline.graph.append(Node(index=27, line="Green", section="F", block_length=50, block_grade=0, speed_limit=30, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[26, 28]))
    Greenline.graph.append(Node(index=28, line="Green", section="F", block_length=50, block_grade=0, speed_limit=30, infrastructure="Switch", elevation=0, cumulative_elevation=0.5, connections=[27, 29])) #! You cannot go from 28 to 150, but you can go 150 to 28
    
    #?Section G
    Greenline.graph.append(Node(index=29, line="Green", section="G", block_length=50, block_grade=0, speed_limit=30, infrastructure="Switch", elevation=0, cumulative_elevation=0.5, connections=[30]))
    Greenline.graph.append(Node(index=30, line="Green", section="G", block_length=50, block_grade=0, speed_limit=30, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[31]))
    Greenline.graph.append(Node(index=31, line="Green", section="G", block_length=50, block_grade=0, speed_limit=30, infrastructure="Station: South Bank", elevation=0, cumulative_elevation=0.5, connections=[32]))
    Greenline.graph.append(Node(index=32, line="Green", section="G", block_length=50, block_grade=0, speed_limit=30, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[33]))

    #?Section H
    Greenline.graph.append(Node(index=33, line="Green", section="H", block_length=50, block_grade=0, speed_limit=30, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[34]))
    Greenline.graph.append(Node(index=34, line="Green", section="H", block_length=50, block_grade=0, speed_limit=30, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[35]))
    Greenline.graph.append(Node(index=35, line="Green", section="H", block_length=50, block_grade=0, speed_limit=30, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[36]))

    #?Section I
    #!Section I is entirely underground
    Greenline.graph.append(Node(index=36, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[37]))
    Greenline.graph.append(Node(index=37, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[38]))
    Greenline.graph.append(Node(index=38, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[39]))
    Greenline.graph.append(Node(index=39, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground, Station: Central", elevation=0, cumulative_elevation=0.5, connections=[40]))
    Greenline.graph.append(Node(index=40, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[41]))
    Greenline.graph.append(Node(index=41, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[42]))
    Greenline.graph.append(Node(index=42, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[43]))
    Greenline.graph.append(Node(index=43, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[44]))
    Greenline.graph.append(Node(index=44, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[45]))
    Greenline.graph.append(Node(index=45, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[46]))
    Greenline.graph.append(Node(index=46, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[47]))
    Greenline.graph.append(Node(index=47, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[48]))
    Greenline.graph.append(Node(index=48, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground, Station: Inglewood", elevation=0, cumulative_elevation=0.5, connections=[49]))
    Greenline.graph.append(Node(index=49, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[50]))
    Greenline.graph.append(Node(index=50, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[51]))
    Greenline.graph.append(Node(index=51, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[52]))
    Greenline.graph.append(Node(index=52, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[53]))
    Greenline.graph.append(Node(index=53, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[54]))
    Greenline.graph.append(Node(index=54, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[55]))
    Greenline.graph.append(Node(index=55, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[56]))
    Greenline.graph.append(Node(index=56, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground", elevation=0, cumulative_elevation=0.5, connections=[57]))
    Greenline.graph.append(Node(index=57, line="Green", section="I", block_length=50, block_grade=0, speed_limit=30, infrastructure="Underground, Station: Overbook", elevation=0, cumulative_elevation=0.5, connections=[58]))

    #?Section J
    #!How do I avoid routing the train through the yard as a shortcut?
    Greenline.graph.append(Node(index=58, line="Green", section="J", block_length=50, block_grade=0, speed_limit=30, infrastructure="Switch", elevation=0, cumulative_elevation=0.5, connections=[59, 0]))
    Greenline.graph.append(Node(index=59, line="Green", section="J", block_length=50, block_grade=0, speed_limit=30, infrastructure="Switch", elevation=0, cumulative_elevation=0.5, connections=[60]))
    Greenline.graph.append(Node(index=60, line="Green", section="J", block_length=50, block_grade=0, speed_limit=30, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[61]))
    Greenline.graph.append(Node(index=61, line="Green", section="J", block_length=50, block_grade=0, speed_limit=30, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[62]))
    Greenline.graph.append(Node(index=62, line="Green", section="J", block_length=50, block_grade=0, speed_limit=30, infrastructure="Switch", elevation=0, cumulative_elevation=0.5, connections=[63]))

    #?Section K
    Greenline.graph.append(Node(index=63, line="Green", section="K", block_length=100, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[64]))
    Greenline.graph.append(Node(index=64, line="Green", section="K", block_length=100, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[65]))
    Greenline.graph.append(Node(index=65, line="Green", section="K", block_length=200, block_grade=0, speed_limit=70, infrastructure="Station: Glenbury", elevation=0, cumulative_elevation=0.5, connections=[66]))
    Greenline.graph.append(Node(index=66, line="Green", section="K", block_length=200, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[67]))
    Greenline.graph.append(Node(index=67, line="Green", section="K", block_length=100, block_grade=0, speed_limit=40, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[68]))
    Greenline.graph.append(Node(index=68, line="Green", section="K", block_length=100, block_grade=0, speed_limit=40, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[69]))

    #?Section L
    Greenline.graph.append(Node(index=69, line="Green", section="L", block_length=100, block_grade=0, speed_limit=40, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[70]))
    Greenline.graph.append(Node(index=70, line="Green", section="L", block_length=100, block_grade=0, speed_limit=40, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[71]))
    Greenline.graph.append(Node(index=71, line="Green", section="L", block_length=100, block_grade=0, speed_limit=40, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[72]))
    Greenline.graph.append(Node(index=72, line="Green", section="L", block_length=100, block_grade=0, speed_limit=40, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[73]))
    Greenline.graph.append(Node(index=73, line="Green", section="L", block_length=100, block_grade=0, speed_limit=40, infrastructure="Station: Dormont", elevation=0, cumulative_elevation=0.5, connections=[74]))

    #?Section M
    Greenline.graph.append(Node(index=74, line="Green", section="M", block_length=100, block_grade=0, speed_limit=40, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[75]))
    Greenline.graph.append(Node(index=75, line="Green", section="M", block_length=100, block_grade=0, speed_limit=40, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[76]))
    Greenline.graph.append(Node(index=76, line="Green", section="M", block_length=100, block_grade=0, speed_limit=40, infrastructure="Switch", elevation=0, cumulative_elevation=0.5, connections=[77]))




    














    return Greenline






