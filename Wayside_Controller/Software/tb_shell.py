from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import * 
import importlib
import copy
import sys
from time import time

from SoftwareShell2 import Wayside_Shell
from GreenMainPLC import GreenPLC

def main():
    occ=[False for i in range(151)]

    sh=Wayside_Shell()
    #sh=shell()
    auth,switch77,switch85,switch28,switch13,signal77,signal85,signal28,signal13,crossing19,crossing108=sh.update_occupancy(occ)

    for i in range(151):
        print(f"Green Line Authority Block {i}: {auth[i]} ")
    
    print(f"Switches: {switch77}, {switch85}, {switch28}, {switch13}")
    print(f"Signals: {signal77}, {signal85}, {signal28}, {signal13}")
    print(f"Crossings: {crossing19}, {crossing108}")

if __name__== "__main__":
    main()