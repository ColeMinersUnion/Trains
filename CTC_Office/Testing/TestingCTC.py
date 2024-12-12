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
    assert(makeRoute() == '18937.6;18837.6;18737.6;18537.6;18337.6;18237.6;18137.6;18037.6;17937.6;17837.6;17737.6;17637.6;17537.6;17437.6;17337.6;17037.6;16737.6;16437.6;16137.6;15837.6;15537.6;15237.6;14937.6;14637.6;14537.6;14451.0;14351.0;14276.0;14201.0;14126.0;14051.0;13976.0;13901.0;13826.0;13751.0;13676.0;13601.0;13526.0;13451.0;13151.0;12851.0;12551.0;12251.0;11951.0;11651.0;11351.0;11051.0;10751.0;10716.0;10616.0;10516.0;10436.0;10336.0;10236.0;10146.0;10046.0;9946.0;9846.0;9746.0;9646.0;9546.0;9384.0;9284.0;9184.0;9134.0;9084.0;9034.0;8984.0;8934.0;8884.0;8834.0;8784.0;8734.0;8684.0;8634.0;8584.0;8534.0;8484.0;8434.0;8384.0;8334.0;8284.0;8234.0;8184.0;8134.0;8084.0;8034.0;7984.0;7934.0;7884.0;7834.0;7784.0;7734.0;7684.0;7634.0;7450.0;7410.0;7375.0;7325.0;7275.0;7175.0;6975.0;6675.0;6375.0;6075.0;5775.0;5625.0;5475.0;5325.0;5175.0;5025.0;4875.0;4725.0;4575.0;4475.0;4375.0;4275.0;4175.0;4075.0;3975.0;3875.0;3775.0;3675.0;3575.0;3475.0;3375.0;3225.0;3075.0;2925.0;2775.0;2625.0;2475.0;2325.0;2175.0;1875.0;1575.0;1275.0;975.0;775.0;675.0;625.0;575.0;525.0;475.0;425.0;375.0;325.0;275.0;225.0;175.0;125.0;75.0;25.0;900;850;800;750;700;650;600;550;500;450;400;350;300;250;200;150;100;50;0;0;')

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
    return CTC.Schedule["Green"].trains[0].location.index

def test_movingTrain():
    assert(movingTrain() == 0) #Train should have returned to yard

    

if __name__ == "__main__":
    print("Running tests")
    print(makeRoute())
    #test_makeRoute()
    #print("Everything passed")
