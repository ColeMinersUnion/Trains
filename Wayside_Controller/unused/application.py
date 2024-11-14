from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import * 
import importlib
import copy

class WaysideShell:
    def __init__(self):
        self.plc = None
        self.ctc = CTC()
        self.tm = TrackModel()
        self.occupancy = [False for i in range(17)]
        self.next_authority = [False for i in range(17)]
        self.maintenance_occupancy = [False for i in range(17)]
        self.block_error = [False for i in range(17)]
        self.switch_5 = False
        self.crossing_3 = False
        self.signal_6 = False
        self.signal_12 = False
    #uploads PLC code
    def upload_plc(self, file_name):
        try:
            plc = importlib.import_module(file_name)
        #throws an error message if the PLC code cannot be uploaded
        except ImportError:
            print(f"Error: Module '{file_name}' not found.")
            return False

    
        blue_plc = getattr(plc, file_name)         
        self.plc = blue_plc()
        self.plc.say_hi()
        return True

    #dispatches commanded speed, commanded authority to the track model and commanded switch change to the PLC based on suggested values from CTC
    def dispatch(self, speed, authority, switch):
        self.tm.dispatch(speed, authority)
        self.plc.dispatch(switch)

        

    #fetches current block occupancy
    def get_blocks(self):
        return self.occupancy
    #sets up copies of data to pass back to respective destinations
    def set_occupancy(self, occupancy):
        self.occupancy = copy.deepcopy(occupancy)
        self.plc.update_track(self.occupancy)
        self.next_authority = copy.deepcopy(self.plc.next_authority)
        self.switch_5 = copy.deepcopy(self.plc.switch_5)
        self.crossing_3 = copy.deepcopy(self.plc.crossing_3)
        self.signal_6 = copy.deepcopy(self.plc.signal_6)
        self.signal_12 = copy.deepcopy(self.plc.signal_12)
        self.block_error = copy.deepcopy(self.plc.block_error)


        
    
    def maintenance_blocks(self, blocks):
        self.plc.update_maint_occ(blocks)
        self.maintenance_occupancy = copy.deepcopy(self.plc.maint_occ)
        self.tm.set_maint_occ(self.maintenance_occupancy) 
    

class TrackModel:
    def __init__ (self):
        self.occupancy = [False for i in range(17)]
        self.switch_5 = False
        self.signal_6 = False
        self.signal_12 = False
        self.crossing_3 = False
        self.shell = None
        self.trains = []
        self.speed = 0
        self.authority = 0
        self.maint_occ = [False for i in range(17)]
    #takes in commanded speed, commanded authority from the shell
    def dispatch(self, Speed, Authority):
        self.trains.append(0)
        self.occupancy[0] = True
        self.speed = Speed
        self.authority = Authority
        self.shell.set_occupancy(self.occupancy)
    
    def update(self):
        self.switch_5 = copy.deepcopy(self.shell.switch_5)
        self.signal_6 = copy.deepcopy(self.shell.signal_6)  
        self.crossing_3 = copy.deepcopy(self.shell.crossing_3)
        self.signal_12 = copy.deepcopy(self.shell.signal_12)

    def move_trains(self):
        #moves the train forward in the case of no present switch or to a new super block of track depending upon where the train currently stands and the state of the switch on block 5
        self.switch_5 = copy.deepcopy(self.shell.switch_5)
        self.signal_6 = copy.deepcopy(self.shell.signal_6)
        self.signal_12 = copy.deepcopy(self.shell.signal_12)
        self.crossing_3 = copy.deepcopy(self.shell.crossing_3)

        for i in range(len(self.trains)):
            if self.shell.next_authority[self.trains[i]] == True:
                if self.trains[i] == 5 and self.switch_5 == False:
                    self.trains[i] = 12
                    self.occupancy[5] = False
                    self.occupancy[12] = True
                else:
                    self.occupancy[self.trains[i]] = False
                    self.occupancy[self.trains[i] + 1] = True
                    self.trains[i] += 1
        self.shell.set_occupancy(self.occupancy)
    
    def set_maint_occ(self, maint_blocks):
        for i in range(17):
            if maint_blocks[i] == True and self.maint_occ[i] == False:
                self.occupancy[i] = True
                self.maint_occ[i] = True
            if maint_blocks[i] == False and self.maint_occ[i] == True:
                self.occupancy[i] = False
                self.maint_occ[i] = False
        
        self.shell.set_occupancy(self.occupancy)

    def murphy_track(self, murphy_list):
        for i in range(17):
            if murphy_list[i] == True:
                self.occupancy[i] = True
            else:
                self.occupancy[i] = False


