# receiver.py
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import*
from PyQt6.QtCore import pyqtSlot , pyqtSignal, Qt
import copy


class CTCWindow(QMainWindow):
    ctc_ws_sugg_switch = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        uic.loadUi("Wayside_Controller/Hardware/ctc_tb.ui", self)
        self.occupancy = [False for i in range(151)]
        self.authority = [False for i in range(151)]
        self.switch_58 = False
        self.switch_62 = False
        self.signal_58 = False
        self.signal_62 = False



        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)  # Function to update the UI
        self.timer.start(15)  # Updates every 1.5 seconds 

        self.yard_button.clicked.connect(self.toggle_yard)
        self.blk76_button.clicked.connect(self.toggle_blk76)

    def toggle_yard(self):
        self.ctc_ws_sugg_switch.emit(0)

    def toggle_blk76(self):
        self.ctc_ws_sugg_switch.emit(76)

        
    def update_ui(self):
        for i in range(41, 77):
            self.ctc_block_table.setItem(i-41, 0, QTableWidgetItem(str(self.occupancy[i])))   

        for i in range(41, 69):
            self.ctc_block_table.setItem(i-41,1, QTableWidgetItem(str(self.authority[i])))

        if(self.switch_58):
            self.ctc_elements_table.setItem(0,0, QTableWidgetItem("57 -> 58"))
        else:
            self.ctc_elements_table.setItem(0,0, QTableWidgetItem("57 -> Yard"))

        if(self.switch_62): 
            self.ctc_elements_table.setItem(1,0, QTableWidgetItem("62 -> 63"))
        else:
            self.ctc_elements_table.setItem(1,0, QTableWidgetItem("Yard -> 63"))

        if(self.signal_58):
            self.ctc_elements_table.setItem(2,0, QTableWidgetItem("Green"))
        else:
            self.ctc_elements_table.setItem(2,0, QTableWidgetItem("Red"))
        
        if(self.signal_62):
            self.ctc_elements_table.setItem(3,0, QTableWidgetItem("Green"))
        else:
            self.ctc_elements_table.setItem(3,0, QTableWidgetItem("Red"))     
    

    @pyqtSlot(dict)
    def update_track(self, data):
        result = data["result"]
        if result:
            print("Change successful")
        else:
            print("Change failed")
        self.switch_58 = data["switch_58"]
        self.switch_62 = data["switch_62"]
        self.signal_58 = data["signal_58"]
        self.signal_62 = data["signal_62"]
       


        
        