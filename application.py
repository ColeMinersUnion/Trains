from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import * 
import importlib
import copy

class WaysideShell:
    def __init__(self):
        self.plc = None
        self.ctc = CTC()
        self.tm = TrackModel()
        self.occupancy = [False for i in range(17)]
        self.next_authority = [False for i in range(17)]
        self.switch_5 = False
        self.crossing_3 = False
        self.signal_6 = False
        self.signal_12 = False

    def upload_plc(self, file_name):
        try:
            plc = importlib.import_module(file_name)

        except ImportError:
            print(f"Error: Module '{file_name}' not found.")
            return False

    
        blue_plc = getattr(plc, file_name)         
        self.plc = blue_plc()
        self.plc.say_hi()
        return True


    def dispatch(self, speed, authority, switch):
        self.tm.dispatch(speed, authority)
        self.plc.dispatch(switch)

        

    
    def get_blocks(self):
        return self.occupancy
    
    def set_occupancy(self, occupancy):
        self.occupancy = copy.deepcopy(occupancy)
        self.plc.update_track(self.occupancy)
        self.next_authority = copy.deepcopy(self.plc.next_authority)
        self.switch_5 = copy.deepcopy(self.plc.switch_5)
        self.crossing_3 = copy.deepcopy(self.plc.crossing_3)
        self.signal_6 = copy.deepcopy(self.plc.signal_6)
        self.signal_12 = copy.deepcopy(self.plc.signal_12)


        
    
    def maintenance_blocks(self, blocks):
        return self.plc.update_maintenance(blocks)
    

class TrackModel:
    def __init__ (self):
        self.occupancy = [False for i in range(17)]
        self.switch_5 = False
        self.signal_6 = False
        self.signal_12 = False
        self.crossing_3 = False
        self.shell = None
        self.trains = []

    def dispatch(self, Speed, Authority):
        self.trains.append(0)
        self.occupancy[0] = True
        print(Speed, Authority)
        self.shell.set_occupancy(self.occupancy)

    def move_trains(self):

        self.switch_5 = copy.deepcopy(self.shell.switch_5)
        self.signal_6 = copy.deepcopy(self.shell.signal_6)
        self.signal_12 = copy.deepcopy(self.shell.signal_12)
        self.crossing_3 = copy.deepcopy(self.shell.crossing_3)
        if len(self.trains) > 0:
            print(self.trains[0], self.switch_5)
        for i in range(len(self.trains)):
            if self.shell.next_authority[self.trains[i]] == True:
                if self.trains[i] == 5 and self.switch_5 == False:
                    print("Train at block", self.trains[i], " has moved to block ", 12)
                    self.trains[i] = 12
                    self.occupancy[5] = False
                    self.occupancy[12] = True
                else:
                    print("Train at block", self.trains[i], " has moved to block ", self.trains[i] + 1)
                    self.occupancy[self.trains[i]] = False
                    self.occupancy[self.trains[i] + 1] = True
                    self.trains[i] += 1
        self.shell.set_occupancy(self.occupancy)

class CTC:
    def __init__(self):
        self.occupancy = [False for i in range(17)]
        self.block_error = [False for i in range(17)]
        self.switch_5 = False
        self.signal_6 = False
        self.signal_12 = False
        self.crossing_3 = False
        self.shell = None

    def dispatch(self, Speed, Authority, Switch):
        if all(i == False for i in self.occupancy[0:6]):
            print("ctc dipatch successful")
            self.shell.dispatch(Speed, Authority, Switch)
            return True
        else:
            print("Cannot dispatch train")
            return False
        
    def maintenance(self, maint_blocks):
        pass

    def set_occupancy(self, occupancy):
        self.occupancy = occupancy

class Application(object):
    def __init__(self, app):
        self.app = app

        self.shell = WaysideShell()
        self.ctc = self.shell.ctc
        self.tm = self.shell.tm
        self.ctc.shell = self.shell
        self.tm.shell = self.shell

        self.ui = uic.loadUi('WaysideShell.ui')

        # Sets the maintenance states to unchecked, they need to start checked for the checkboxes to activate
        for index in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(index)
            item.setCheckState(QtCore.Qt.Unchecked)

        self.wayside_inputs()
        self.ctc_inputs()

        self.plc_uploaded = False
        # Setup the periodic update
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)  # Function to update the UI
        self.timer.start(1500)  # Updates every 1.5 seconds 

        self.ui.show()
        self.run()
    def run(self):
        self.app.exec_()


    ################Wayside Functions#########################
    def wayside_inputs(self):
        # Connects the buttons to their functions
        self.ui.plc_upload_button.clicked.connect(self.upload_plc)
        self.ui.manual_sw5_button.clicked.connect(self.manual_switch_5)
        self.ui.manual_x3_button.clicked.connect(self.manual_crossing_3)
        self.ui.manual_sig6_button.clicked.connect(self.manual_signal_6)
        self.ui.manual_sig12_button.clicked.connect(self.manual_signal_12)
    def upload_plc(self):
        file_name = self.ui.plc_file_input.text()
        self.plc_uploaded = self.shell.upload_plc(file_name)

    def manual_switch_5(self):
        if self.plc_uploaded == False:
            self.shell.switch_5 = not self.shell.switch_5
        else:
            print("In auto mode")
    
    def manual_crossing_3(self):
        if self.plc_uploaded == False:
            self.shell.crossing_3 = not self.shell.crossing_3
        else:
            print("In auto mode")
    
    def manual_signal_6(self):
        if self.plc_uploaded == False:
            self.shell.signal_6 = not self.shell.signal_6
        else:
            print("In auto mode")
    
    def manual_signal_12(self):
        if self.plc_uploaded == False:
            self.shell.signal_12 = not self.shell.signal_12
        else:
            print("In auto mode")
    
    def update_wayside_tables(self):
        for i in range(len(self.shell.occupancy)):
            self.ui.wayside_block_table.setItem(i,0, QTableWidgetItem(str(self.shell.occupancy[i])))
            self.ui.wayside_block_table.setItem(i,1, QTableWidgetItem(str(self.shell.next_authority[i])))
    
            self.ui.wayside_elements_table.setItem(0,0, QTableWidgetItem(str(self.shell.switch_5)))
            self.ui.wayside_elements_table.setItem(1,0, QTableWidgetItem(str(self.shell.crossing_3)))
            self.ui.wayside_elements_table.setItem(2,0, QTableWidgetItem(str(self.shell.signal_6)))
            self.ui.wayside_elements_table.setItem(3,0, QTableWidgetItem(str(self.shell.signal_12)))
            

    #################CTC Functions###########################
    def ctc_inputs(self):
        self.ui.dispatch_button.clicked.connect(self.dispatch_train)

    def dispatch_train(self):
        if self.plc_uploaded == False:
            print("cannot dispatch without plc")
        else:
            speed = int(self.ui.suggested_speed.text())
            authority = int(self.ui.suggested_auth.text())
            switch = eval(self.ui.suggested_switch.currentText())
            self.ctc.dispatch(speed, authority, switch)

    #################Track Model Functions####################



    def move_trains(self):
        self.tm.move_trains()

    

    #################Update UI################################
    
    def update_ui(self):
        self.update_wayside_tables()
        if self.plc_uploaded:
            self.move_trains()
        

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Application(app)
