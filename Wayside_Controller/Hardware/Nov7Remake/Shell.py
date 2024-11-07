# receiver.py
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSlot , pyqtSignal
import copy
from GreenYardPLC import PLC

class WaysideWindow(QMainWindow):
    ws_tm_authority = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        uic.loadUi("app.ui", self)
        self.plc = PLC()
        self.occupancy = copy.deepcopy(self.plc.occupancy)
        self.authority = [False for i in range(28)]
        self.switch_58 = False
        self.switch_62 = False
        self.maintenance = [False for i in range(36)]
        self.signal_58 = False
        self.signal_62 = False
        self.exit = False
        self.switch_bool = True

        # Setup the periodic update
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)  # Function to update the UI
        self.timer.start(15)  # Updates every 1.5 seconds 
        
    def update_ui(self):
        for i in range(len(self.occupancy)):
            self.wayside_block_table.setItem(i,0, QTableWidgetItem(str(self.occupancy[i])))   

        for i in range(len(self.authority)):
            self.wayside_block_table.setItem(i,1, QTableWidgetItem(str(self.authority[i])))

    @pyqtSlot(list)
    def update_occupancy(self, new_occ):
        # Slot to update the label text
        self.occupancy = copy.deepcopy(new_occ)

        self.plc.update(self.occupancy, self.switch_bool, self.maintenance)
        self.authority = copy.deepcopy(self.plc.authority)
        self.ws_tm_authority.emit(self.plc.authority)

        