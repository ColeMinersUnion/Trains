from Graph import Graph, Node
#I know it's long. I don't care. It was easier to hard code this than struggle with the excel file.
def Green() -> Graph:
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

    #?Section N
    Greenline.graph.append(Node(index=77, line="Green", section="N", block_length=300, block_grade=0, speed_limit=70, infrastructure="Switch, Station: Mt. Lebanon", elevation=0, cumulative_elevation=0.5, connections=[76, 78, 101]))
    Greenline.graph.append(Node(index=78, line="Green", section="N", block_length=300, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[77, 79]))
    Greenline.graph.append(Node(index=79, line="Green", section="N", block_length=300, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[78, 80]))
    Greenline.graph.append(Node(index=80, line="Green", section="N", block_length=300, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[79, 81]))
    Greenline.graph.append(Node(index=81, line="Green", section="N", block_length=300, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[80, 79]))
    Greenline.graph.append(Node(index=82, line="Green", section="N", block_length=300, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[81, 79]))
    Greenline.graph.append(Node(index=83, line="Green", section="N", block_length=300, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[82, 79]))
    Greenline.graph.append(Node(index=84, line="Green", section="N", block_length=300, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[83, 85]))
    Greenline.graph.append(Node(index=85, line="Green", section="N", block_length=300, block_grade=0, speed_limit=70, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[84, 86, 100]))

    #?Section O
    Greenline.graph.append(Node(index=86, line="Green", section="O", block_length=100, block_grade=0, speed_limit=25, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[87]))
    Greenline.graph.append(Node(index=87, line="Green", section="O", block_length=86.6, block_grade=0, speed_limit=25, infrastructure="", elevation=0, cumulative_elevation=0.5, connections=[88]))
    Greenline.graph.append(Node(index=88, line="Green", section="O", block_length=100, block_grade=0, speed_limit=25, infrastructure="Station: Poplar", elevation=0, cumulative_elevation=0.5, connections=[89]))

    #?Section P
    Greenline.graph.append(Node(index=89, line="Green", section="P", block_length=75, block_grade=-0.5, speed_limit=25, infrastructure="", elevation=-0.375, cumulative_elevation=0.125, connections=[90]))
    Greenline.graph.append(Node(index=90, line="Green", section="P", block_length=75, block_grade=-1, speed_limit=25, infrastructure="", elevation=-0.75, cumulative_elevation=-0.625, connections=[91]))
    Greenline.graph.append(Node(index=91, line="Green", section="P", block_length=75, block_grade=-2, speed_limit=25, infrastructure="", elevation=-1.5, cumulative_elevation=-2.125, connections=[92]))
    Greenline.graph.append(Node(index=92, line="Green", section="P", block_length=75, block_grade=0, speed_limit=25, infrastructure="", elevation=0, cumulative_elevation=-2.125, connections=[93]))
    Greenline.graph.append(Node(index=93, line="Green", section="P", block_length=75, block_grade=2, speed_limit=25, infrastructure="", elevation=1.5, cumulative_elevation=-0.625, connections=[94]))
    Greenline.graph.append(Node(index=94, line="Green", section="P", block_length=75, block_grade=1, speed_limit=25, infrastructure="", elevation=0.75, cumulative_elevation=0.125, connections=[95]))
    Greenline.graph.append(Node(index=95, line="Green", section="P", block_length=75, block_grade=0.5, speed_limit=25, infrastructure="", elevation=0.375, cumulative_elevation=0.5, connections=[96]))
    Greenline.graph.append(Node(index=96, line="Green", section="P", block_length=75, block_grade=0, speed_limit=25, infrastructure="Station: Castle Shannon", elevation=0, cumulative_elevation=0, connections=[97]))
    Greenline.graph.append(Node(index=97, line="Green", section="P", block_length=75, block_grade=0, speed_limit=25, infrastructure="", elevation=0, cumulative_elevation=0, connections=[98]))

    #?Seciton Q
    Greenline.graph.append(Node(index=98, line="Green", section="Q", block_length=75, block_grade=0, speed_limit=25, infrastructure="", elevation=0, cumulative_elevation=0, connections=[99]))
    Greenline.graph.append(Node(index=99, line="Green", section="Q", block_length=75, block_grade=0, speed_limit=25, infrastructure="", elevation=0, cumulative_elevation=0, connections=[100]))
    Greenline.graph.append(Node(index=100, line="Green", section="Q", block_length=75, block_grade=0, speed_limit=25, infrastructure="", elevation=0, cumulative_elevation=0, connections=[85]))

    #?Section R
    Greenline.graph.append(Node(index=101, line="Green", section="R", block_length=35, block_grade=0, speed_limit=26, infrastructure="", elevation=0, cumulative_elevation=0, connections=[102]))

    #?Section S
    Greenline.graph.append(Node(index=102, line="Green", section="S", block_length=100, block_grade=0, speed_limit=28, infrastructure="Switch", elevation=0, cumulative_elevation=0, connections=[103]))
    Greenline.graph.append(Node(index=103, line="Green", section="S", block_length=100, block_grade=0, speed_limit=28, infrastructure="", elevation=0, cumulative_elevation=0, connections=[104]))
    Greenline.graph.append(Node(index=104, line="Green", section="S", block_length=80, block_grade=0, speed_limit=28, infrastructure="", elevation=0, cumulative_elevation=0, connections=[105]))

    #?Section T
    Greenline.graph.append(Node(index=105, line="Green", section="T", block_length=100, block_grade=0, speed_limit=28, infrastructure="Station: Dormont", elevation=0, cumulative_elevation=0, connections=[106]))
    Greenline.graph.append(Node(index=106, line="Green", section="T", block_length=100, block_grade=0, speed_limit=28, infrastructure="", elevation=0, cumulative_elevation=0, connections=[107]))
    Greenline.graph.append(Node(index=107, line="Green", section="T", block_length=90, block_grade=0, speed_limit=28, infrastructure="", elevation=0, cumulative_elevation=0, connections=[108]))
    Greenline.graph.append(Node(index=108, line="Green", section="T", block_length=100, block_grade=0, speed_limit=28, infrastructure="Crossing", elevation=0, cumulative_elevation=0, connections=[109]))
    Greenline.graph.append(Node(index=109, line="Green", section="T", block_length=100, block_grade=0, speed_limit=28, infrastructure="", elevation=0, cumulative_elevation=0, connections=[110]))

    #?Section U
    Greenline.graph.append(Node(index=110, line="Green", section="U", block_length=100, block_grade=0, speed_limit=30, infrastructure="", elevation=0, cumulative_elevation=0, connections=[111]))
    Greenline.graph.append(Node(index=111, line="Green", section="U", block_length=100, block_grade=0, speed_limit=30, infrastructure="", elevation=0, cumulative_elevation=0, connections=[112]))
    Greenline.graph.append(Node(index=112, line="Green", section="U", block_length=100, block_grade=0, speed_limit=30, infrastructure="", elevation=0, cumulative_elevation=0, connections=[113]))
    Greenline.graph.append(Node(index=113, line="Green", section="U", block_length=100, block_grade=0, speed_limit=30, infrastructure="", elevation=0, cumulative_elevation=0, connections=[114]))
    Greenline.graph.append(Node(index=114, line="Green", section="U", block_length=162, block_grade=0, speed_limit=30, infrastructure="Station: Glenbury", elevation=0, cumulative_elevation=0, connections=[115]))
    Greenline.graph.append(Node(index=115, line="Green", section="U", block_length=100, block_grade=0, speed_limit=30, infrastructure="", elevation=0, cumulative_elevation=0, connections=[116]))
    Greenline.graph.append(Node(index=116, line="Green", section="U", block_length=100, block_grade=0, speed_limit=30, infrastructure="", elevation=0, cumulative_elevation=0, connections=[117]))

    #?Section V
    Greenline.graph.append(Node(index=117, line="Green", section="V", block_length=50, block_grade=0, speed_limit=15, infrastructure="", elevation=0, cumulative_elevation=0, connections=[118]))
    Greenline.graph.append(Node(index=118, line="Green", section="V", block_length=50, block_grade=0, speed_limit=15, infrastructure="", elevation=0, cumulative_elevation=0, connections=[119]))
    Greenline.graph.append(Node(index=119, line="Green", section="V", block_length=50, block_grade=0, speed_limit=15, infrastructure="", elevation=0, cumulative_elevation=0, connections=[120]))
    Greenline.graph.append(Node(index=120, line="Green", section="V", block_length=50, block_grade=0, speed_limit=15, infrastructure="", elevation=0, cumulative_elevation=0, connections=[121]))
    Greenline.graph.append(Node(index=121, line="Green", section="V", block_length=50, block_grade=0, speed_limit=15, infrastructure="", elevation=0, cumulative_elevation=0, connections=[122]))

    #?Section W (UNDERGROUND)
    Greenline.graph.append(Node(index=122, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[123]))
    Greenline.graph.append(Node(index=123, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground, Station: Overbrook", elevation=0, cumulative_elevation=0, connections=[124]))
    Greenline.graph.append(Node(index=124, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[125]))
    Greenline.graph.append(Node(index=125, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[126]))
    Greenline.graph.append(Node(index=126, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[127]))
    Greenline.graph.append(Node(index=127, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[128]))
    Greenline.graph.append(Node(index=128, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[129]))
    Greenline.graph.append(Node(index=129, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[130]))
    Greenline.graph.append(Node(index=130, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[131]))
    Greenline.graph.append(Node(index=131, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[132]))
    Greenline.graph.append(Node(index=132, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground, Station: Inglewood", elevation=0, cumulative_elevation=0, connections=[133]))
    Greenline.graph.append(Node(index=133, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[134]))
    Greenline.graph.append(Node(index=134, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[135]))
    Greenline.graph.append(Node(index=135, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[136]))
    Greenline.graph.append(Node(index=136, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[137]))
    Greenline.graph.append(Node(index=137, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[138]))
    Greenline.graph.append(Node(index=138, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[139]))
    Greenline.graph.append(Node(index=139, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[140]))
    Greenline.graph.append(Node(index=140, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[141]))
    Greenline.graph.append(Node(index=141, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground, Station: Central", elevation=0, cumulative_elevation=0, connections=[142]))
    Greenline.graph.append(Node(index=142, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[143]))
    Greenline.graph.append(Node(index=143, line="Green", section="W", block_length=50, block_grade=0, speed_limit=20, infrastructure="Underground", elevation=0, cumulative_elevation=0, connections=[144]))

    #?Section X
    Greenline.graph.append(Node(index=144, line="Green", section="X", block_length=50, block_grade=0, speed_limit=20, infrastructure="", elevation=0, cumulative_elevation=0, connections=[145]))
    Greenline.graph.append(Node(index=145, line="Green", section="X", block_length=50, block_grade=0, speed_limit=20, infrastructure="", elevation=0, cumulative_elevation=0, connections=[146]))
    Greenline.graph.append(Node(index=146, line="Green", section="X", block_length=50, block_grade=0, speed_limit=20, infrastructure="", elevation=0, cumulative_elevation=0, connections=[147]))

    #?Section Y
    Greenline.graph.append(Node(index=147, line="Green", section="Y", block_length=50, block_grade=0, speed_limit=20, infrastructure="", elevation=0, cumulative_elevation=0, connections=[148]))
    Greenline.graph.append(Node(index=148, line="Green", section="Y", block_length=184, block_grade=0, speed_limit=20, infrastructure="", elevation=0, cumulative_elevation=0, connections=[149]))
    Greenline.graph.append(Node(index=149, line="Green", section="Y", block_length=40, block_grade=0, speed_limit=20, infrastructure="", elevation=0, cumulative_elevation=0, connections=[150]))

    #?Section Z
    Greenline.graph.append(Node(index=150, line="Green", section="Z", block_length=35, block_grade=0, speed_limit=20, infrastructure="", elevation=0, cumulative_elevation=0, connections=[28]))


    return Greenline






