import importlib.util
import copy
import socket
import json
from PyQt6.QtCore import pyqtSignal, QObject
import sys
from time import time
from GreenYardPLC import PLC

class WaysideShell:
    tm_ws_occupancy = pyqtSignal(list)
    ws_tm_authority = pyqtSignal(list)
    ws_tm_switch_58 = pyqtSignal(bool)
    ws_tm_switch_62 = pyqtSignal(bool)
    ws_tm_signal_58 = pyqtSignal(bool)
    ws_tm_signal_62 = pyqtSignal(bool)
    ws_tm_dispatch = pyqtSignal(tuple)
    def __init__(self):
        self.plc = None
        self.region = {"Line": "Green", "Region": (41, 77)}
        self.occupancy = [False for i in range(36)]
        self.authority = [False for i in range(28)]
        self.switch_58 = False
        self.switch_62 = False
        self.maintenance = [False for i in range(36)]
        self.signal_58 = False
        self.signal_62 = False
        self.exit = False
        self.switch_bool = True


    def send(self):
        self.plc.update(self.occupancy, self.switch_bool, self.maintenance)
        self.ws_tm_authority.emit(self.plc.authority)
        self.ws_tm_switch_58.emit(self.plc.switch_57)
        self.ws_tm_switch_62.emit(self.plc.switch_63)
        self.ws_tm_signal_58.emit(self.plc.signal_57)
        self.ws_tm_signal_62.emit(self.plc.signal_63)

    def dispatch(self, spd, auth):
        self.ws_tm_dispatch.emit((spd, auth))