class CTC:
    def __init__(self):
        self.occupancy = [False for i in range(17)]
        self.block_error = [False for i in range(17)]
        self.switch_5 = False
        self.signal_6 = False
        self.signal_12 = False
        self.crossing_3 = False
        self.shell = None
        self.maint_proposed = [False for i in range(17)]
    #dispatches suggested values for speed, authority and switch change to the wayside shell
    def dispatch(self, Speed, Authority, Switch):
        if all(i == False for i in self.occupancy[0:6]):
            self.shell.dispatch(Speed, Authority, Switch)
            return True
        else:
            return False
        
    def maintenance(self, maint_blocks):
        self.shell.maintenance_blocks(maint_blocks)
    
    def update(self):
        self.switch_5 = copy.deepcopy(self.shell.switch_5)
        self.signal_6 = copy.deepcopy(self.shell.signal_6)
        self.crossing_3 = copy.deepcopy(self.shell.crossing_3)
        self.signal_12 = copy.deepcopy(self.shell.signal_12)
        self.block_error = copy.deepcopy(self.shell.block_error)

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

        self.ui = uic.loadUi('Wayside_Controller/WaysideShell.ui')

        # Sets the maintenance states to unchecked, they need to start checked for the checkboxes to activate
        for index in range(self.ui.maint_list.count()):
            item = self.ui.maint_list.item(index)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)

        for index in range(self.ui.murphy_list.count()):
            item = self.ui.murphy_list.item(index)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)

        self.wayside_inputs()
        self.ctc_inputs()
        self.track_model_inputs()

        self.plc_uploaded = False
        # Setup the periodic update
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)  # Function to update the UI
        self.timer.start(1500)  # Updates every 1.5 seconds 

        self.ui.show()
        self.run()
    def run(self):
        self.app.exec()


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
        self.ui.wayside_log.append(">>PLC uploaded")
    #manual mode functions:
    def manual_switch_5(self):
        if self.plc_uploaded == False:
            self.shell.switch_5 = not self.shell.switch_5
        else:
            self.ui.wayside_log.append(">>Cannot change switch once PLC is uploaded")
    
    def manual_crossing_3(self):
        if self.plc_uploaded == False:
            self.shell.crossing_3 = not self.shell.crossing_3
        else:
            self.ui.wayside_log.append(">>Cannot change switch once PLC is uploaded")
    
    def manual_signal_6(self):
        if self.plc_uploaded == False:
            self.shell.signal_6 = not self.shell.signal_6
        else:
            self.ui.wayside_log.append(">>Cannot change switch once PLC is uploaded")
    
    def manual_signal_12(self):
        if self.plc_uploaded == False:
            self.shell.signal_12 = not self.shell.signal_12
        else:
            self.ui.wayside_log.append(">>Cannot change switch once PLC is uploaded")
    #updates key inputs and outputs on the table in the wayside UI
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
        self.ui.maint_list.itemChanged.connect(self.maintenance_change)
    
    def update_ctc_tables(self):
        self.ui.ctc_elements_table.setItem(0,0, QTableWidgetItem(str(self.ctc.switch_5)))
        self.ui.ctc_elements_table.setItem(1,0, QTableWidgetItem(str(self.ctc.crossing_3)))
        self.ui.ctc_elements_table.setItem(2,0, QTableWidgetItem(str(self.ctc.signal_6)))
        self.ui.ctc_elements_table.setItem(3,0, QTableWidgetItem(str(self.ctc.signal_12)))

    def dispatch_train(self):
        if self.plc_uploaded == False:
            self.ui.ctc_log.append(">>cannot dispatch train without plc")
        else:
            speed = int(self.ui.suggested_speed.text())
            authority = int(self.ui.suggested_auth.text())
            switch = eval(self.ui.suggested_switch.currentText())
            self.ctc.dispatch(speed, authority, switch)
            self.ui.ctc_log.append(">>Dispatched train with speed: " + str(speed) + " and authority: " + str(authority))
            self.ui.tm_log.append(">>Dispatched train with speed: " + str(self.tm.speed) + " and authority: " + str(self.tm.authority))
    
    def maintenance_change(self):
        if self.plc_uploaded == False:
            self.ui.ctc_log.append(">>cannot use maintenance mode without plc")
        else:
            maint_blocks = []
            for i in range(self.ui.maint_list.count()):
                item = self.ui.maint_list.item(i)
                if item.checkState() == QtCore.Qt.Checked:
                    maint_blocks.append(True)
                else:
                    maint_blocks.append(False)
            maint_blocks.insert(0, False)  # Ensure index 0 is always False
            self.ctc.maintenance(maint_blocks)
            

    #################Track Model Functions####################


    def track_model_inputs(self):
        self.ui.murphy_list.itemChanged.connect(self.murphy_change)

    def move_trains(self):
        self.tm.move_trains()

    def murphy_change(self):
        murphy_list = []
        for i in range(self.ui.murphy_list.count()):
            item = self.ui.murphy_list.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                murphy_list.append(True)
            else:
                murphy_list.append(False)
        murphy_list.insert(0, False)
        self.tm.murphy_track(murphy_list)
        for i in range(len(self.ctc.block_error)):
            if self.ctc.block_error[i] == True:
                self.ui.ctc_log.append(">>Block " + str(i) + " has an error")

    def update_tm_tables(self):
        for i in range(len(self.tm.occupancy)):
            self.ui.tm_block_table.setItem(i,0, QTableWidgetItem(str(self.tm.occupancy[i])))
            self.ui.tm_block_table.setItem(i,1, QTableWidgetItem(str(self.shell.next_authority[i])))

        self.ui.tm_elements_table.setItem(0,0, QTableWidgetItem(str(self.tm.switch_5)))
        self.ui.tm_elements_table.setItem(1,0, QTableWidgetItem(str(self.tm.crossing_3)))
        self.ui.tm_elements_table.setItem(2,0, QTableWidgetItem(str(self.tm.signal_6)))
        self.ui.tm_elements_table.setItem(3,0, QTableWidgetItem(str(self.tm.signal_12)))

    #################Update UI################################
    
    def update_ui(self):
        self.update_wayside_tables()
        self.ctc.update()
        self.update_ctc_tables()
        self.tm.update()
        self.update_tm_tables()
        if self.plc_uploaded:
            self.move_trains()
        

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Application(app)
