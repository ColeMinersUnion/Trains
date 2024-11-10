# receiver.py
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSlot , pyqtSignal
import copy
from GreenYardPLC import PLC

class WaysideWindow(QMainWindow):
    ws_tm_authority = pyqtSignal(list)
    ws_tm_dispatch = pyqtSignal(tuple)
    
    def __init__(self):
        super().__init__()
        uic.loadUi("app.ui", self)
        self.plc = PLC()
        self.occupancy = [False for i in range(151)]
        self.authority = [False for i in range(151)]
        self.switch_58 = False
        self.switch_62 = False
        self.maintenance = [False for i in range(151)]
        self.signal_58 = False
        self.signal_62 = False
        self.exit = False
        self.switch_bool = True

        #reads inputs from the user
        self.user_inputs()


        # Setup the periodic update
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)  # Function to update the UI
        self.timer.start(15)  # Updates every 1.5 seconds 
        

    def user_inputs(self):
        self.manual_sw58_button.clicked.connect(self.toggle_switch_58)
        self.manual_sw62_button.clicked.connect(self.toggle_switch_62)
        self.manual_sig58_button.clicked.connect(self.toggle_signal_58)
        self.manual_sig62_button.clicked.connect(self.toggle_signal_62)

    
    def toggle_switch_58(self):
        self.switch_58 = not self.switch_58
    
    def toggle_switch_62(self):
        self.switch_62 = not self.switch_62

    def toggle_signal_58(self):
        self.signal_58 = not self.signal_58
    
    def toggle_signal_62(self):
        self.signal_62 = not self.signal_62



    def update_ui(self):
        for i in range(41, 77):
            self.wayside_block_table.setItem(i-41, 0, QTableWidgetItem(str(self.occupancy[i])))   

        for i in range(41, 69):
            self.wayside_block_table.setItem(i-41,1, QTableWidgetItem(str(self.authority[i])))

        if(self.switch_58):
            self.wayside_elements_table.setItem(0,0, QTableWidgetItem("57 -> 58"))
        else:
            self.wayside_elements_table.setItem(0,0, QTableWidgetItem("57 -> Yard"))

        if(self.switch_62): 
            self.wayside_elements_table.setItem(1,0, QTableWidgetItem("62 -> 63"))
        else:
            self.wayside_elements_table.setItem(1,0, QTableWidgetItem("Yard -> 63"))

        if(self.signal_58):
            self.wayside_elements_table.setItem(2,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table.setItem(2,0, QTableWidgetItem("Red"))
        
        if(self.signal_62):
            self.wayside_elements_table.setItem(3,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table.setItem(3,0, QTableWidgetItem("Red"))


    @pyqtSlot(list)
    def update_occupancy(self, new_occ):
        # Slot to update the label text
        self.occupancy, self.authority, sw_success, self.switch_58, self.switch_62, self.maintenance = self.plc.update(new_occ, self.switch_bool, self.maintenance, self.maintenance)
        self.ws_tm_authority.emit(self.authority)

    @pyqtSlot(tuple)
    def send_dispatch(self, dispatch):
        self.ws_tm_dispatch.emit(dispatch)
        