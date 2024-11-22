from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSlot , pyqtSignal
from time import time



# receiver.py
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import*
from PyQt6.QtCore import pyqtSlot , pyqtSignal, Qt
import copy


class TrackModelWindow():
    tk_ws_occupancy = pyqtSignal(list)
    tk_tm_next_block = pyqtSignal(int, float) # next block number and length?
    tk_tm_authority = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.occupancy = [False for i in range(151)]
        self.authority = [False for i in range(151)]
        self.maintenance = [False for i in range(151)]
        self.switch_58 = False
        self.switch_62 = False
        self.signal_58 = False
        self.signal_62 = False


        

        

    @pyqtSlot(list)
    def update_authority(self, new_auth):
        # Slot to update the label text
        self.authority = copy.deepcopy(new_auth)
        self.tk_tm_authority.emit(self.authority)


    @pyqtSlot(bool)
    def update_switch_58(self, new_switch):
        self.switch_58 = new_switch

    @pyqtSlot(bool)
    def update_switch_62(self, new_switch):
        self.switch_62 = new_switch

    @pyqtSlot(bool)
    def update_signal_58(self, new_signal):
        self.signal_58 = new_signal
    
    @pyqtSlot(bool)
    def update_signal_62(self, new_signal):
        self.signal_62 = new_signal

    
    @pyqtSlot(int)
    def occupancy_changed(self, block):
        self.occupancy[block] = False
        self.occupancy[block + 1] = True  #change this to the accurate next block 
        block_length = 0 #get the length of the next block
        self.tk_tm_next_block.emit(block + 1, block_length)
        self.tk_ws_occupancy.emit(self.occupancy)


    @pyqtSlot(list)
    def update_maintenance(self, new_maint):
        for i in range(41,77):
            if new_maint[i] == True and self.maintenance[i] == False:
                self.maintenance[i] = True
                self.occupancy[i] = True

            elif new_maint[i] == False and self.maintenance[i] == True:
                self.maintenance[i] = False
                self.occupancy[i] = False
        
        self.tk_ws_occupancy.emit(self.occupancy)
        
