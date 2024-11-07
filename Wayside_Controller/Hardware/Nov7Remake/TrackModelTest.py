# receiver.py
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QMainWindow
from PyQt6.QtCore import pyqtSlot , pyqtSignal, Qt
import copy


class TrackModelWindow(QMainWindow):
    tm_ws_occupancy = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        uic.loadUi("testbench.ui", self)
        self.occupancy = [False for i in range(36)]
        self.authority = [False for i in range(28)]

        for index in range(self.occ_list.count()):
            item = self.occ_list.item(index)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)

        self.occ_list.itemChanged.connect(self.occupancy_change)

        
       
    def occupancy_change(self):
        for i in range(self.occ_list.count()):
            item = self.occ_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                self.occupancy[i] = True
            else:
                self.occupancy[i] = False
        self.tm_ws_occupancy.emit(self.occupancy)

    @pyqtSlot(list)
    def update_authority(self, new_auth):
        # Slot to update the label text
        self.authority = copy.deepcopy(new_auth)

        
        