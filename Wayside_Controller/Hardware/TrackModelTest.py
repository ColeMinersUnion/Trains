# receiver.py
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QMainWindow
from PyQt6.QtCore import pyqtSlot , pyqtSignal, Qt
import copy


class TrackModelWindow(QMainWindow):
    tm_ws_occupancy = pyqtSignal(list)
    ctc_ws_suggested_switch = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        uic.loadUi("Wayside_Controller/Hardware/testbench.ui", self)
        self.occupancy = [False for i in range(151)]
        self.authority = [False for i in range(151)]

        for index in range(self.occ_list.count()):
            item = self.occ_list.item(index)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)


        self.occ_list.itemChanged.connect(self.occupancy_change)
        self.yard_switch.clicked.connect(self.toggle_yard_switch)
        self.loop_switch.clicked.connect(self.toggle_loop_switch)
        
    def toggle_yard_switch(self):
        self.ctc_ws_suggested_switch.emit(0)

    def toggle_loop_switch(self):
        self.ctc_ws_suggested_switch.emit(76)

    
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

        
        