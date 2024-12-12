from numpy import array
from PyQt6.QtWidgets import QMainWindow, QPushButton, QScrollArea, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel
from PyQt6.QtCore import pyqtSlot, pyqtSignal
import sys, os
try:
    from Components.SchedulePreviewer import SchedulePreviewer
    from Components.NewTrainWidget import NewTrainWidget
    from Components.OccupancyWidget import OccupancyWidget
    from Components.MaintenanceBlocks import MaintenanceWidget
    from Components.SwitchWidget import SwitchWidget
except:
    from CTC_Office.Frontend.Components.SchedulePreviewer import SchedulePreviewer
    from CTC_Office.Frontend.Components.OccupancyWidget import OccupancyWidget
    from CTC_Office.Frontend.Components.NewTrainWidget import NewTrainWidget
    from CTC_Office.Frontend.Components.MaintenanceBlocks import MaintenanceWidget
    from CTC_Office.Frontend.Components.SwitchWidget import SwitchWidget
    sys.path.insert(1, os.path.join(os.getcwd(), 'CTC_Office', 'Backend'))
    print(os.getcwd())
    from CTC import CTC_Office    
    #print(os.getcwd())
    

from datetime import datetime
import time

Green = ['Pioneer', 'Edgebrook', 'Station D', 
         'Whited', 'South Bank', 'Central',
         'Inglewood', 'Overbrook', 'Glenbury',
         'Dormont', 'MT Lebanon', 'Poplar',
         'Castle Shannon', 'Dormont', 'Glenbury',
         'Overbrook', 'Inglewood', 'Central']

Modes = ["Manual", "Automatic", "Maintenance"]

