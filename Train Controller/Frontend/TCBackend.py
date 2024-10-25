from PyQt5.QtCore import QObject
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QGridLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import pyqtSignal, Qt

class TCBackend(QObject):
    result_updated = pyqtSignal(dict)
    #values_updated = pyqtSignal(dict)
    #final_result_updated = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self._status = None  # Private attribute for status
        self._pwr = None   # Private attribute for power
        self._brake = None   # Private attribute for brake

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def pwr(self):
        return self._pwr

    @pwr.setter
    def pwr(self, value):
        self._pwr = value

    @property
    def brake(self):
        return self._brake

    @brake.setter
    def brake(self, value):
        self._brake = value

    def calculate_and_update(self, status, pwr, brake):
        # Update the values dictionary with the new value and interface name
        status = self.status
        pwr  = self.pwr
        brake = self.brake

        #put calculations here 

        print(f"Status: {self.status}")
        print(f"Power: {self.pwr}")
        print(f"Brake: {self.brake}")

        # Send the result back to the UI interfaces
        self.send_result_to_interfaces(self.status, self.pwr, self.brake)


    def power_calc(self, Kp, Ki):
        #put power calculations here 
        return self.Kp, self.Ki

    def send_result_to_interfaces(self, status, pwr, brake):
        # Emit a signal to update the UI interfaces with the result
        # (assuming you have a signal defined in the Backend class)
        self.result_updated.emit(self.status, self.pwr, self.brake)