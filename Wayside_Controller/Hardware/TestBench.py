from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import * 
import importlib
import copy
import sys

from Shell import WaysideShell


class TrackModel():
    tm_ws_occupancy = pyqtSignal(list)

    def __init__(self):

        self.occupancy = [False for i in range(36)]

    def send_occ(self):
        self.tm_ws_occupancy




class Application(object):
    def __init__(self, app):
        self.app = app
        self.shell = WaysideShell()
        self.tm = TrackModel()

        self.ui = uic.loadUi('Wayside_Controller/Hardware/app.ui')
        self.tbui = uic.loadUi('Wayside_Controller/Hardware/testbench.ui')
        for index in range(self.tbui.occ_list.count()):
            item = self.tbui.occ_list.item(index)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            

          
        self.tbui.occ_list.itemChanged.connect(self.update_tm)
        self.user_inputs()
        
        # Setup the periodic update
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)  # Function to update the UI
        self.timer.start(15)  # Updates every 1.5 seconds 

        self.ui.show()
        self.tbui.show()
        self.run()
        
    def update_tm(self):
        occ_list = []
        for i in range(self.tbui.occ_list.count()):
            item = self.tbui.occ_list.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                occ_list.append(True)
            else:
                occ_list.append(False)
                self.tm.occupancy = copy.deepcopy(occ_list)

    def run(self):
        self.app.exec()

    def user_inputs(self):
        if(any(self.shell.occupancy)):
            self.ui.manual_sw58_button.setEnabled(False)
            self.ui.manual_sw62_button.setEnabled(False)
            self.ui.manual_sig58_button.setEnabled(False)
            self.ui.manual_sig62_button.setEnabled(False)

        self.ui.manual_sw58_button.clicked.connect(self.shell.toggle_switch_58)
        self.ui.manual_sw62_button.clicked.connect(self.shell.toggle_switch_62)
        self.ui.manual_sig58_button.clicked.connect(self.shell.toggle_signal_58)
        self.ui.manual_sig62_button.clicked.connect(self.shell.toggle_signal_62)



    def update_ui(self):
        for i in range(len(self.shell.occupancy)):
            self.ui.wayside_block_table.setItem(i,0, QTableWidgetItem(str(self.shell.occupancy[i])))

        for i in range(len(self.shell.authority)):
            self.ui.wayside_block_table.setItem(i,1, QTableWidgetItem(str(self.shell.authority[i])))

        if(self.shell.switch_58):
            self.ui.wayside_elements_table.setItem(0,0, QTableWidgetItem("57 -> 58"))
        else:
            self.ui.wayside_elements_table.setItem(0,0, QTableWidgetItem("57 -> Yard"))

        if(self.shell.switch_62): 
            self.ui.wayside_elements_table.setItem(1,0, QTableWidgetItem("62 -> 63"))
        else:
            self.ui.wayside_elements_table.setItem(1,0, QTableWidgetItem("Yard -> 63"))

        if(self.shell.signal_58):
            self.ui.wayside_elements_table.setItem(2,0, QTableWidgetItem("Green"))
        else:
            self.ui.wayside_elements_table.setItem(2,0, QTableWidgetItem("Red"))
        
        if(self.shell.signal_62):
            self.ui.wayside_elements_table.setItem(3,0, QTableWidgetItem("Green"))
        else:
            self.ui.wayside_elements_table.setItem(3,0, QTableWidgetItem("Red"))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Application(app)