import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Backend')))

from GetGreen import Green
from Default import greenSkips
from Skiplist import Skiplist
from Train import Train
from TrainSchedule import TrainSchedule
from Route import Route

skips = greenSkips()
green = Green()

def Central():
    
    SL = Skiplist(green, skips)
    return SL.skipRoute(0, 10)

def CentralAuth():
    Thomas = TrainSchedule(green)
    skips = greenSkips()
    SL = Skiplist(green, skips)
    rt1 = SL.skipRoute(0, 18) #To Central but the far one
    #rt2 = SL.skipRoute(18, 20) #To the yard
    Incoming = Route(rt1[0], rt1[len(rt1)-1], green)
    Incoming.paths = rt1
    
    Thomas.routes = [Incoming]

    James = Train(line=green, schedule=Thomas, id=101, location=green.graph[0])
    #print(James.schedule.routes[1].paths)
    return James.stringAuth()

def test_central():
    assert(Central() == [63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 85, 84, 83, 82, 81, 80, 79, 78, 77, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])

def test_central_auth():
    assert(CentralAuth() == '18512.6;18412.6;18312.6;18112.6;17912.6;17812.6;17712.6;17612.6;17512.6;17412.6;17312.6;17212.6;17112.6;17012.6;16912.6;16612.6;16312.6;16012.6;15712.6;15412.6;15112.6;14812.6;14512.6;14212.6;14112.6;14026;13926;13851;13776;13701;13626;13551;13476;13401;13326;13251;13176;13101;13026;12726;12426;12126;11826;11526;11226;10926;10626;10326;10291;10191;10091;10011;9911;9811;9721;9621;9521;9421;9321;9221;9121;8959;8859;8759;8709;8659;8609;8559;8509;8459;8409;8359;8309;8259;8209;8159;8109;8059;8009;7959;7909;7859;7809;7759;7709;7659;7609;7559;7509;7459;7409;7359;7309;7259;7209;7025;6985;6950;6900;6850;6750;6550;6250;5950;5650;5350;5200;5050;4900;4750;4600;4450;4300;4150;4050;3950;3850;3750;3650;3550;3450;3350;3250;3150;3050;2950;2800;2650;2500;2350;2200;2050;1900;1750;1450;1150;850;550;350;250;200;150;100;50;0;')





