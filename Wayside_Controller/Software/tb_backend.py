from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import * 
import importlib
import copy
import sys
from time import time

from SoftwareShell import WaysideShell
from GreenMainPLC import GreenPLC

def main():
    #occ=[]
    occ=[False for i in range(151)]
    sw77=False
    sw85=False
    sw28=False
    sw13=False
    
    #ws=WaysideShell()
    plc=GreenPLC()
    auth=plc.update_authority(occ)
    for i in range(151):
        print(f"Green Line Authority Block {i}: {auth[i]} ")
    
    switch77,switch85,switch28,switch13=plc.update_switch(occ)
    print(f"Switches: {switch77}, {switch85}, {switch28}, {switch13}")

    signal77,signal85,signal28,signal13=plc.update_signal(switch77,switch85,switch28,switch13)
    print(f"Signals: {signal77}, {signal85}, {signal28}, {signal13}")

    crossing19,crossing108=plc.update_crossing(occ)
    print(f"Crossings: {crossing19}, {crossing108}")

if __name__== "__main__":
    main()