class CTCApplication(QMainWindow):
    emitTrain = pyqtSignal(list, str)
    emitSwitch = pyqtSignal(int)
    emitMaintenance = pyqtSignal(list)
    emitMaintenanceSwitch = pyqtSignal(int)
    def __init__(self, Office = CTC_Office()):
        super().__init__()
        self.Office = Office
        self.Office.addGreenLine()

        self.ActiveMode = Modes[0]

        #Manual widgets
        self.GreenOcc = OccupancyWidget()
        self.RedOcc = OccupancyWidget()
        self.newTrainWidget = NewTrainWidget(Green)
        self.hlayout = QHBoxLayout()
        self.Manual_layout = QVBoxLayout()
        self.TestBench_layout = QVBoxLayout()
        self.Auto_layout = QVBoxLayout()
        self.main = QWidget()
        self.breakBlok = QLineEdit(parent=self)
        self.submitBreak = QPushButton("Break Block")
        self.break_state = True
        self.fixBlock = QLineEdit(parent=self)
        self.submitFix =QPushButton("Fix Block")
        self.fix_state = True
        self.GreenBlocks = MaintenanceWidget()

        self.maintenance_layout = QVBoxLayout()

        self.GreenSwitchs = SwitchWidget()
        self.GreenSwitchs.emitSwitch.connect(self.handleMaintenanceSwitch)
        
        self.Title = QLabel()
        self.Title.setText(f"{self.ActiveMode} Mode")
        self.Title.styleSheet = "font-size: 60px; font-weight: bold;"
        self.Manual_layout.addWidget(self.Title)


        self.hlayout.addWidget(self.newTrainWidget)
        self.hlayout.addWidget(self.GreenOcc)
        self.Manual_layout.addLayout(self.hlayout)
        self.Manual_layout.setSpacing(10)
        #!TestBench Stuff
        self.switchState = QLabel()
        self.speed = QLabel()
        self.auth = QLabel()


        self.setWindowTitle("CTC Office")
        self.TestBench_layout.addWidget(QLabel("Test Bench"))

        self.submitBreak.setCheckable(True)
        self.submitBreak.released.connect(self.onBreak)
        self.submitBreak.setChecked(self.break_state)

        self.submitFix.setCheckable(True)
        self.submitFix.released.connect(self.onFix)
        self.submitFix.setChecked(self.fix_state)

        self.mostRecentBreak = 0
        self.mostRecentSwitch = ()

        lbl = QLabel()
        lbl.setText("Testbench Information")

        lbl1 = QLabel()
        lbl1.setText("Green Line Occupancy")
        self.Manual_layout.addWidget(lbl1)
        self.Manual_layout.addWidget(self.GreenOcc.widget)
        self.Manual_layout.addWidget(QLabel("Green Line Block Status"))
        self.Manual_layout.addWidget(self.GreenBlocks.widget)

        self.lbl10 = QLabel()
        self.lbl10.setWordWrap(True)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.lbl10)
        self.lbl10.setText("Outputted String for Train")
        self.maintenance_layout.addWidget(QLabel("Maintenance"))


        lbl4 = QLabel()
        lbl4.setText("Breaking the track")
        self.BreakTrack = QWidget()
        self.BreakLayout = QVBoxLayout()
        self.BreakLayout.addWidget(lbl4)
        self.BreakLayout.addWidget(self.breakBlok)
        self.BreakLayout.addWidget(self.submitBreak)
        self.BreakTrack.setLayout(self.BreakLayout)
        self.maintenance_layout.addWidget(self.BreakTrack)

        lbl5 = QLabel()
        lbl5.setText("Fixing the track")
        self.FixTrack = QWidget()
        self.FixLayout = QVBoxLayout()
        self.FixLayout.addWidget(lbl5)
        self.FixLayout.addWidget(self.fixBlock)
        self.FixLayout.addWidget(self.submitFix)
        self.FixTrack.setLayout(self.FixLayout)
        self.maintenance_layout.addWidget(self.FixTrack)
        
        self.switches = QWidget()
        self.switch_layout = QVBoxLayout()
        self.switch_layout.addWidget(QLabel("Switches"))
        self.switch_layout.addWidget(self.GreenSwitchs)
        self.switches.setLayout(self.switch_layout)
        self.maintenance_layout.addWidget(self.switches)
        #Test bench stuff
        self.TestBench_layout.addWidget(lbl)
        self.TestBench_layout.addWidget(self.speed)
        self.TestBench_layout.addWidget(self.auth)
        self.TestBench_layout.addWidget(self.switchState)
        self.TestBench_layout.addWidget(scroll_area)

        #setting signals
        self.newTrainWidget.emitTrain.connect(self.handleNewGreenTrain)

        self.wrapperLayout = QHBoxLayout()
        self.ManualColumn = QWidget()
        
        self.ManualColumn.setLayout(self.Manual_layout)
        self.wrapperLayout.addWidget(self.ManualColumn)

        self.MaintenaceColumn = QWidget()
        self.MaintenaceColumn.setLayout(self.maintenance_layout)
        self.wrapperLayout.addWidget(self.MaintenaceColumn)

        self.TestBenchColumn = QWidget()
        self.TestBenchColumn.setLayout(self.TestBench_layout)
        self.wrapperLayout.addWidget(self.TestBenchColumn)


        #self.AutoColumn = QWidget()
        #self.AutoColumn.setLayout(self.Auto_layout)
        
        self.main.setLayout(self.wrapperLayout)

        self.setCentralWidget(self.main)        

    def changeMode(self, mode: int):
        self.ActiveMode = Modes[mode]
        self.Title.setText(f"{self.ActiveMode} Mode")


    def onBreak(self):
        self.changeMode(2)
        txt = self.breakBlok.text()
        self.mostRecentBreak = int(txt)
        if(self.Office.breakTrack("Green", int(txt))):
            self.breakBlok.setText(f'Block {int(txt)} is now broken. ')
        else:
            self.breakBlok.setText("That block does not exist, try again.")
        blockState = [x.maintenance for x in self.Office.line["Green"].graph]
        print(array(blockState))
        self.emitMaintenance.emit(blockState)
    
    @pyqtSlot(bool)
    def MaintenanceResponse(self, success: bool):
        if(success):
            self.updateBlocks()
        else:
            self.breakBlok.setText("The Wayside Office deemed maintenance operation irresponsible.")
            self.Office.fixTrack("Green", self.mostRecentBreak)
            self.updateBlocks()
        
    @pyqtSlot(bool)
    def MaintenanceSwitchResponse(self, success: bool):
        if(success):
            self.updateBlocks()
        else:
            self.breakBlok.setText("The Wayside Office deemed maintenance operation irresponsible.")
            for block in self.mostRecentSwitch:
                self.Office.fixTrack("Green", block)
            self.updateBlocks()
    
    def onFix(self):
        self.changeMode(2)
        txt = self.fixBlock.text()
        if(self.Office.fixTrack("Green", int(txt))):
            self.fixBlock.setText(f'Block {int(txt)} is now fixed. ')
        else:
            self.fixBlock.setText("That block does not exist or was not broken, try again.")
        blockState = [x.maintenance for x in self.Office.line["Green"].graph]
        self.emitMaintenance.emit(blockState)
        
    def onAuto(self):
        self.changeMode(1)
        fn = self.Automatic.text()
        try:
            #print(os.getcwd())
            file = open(fn)
            txt = file.readline()
            self.Office.addTrain([txt])
            self.Automatic.setText(f'File {fn} has been read')
            self.autoMove()
            file.close()
        except:
            self.Automatic.setText(f'File {fn} could not be found')
        self.auto_state = self.Auto.isChecked()

    def autoMove(self):
        self.changeMode(1)
        id = self.Office.nextID - 1
        train = self.Office.Schedule.trains[id]

        while(train.move()):
            self.scheduleWidget.update(train.id, str(train.location), train.Next_Stop, datetime.now())

            self.speed.setText(f'Speed: {train.speedy()}')
            self.auth.setText(f'Authority {train.auth()}')
            if train.Next_Stop == 'Station B':
                self.switchState.setText("Up")
            else:
                self.switchState.setText("Down")

            time.sleep(train.waitTime(speedUp=True))

    @pyqtSlot(list)
    def updateOccupancy(self, occupancies: list):
        #print(array(occupancies))
        line = ""
        if(len(occupancies) == 151):
            line = "Green"
        else:
            line = "Red"
        self.Office.updateTrack(line, occupancies)
        self.updateBlocks()
        trains = [(x.id, str(x.location)) for x in self.Office.Schedule[line].trains]
        print(f'Trains: {trains}')
        if(line == "Green"):
            self.GreenOcc.update(trains)
            self.updateBlocks()
        else:
            self.RedOcc.update(trains)
        return True
        
    def updateBlocks(self):
        blockList = []
        for block in self.Office.line["Green"].graph:
            if block.maintenance:
                blockList.append((block.index, "Maintenance"))
            elif block.closed:
                blockList.append((block.index, "Closed"))
        self.GreenBlocks.update(blockList)
            


    #handles the emitted signals from the NewTrainWidget
    @pyqtSlot(dict)
    def handleNewGreenTrain(self, train: dict):
        self.changeMode(0)
        auth = self.Office.addTrain("Green", [i for i in train.keys()]) #making sure it's a list
        self.Office.Schedule["Green"].trains[-1].move()
        self.emitTrain.emit([(63, 100, 70), (64, 100, 70), (65, 200, 70), (66, 200, 70), (67, 100, 40), (68, 100, 40), (69, 100, 40), (70, 100, 40), (71, 100, 40), (72, 100, 40), (73, 100, 40), (74, 100, 40), (75, 100, 40), (76, 100, 40), (77, 300, 70), (78, 300, 70), (79, 300, 70), (80, 300, 70), (81, 300, 70), (82, 300, 70), (83, 300, 70), (84, 300, 70), (85, 300, 70), (86, 100, 25), (87, 86.6, 25), (88, 100, 25), (89, 75, 25), (90, 75, 25), (91, 75, 25), (92, 75, 25), (93, 75, 25), (94, 75, 25), (95, 75, 25), (96, 75, 25), (97, 75, 25), (98, 75, 25), (99, 75, 25), (100, 75, 25), (85, 300, 70), (84, 300, 70), (83, 300, 70), (82, 300, 70), (81, 300, 70), (80, 300, 70), (79, 300, 70), (78, 300, 70), (77, 300, 70), (101, 35, 26), (102, 100, 28), (103, 100, 28), (104, 80, 28), (105, 100, 28), (106, 100, 28), (107, 90, 28), (108, 100, 28), (109, 100, 28), (110, 100, 30), (111, 100, 30), (112, 100, 30), (113, 100, 30), (114, 162, 30), (115, 100, 30), (116, 100, 30), (117, 50, 15), (118, 50, 15), (119, 50, 15), (120, 50, 15), (121, 50, 15), (122, 50, 20), (123, 50, 20), (124, 50, 20), (125, 50, 20), (126, 50, 20), (127, 50, 20), (128, 50, 20), (129, 50, 20), (130, 50, 20), (131, 50, 20), (132, 50, 20), (133, 50, 20), (134, 50, 20), (135, 50, 20), (136, 50, 20), (137, 50, 20), (138, 50, 20), (139, 50, 20), (140, 50, 20), (141, 50, 20), (142, 50, 20), (143, 50, 20), (144, 50, 20), (145, 50, 20), (146, 50, 20), (147, 50, 20), (148, 184, 20), (149, 40, 20), (150, 35, 20), (28, 50, 30), (27, 50, 30), (26, 100, 70), (25, 200, 70), (24, 300, 70), (23, 300, 70), (22, 300, 70), (21, 300, 70), (20, 150, 60), (19, 150, 60), (18, 150, 60), (17, 150, 60), (16, 150, 70), (15, 150, 70), (14, 150, 70), (13, 150, 45), (12, 100, 45), (11, 100, 45), (10, 100, 45), (9, 100, 45), (8, 100, 45), (7, 100, 45), (6, 100, 45), (5, 100, 45), (4, 100, 45), (3, 100, 45), (2, 100, 45), (1, 100, 45), (13, 150, 45), (14, 150, 70), (15, 150, 70), (16, 150, 70), (17, 150, 60), (18, 150, 60), (19, 150, 60), (20, 150, 60), (21, 300, 70), (22, 300, 70), (23, 300, 70), (24, 300, 70), (25, 200, 70), (26, 100, 70), (27, 50, 30), (28, 50, 30), (29, 50, 30), (30, 50, 30), (31, 50, 30), (32, 50, 30), (33, 50, 30), (34, 50, 30), (35, 50, 30), (36, 50, 30), (37, 50, 30), (38, 50, 30), (39, 50, 30), (40, 50, 30), (41, 50, 30), (42, 50, 30), (43, 50, 30), (44, 50, 30), (45, 50, 30), (46, 50, 30), (47, 50, 30), (48, 50, 30), (49, 50, 30), (50, 50, 30), (51, 50, 30), (52, 50, 30), (53, 50, 30), (54, 50, 30), (55, 50, 30), (56, 50, 30), (57, 50, 30)]
                            ,auth)
        return True
    
    @pyqtSlot(int)
    def handleGreenOutputSwitch(self, switch: int):
        self.emitSwitch.emit(switch)
        #print(f"Switching to {switch}")
        return True

    @pyqtSlot(tuple)
    def handleMaintenanceSwitch(self, switches: tuple):
        self.changeMode(2)
        self.mostRecentSwitch = switches
        for block in switches:
            if(self.Office.breakTrack("Green", block)):
                self.breakBlok.setText(f'Block {block} is now broken. ')
            else:
                self.breakBlok.setText("That block does not exist, try again.")
        blockState = [x.maintenance for x in self.Office.line["Green"].graph]
        self.emitMaintenance.emit(blockState)
        self.emitMaintenanceSwitch.emit(switches[0])
        




        
    
    

         



