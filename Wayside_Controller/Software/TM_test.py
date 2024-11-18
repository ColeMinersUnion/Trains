from PyQt6 import *
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import * 
import importlib
import copy
import sys


class Track(QObject):
    tm_ws_occupancy = pyqtSignal(list)
    def __init__(self):
        self.occupancy =[False for i in range(150)]

        self.send_occ()

    def send_occ(self):
        self.tm_ws_occupancy.emit(self.occupancy)
        print("Connection success!")
    
    