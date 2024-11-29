from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import*
from PyQt6 import uic
import sys
from PyQt6.QtWidgets import QApplication



class WaysideHardwareView(QMainWindow):
# Signal to send data to Handler
    wsh_int_sw58 = pyqtSignal()
    wsh_int_sw62 = pyqtSignal()
    wsh_int_sig58 = pyqtSignal()
    wsh_int_sig62 = pyqtSignal()
    wsh_int_connect = pyqtSignal()
    def __init__(self):
        super().__init__()
        uic.loadUi("Wayside_Controller/Hardware/app.ui", self) # Load the UI file
    

    def user_inputs(self):
        self.manual_sw58_button.clicked.connect(self.toggle_sw58)
        self.manual_sw62_button.clicked.connect(self.toggle_sw62)
        self.manual_sig58_button.clicked.connect(self.toggle_sig58)
        self.manual_sig62_button.clicked.connect(self.toggle_sig62)
        self.connect_green.clicked.connect(self.connect)

    def toggle_sw58(self):
        self.wsh_int_sw58.emit()

    def toggle_sw62(self):
        self.wsh_int_sw58.emit()
    
    def toggle_sig58(self):
        self.wsh_int_sig58.emit()

    def toggle_sig62(self):
        self.wsh_int_sig62.emit()

    def connect(self):
        self.wsh_int_connect.emit()
    
    @pyqtSlot(list)
    def update_occupancy_table(self, occupancy):
        for i in range(41, 77):
            self.wayside_block_table.setItem(i-41, 0, QTableWidgetItem(str(occupancy[i]))) 

    @pyqtSlot(list)
    def update_authority_table(self, authority):
        for i in range(41, 69):
            self.wayside_block_table.setItem(i-41,1, QTableWidgetItem(str(authority[i])))


    @pyqtSlot(bool)
    def update_sw58(self, switch):
        if switch:
            self.wayside_elements_table.setItem(0,0, QTableWidgetItem("57 -> 58"))
        else:
            self.wayside_elements_table.setItem(0,0, QTableWidgetItem("57 -> Yard"))

    @pyqtSlot(bool)
    def update_sw62(self, switch):
        if switch:
            self.wayside_elements_table.setItem(1,0, QTableWidgetItem("62 -> 63"))
        else:
            self.wayside_elements_table.setItem(1,0, QTableWidgetItem("Yard -> 63"))

    @pyqtSlot(bool)
    def update_sig58(self, signal):
        if signal:
            self.wayside_elements_table.setItem(2,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table.setItem(2,0, QTableWidgetItem("Red"))

    @pyqtSlot(bool)
    def update_sig62(self, signal):
        if signal:
            self.wayside_elements_table.setItem(3,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table.setItem(3,0, QTableWidgetItem("Red"))



   


