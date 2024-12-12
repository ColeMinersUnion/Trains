import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Backend')))

from CTC import CTC_Office

def makeRoute():
    CTC = CTC_Office()
    CTC.addGreenLine()
    CTC.addTrain("Green", [18])
    return CTC.Schedule["Green"].trains[0].stringAuth()

def test_makeRoute():
    assert(makeRoute() == '18537.6;18437.6;18337.6;18137.6;17937.6;17837.6;17737.6;17637.6;17537.6;17437.6;17337.6;17237.6;17137.6;17037.6;16937.6;16637.6;16337.6;16037.6;15737.6;15437.6;15137.6;14837.6;14537.6;14237.6;14137.6;14051.0;13951.0;13876.0;13801.0;13726.0;13651.0;13576.0;13501.0;13426.0;13351.0;13276.0;13201.0;13126.0;13051.0;12751.0;12451.0;12151.0;11851.0;11551.0;11251.0;10951.0;10651.0;10351.0;10316.0;10216.0;10116.0;10036.0;9936.0;9836.0;9746.0;9646.0;9546.0;9446.0;9346.0;9246.0;9146.0;8984.0;8884.0;8784.0;8734.0;8684.0;8634.0;8584.0;8534.0;8484.0;8434.0;8384.0;8334.0;8284.0;8234.0;8184.0;8134.0;8084.0;8034.0;7984.0;7934.0;7884.0;7834.0;7784.0;7734.0;7684.0;7634.0;7584.0;7534.0;7484.0;7434.0;7384.0;7334.0;7284.0;7234.0;7050.0;7010.0;6975.0;6925.0;6875.0;6775.0;6575.0;6275.0;5975.0;5675.0;5375.0;5225.0;5075.0;4925.0;4775.0;4625.0;4475.0;4325.0;4175.0;4075.0;3975.0;3875.0;3775.0;3675.0;3575.0;3475.0;3375.0;3275.0;3175.0;3075.0;2975.0;2825.0;2675.0;2525.0;2375.0;2225.0;2075.0;1925.0;1775.0;1475.0;1175.0;875.0;575.0;375.0;275.0;225.0;175.0;125.0;75.0;25.0;850;800;750;700;650;600;550;500;450;400;350;300;250;200;150;100;50;0;0;')

def movingTrain():
    CTC = CTC_Office()
    CTC.addGreenLine()
    CTC.addTrain("Green", [2])
    while(CTC.Schedule["Green"].trains[0].move()):
        print(f'{str(CTC.Schedule["Green"].trains[0].location)}: {CTC.Schedule["Green"].trains[0].auth()}')
    CTC.Schedule["Green"].trains[0].curr_route += 1
    CTC.Schedule["Green"].trains[0].curr_route_index = 0
    while(CTC.Schedule["Green"].trains[0].move()):
        print(f'{str(CTC.Schedule["Green"].trains[0].location)}: {CTC.Schedule["Green"].trains[0].auth()}')

    

if __name__ == "__main__":
    print("Running tests")
    print(movingTrain())
    #test_makeRoute()
    #print("Everything passed")
