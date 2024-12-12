import sys
import os
from PyQt6.QtWidgets import QApplication
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from CTC_Office.Frontend.app import CTCApplication

app = QApplication(sys.argv) #new application

ctc = CTCApplication() #makes CTC

def test_SetSwitch():
    switch = (13, 1, 12)
    blocks, switch_index = ctc.handleMaintenanceSwitch(switch)
    assert(switch_index == 13)
    expected_states = [False for _ in range(151)]
    expected_states[1] = True
    expected_states[12] = True
    expected_states[13] = True
    assert(blocks == expected_states)
    assert(ctc.ActiveMode == "Maintenance")

def test_RemoveMaintenance():    
    ctc.fixBlock.setText(str(1))
    ctc.onFix()
    ctc.fixBlock.setText(str(12))
    ctc.onFix()
    ctc.fixBlock.setText(str(13))
    assert(ctc.onFix() == [False for _ in range(151)])
    assert(ctc.ActiveMode == "Maintenance")

def test_MaintenanceBlock():
    block = 50
    print(block)
    ctc.breakBlok.setText(str(block))
    expected_states = [False for _ in range(151)]
    expected_states[block] = True
    blocks = ctc.onBreak()
    assert(blocks == expected_states)
    assert(ctc.ActiveMode == "Maintenance")

def test_RemoveMaintenanceBlock2():
    block = 50
    ctc.fixBlock.setText(str(block))
    assert(ctc.onFix() == [False for _ in range(151)])
    assert(ctc.ActiveMode == "Maintenance")

def test_DispatchTrain():
    trainDict = {4: [0, 3, 0]}
    auth = ctc.delayedTrainStart(trainDict)
    assert(auth == "5224.1;5124.1;5024.1;4824.1;4624.1;4524.1;4424.1;4324.1;4224.1;4124.1;4024.1;3924.1;3824.1;3724.1;3624.1;3324.1;3024.1;2724.1;2424.1;2124.1;1824.1;1524.1;1224.1;924.1;824.1;737.5;637.5;562.5;487.5;412.5;337.5;262.5;187.5;112.5;37.5;14626;14551;14476;14401;14326;14026;13726;13426;13126;12826;12526;12226;11926;11626;11591;11491;11391;11311;11211;11111;11021;10921;10821;10721;10621;10521;10421;10259;10159;10059;10009;9959;9909;9859;9809;9759;9709;9659;9609;9559;9509;9459;9409;9359;9309;9259;9209;9159;9109;9059;9009;8959;8909;8859;8809;8759;8709;8659;8609;8559;8509;8325;8285;8250;8200;8150;8050;7850;7550;7250;6950;6650;6500;6350;6200;6050;5900;5750;5600;5450;5350;5250;5150;5050;4950;4850;4750;4650;4550;4450;4350;4250;4100;3950;3800;3650;3500;3350;3200;3050;2750;2450;2150;1850;1650;1550;1500;1450;1400;1350;1300;1250;1200;1150;1100;1050;1000;950;900;850;800;750;700;650;600;550;500;450;400;350;300;250;200;150;100;50;0;0;")

def test_Schedule():
    tDict, auth = ctc.readFile("CTC_Office/Testing/TestingSchedule.csv")
    assert(tDict == {4: [0, 5, 0], 13: [0,8,0]})
    assert(auth == "5224.1;5124.1;5024.1;4824.1;4624.1;4524.1;4424.1;4324.1;4224.1;4124.1;4024.1;3924.1;3824.1;3724.1;3624.1;3324.1;3024.1;2724.1;2424.1;2124.1;1824.1;1524.1;1224.1;924.1;824.1;737.5;637.5;562.5;487.5;412.5;337.5;262.5;187.5;112.5;37.5;9626.0;9551.0;9476.0;9401.0;9326.0;9026.0;8726.0;8426.0;8126.0;7826.0;7526.0;7226.0;6926.0;6626.0;6591.0;6491.0;6391.0;6311.0;6211.0;6111.0;6021.0;5921.0;5821.0;5721.0;5621.0;5521.0;5421.0;5259.0;5159.0;5059.0;5009.0;4959.0;4909.0;4859.0;4809.0;4759.0;4709.0;4659.0;4609.0;4559.0;4509.0;4459.0;4409.0;4359.0;4309.0;4259.0;4209.0;4159.0;4109.0;4059.0;4009.0;3959.0;3909.0;3859.0;3809.0;3759.0;3709.0;3659.0;3609.0;3559.0;3509.0;3325.0;3285.0;3250.0;3200.0;3150.0;3050.0;2850.0;2550.0;2250.0;1950.0;1650.0;1500.0;1350.0;1200.0;1050.0;900.0;750.0;600.0;450.0;350.0;250.0;150.0;50.0;5050;4950;4850;4750;4650;4550;4450;4350;4250;4100;3950;3800;3650;3500;3350;3200;3050;2750;2450;2150;1850;1650;1550;1500;1450;1400;1350;1300;1250;1200;1150;1100;1050;1000;950;900;850;800;750;700;650;600;550;500;450;400;350;300;250;200;150;100;50;0;0;")
    assert(ctc.ActiveMode == "Automatic")

def test_Metrics():
    ctc.readFile("CTC_Office/Testing/TestingSchedule.csv") #adding a train
    trainDict = {7: [0, 5, 0]}
    ctc.delayedTrainStart(trainDict)
    ctc.breakBlok.setText(str(51))    
    ctc.onBreak()
    nTrains, nStations, maintenance, closed = ctc.throughputMetrics()
    assert(nTrains == 4) #The previous 2 trains from test_Schedule and test_DispatchTrain are still in the schedule
    assert(nStations == 10) #The yard is considered a station to be serviced. 
    assert(maintenance == 1)
    assert(closed == 0)



if __name__ == '__main__':
    pass



    

