# receiver.py
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import*
from PyQt6.QtCore import pyqtSlot , pyqtSignal, Qt
import copy


class TrackModelWindow(QMainWindow):
    tm_ws_occupancy = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        uic.loadUi("Wayside_Controller/Hardware/tm_tb.ui", self)
        self.occupancy = [False for i in range(151)]
        self.authority = [False for i in range(151)]
        self.switch_58 = False
        self.switch_62 = False
        self.signal_58 = False
        self.signal_62 = False

        for index in range(self.occ_list.count()):
            item = self.occ_list.item(index)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)


        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)  # Function to update the UI
        self.timer.start(15)  # Updates every 1.5 seconds 

        self.occ_list.itemChanged.connect(self.occupancy_change)
        
    def update_ui(self):
        for i in range(41, 77):
            self.tm_block_table.setItem(i-41, 0, QTableWidgetItem(str(self.occupancy[i])))   

        for i in range(41, 69):
            self.tm_block_table.setItem(i-41,1, QTableWidgetItem(str(self.authority[i])))

        if(self.switch_58):
            self.tm_elements_table.setItem(0,0, QTableWidgetItem("57 -> 58"))
        else:
            self.tm_elements_table.setItem(0,0, QTableWidgetItem("57 -> Yard"))

        if(self.switch_62): 
            self.tm_elements_table.setItem(1,0, QTableWidgetItem("62 -> 63"))
        else:
            self.tm_elements_table.setItem(1,0, QTableWidgetItem("Yard -> 63"))

        if(self.signal_58):
            self.tm_elements_table.setItem(2,0, QTableWidgetItem("Green"))
        else:
            self.tm_elements_table.setItem(2,0, QTableWidgetItem("Red"))
        
        if(self.signal_62):
            self.tm_elements_table.setItem(3,0, QTableWidgetItem("Green"))
        else:
            self.tm_elements_table.setItem(3,0, QTableWidgetItem("Red"))     
    
    def occupancy_change(self):
        for i in range(self.occ_list.count()):
            item = self.occ_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                self.occupancy[i + 41] = True
            else:
                self.occupancy[i + 41] = False
        self.tm_ws_occupancy.emit(self.occupancy)
        

    @pyqtSlot(list)
    def update_authority(self, new_auth):
        # Slot to update the label text
        self.authority = copy.deepcopy(new_auth)

    @pyqtSlot(dict)
    def update_track(self, new_track):
        self.switch_58 = new_track["switch_58"]
        self.switch_62 = new_track["switch_62"]



        
        