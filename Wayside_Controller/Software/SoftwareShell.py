from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import * 
import importlib
import copy
import sys
from time import time
from GreenMainPLC import GreenPLC
#from TM_test import Track

class WaysideShell(object):
    ws_tm_authority = pyqtSignal(list)
    #ws_tm_dispatch = pyqtSignal(tuple)

    ws_tm_switch_13 = pyqtSignal(bool)
    ws_tm_switch_28 = pyqtSignal(bool)
    ws_tm_switch_77 = pyqtSignal(bool)
    ws_tm_switch_85 = pyqtSignal(bool)

    ws_tm_signal_13 = pyqtSignal(bool)
    ws_tm_signal_28 = pyqtSignal(bool)
    ws_tm_signal_77 = pyqtSignal(bool)
    ws_tm_signal_85 = pyqtSignal(bool) 

    ws_tm_crossing_19 = pyqtSignal(bool)
    ws_tm_crossing_108 = pyqtSignal(bool)

    def __init__(self,app):
        super().__init__()
        self.app = app
        self.ui = uic.loadUi('Wayside_Controller/Software/app.ui')

        #creating objects to connect signals to slots
        self.plc = GreenPLC()
        #self.tm = Track()

        self.occupancy = [False for i in range(1,151)]
        self.authority = [False for i in range(1,151)]

        self.switch_13 = True
        self.switch_28 = False
        self.switch_77 = False
        self.switch_85 = True
        #self.maintenance = [False for i in range(1,150)]   

        self.signal_13 = False
        self.signal_28 = False
        self.signal_77 = False
        self.signal_85 = False

        self.crossing_19 = False
        self.crossing_108 = False

        #lets user toggle buttons manually
        self.manual_inputs()

        #insert action to connect self.occupancy to incoming  occupancy signal from track model to update_occupancy func
        #self.tm.tm_ws_occupancy.connect(self.update_occupancy)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui) 
        self.timer.start(15) 

        #display UI
        self.ui.show()
        self.app.exec() 
        #self.run()

    ''' def run(self):
        
        self.app.exec()'''
    
    #slot to update occupancy which then updates the plc authority
    #then send out updated authority, switches, signals, crossings 
    @pyqtSlot(list)
    def update_occupancy(self, new_occupancy):
        
        #self.authority,self.switch_77,self.switch_85,self.switch_28,self.switch_13 = self.plc.update_values(new_occupancy) 
        self.authority,self.switch_77,self.switch_85,self.switch_28,self.switch_13,
        self.signal_77, self.signal_85, self.signal_28, self.signal_13, 
        self.crossing_19, self.crossing_108 = self.plc.update_values(new_occupancy)
        #emitting updated authority and switch, signal, crossing states:
        self.ws_tm_authority.emit(self.authority)

        self.ws_tm_switch_77.emit(self.switch_77)
        self.ws_tm_switch_85.emit(self.switch_85)
        self.ws_tm_switch_28.emit(self.switch_28)
        self.ws_tm_switch_13.emit(self.switch_13)

        self.ws_tm_signal_77.emit(self.signal_77)
        self.ws_tm_signal_85.emit(self.signal_85)
        self.ws_tm_signal_28.emit(self.signal_28)
        self.ws_tm_signal_13.emit(self.signal_13)

        self.ws_tm_crossing_19.emit(self.crossing_19)
        self.ws_tm_crossing_108.emit(self.crossing_108)
        return self.authority,self.switch_77,self.switch_85,self.switch_28,self.switch_13,self.signal_77,self.signal_85,self.signal_28,self.signal_13,self.crossing_19,self.crossing_108

    #slot to receive dispatch info from ctc
    '''@pyqtSlot(tuple)
    def send_dispatch(self, dispatch):
        #sending dispatch info signal (to track model):
        self.ws_tm_dispatch.emit(dispatch)'''

    def toggle_switch_13(self):
        self.switch_13 = not self.switch_13
    
    def toggle_switch_28(self):
        self.switch_28 = not self.switch_28

    def toggle_switch_77(self):
        self.switch_77 = not self.switch_77
    
    def toggle_switch_85(self):
        self.switch_85 = not self.switch_85

    def toggle_signal_13(self):
        self.signal_13 = not self.signal_13
    
    def toggle_signal_28(self):
        self.signal_28 = not self.signal_28
    
    def toggle_signal_77(self):
        self.signal_77 = not self.signal_77

    def toggle_signal_85(self):
        self.signal_85 = not self.signal_85
    
    def toggle_crossing_19(self):
        self.crossing_19 = not self.crossing_19
    
    def toggle_crossing_108(self):
        self.crossing_108 =  not self.crossing_108

    def manual_inputs(self):
        self.ui.manual_sw13_button.clicked.connect(self.toggle_switch_13)
        self.ui.manual_sw28_button.clicked.connect(self.toggle_switch_28)
        self.ui.manual_sw77_button.clicked.connect(self.toggle_switch_77)
        self.ui.manual_sw85_button.clicked.connect(self.toggle_switch_85)

        self.ui.manual_sig13_button.clicked.connect(self.toggle_signal_13)
        self.ui.manual_sig28_button.clicked.connect(self.toggle_signal_28)
        self.ui.manual_sig77_button.clicked.connect(self.toggle_signal_77)
        self.ui.manual_sig85_button.clicked.connect(self.toggle_signal_85)

        self.ui.manual_cr19_button.clicked.connect(self.toggle_crossing_19)
        self.ui.manual_cr108_button.clicked.connect(self.toggle_crossing_108)
    
    def update_ui(self):
        #update block table state and authority from Track Model
        for i in range(len(self.occupancy)):
            self.ui.wayside_block_table.setItem(i,0, QTableWidgetItem(str(self.occupancy[i])))

        for i in range(len(self.authority)):
            self.ui.wayside_block_table.setItem(i,1, QTableWidgetItem(str(self.authority[i])))
        
        #update switches 
        if(self.switch_13):
            self.ui.wayside_elements_table.setItem(0,0, QTableWidgetItem("True"))
        else:
            self.ui.wayside_elements_table.setItem(0,0, QTableWidgetItem("False"))
        if(self.switch_28):
            self.ui.wayside_elements_table.setItem(1,0, QTableWidgetItem("True"))
        else:
            self.ui.wayside_elements_table.setItem(1,0, QTableWidgetItem("False"))
        if(self.switch_77):
            self.ui.wayside_elements_table.setItem(2,0, QTableWidgetItem("True"))
        else:
            self.ui.wayside_elements_table.setItem(2,0, QTableWidgetItem("False"))
        if(self.switch_85):
            self.ui.wayside_elements_table.setItem(3,0, QTableWidgetItem("True"))
        else:
            self.ui.wayside_elements_table.setItem(3,0, QTableWidgetItem("False"))
        #update signals
        if(self.signal_13):
            self.ui.wayside_elements_table.setItem(4,0, QTableWidgetItem("Green"))
        else:
            self.ui.wayside_elements_table.setItem(4,0, QTableWidgetItem("Red"))
        if(self.signal_28):
            self.ui.wayside_elements_table.setItem(5,0, QTableWidgetItem("Green"))
        else:
            self.ui.wayside_elements_table.setItem(5,0, QTableWidgetItem("Red"))
        if(self.signal_77):
            self.ui.wayside_elements_table.setItem(6,0, QTableWidgetItem("Green"))
        else:
            self.ui.wayside_elements_table.setItem(6,0, QTableWidgetItem("Red"))
        if(self.signal_85):
            self.ui.wayside_elements_table.setItem(7,0, QTableWidgetItem("Green"))
        else:
            self.ui.wayside_elements_table.setItem(7,0, QTableWidgetItem("Red"))
        #update crossings
        if(self.crossing_19):
            self.ui.wayside_elements_table.setItem(8,0, QTableWidgetItem("Green"))
        else:
            self.ui.wayside_elements_table.setItem(8,0, QTableWidgetItem("Red"))
        if(self.crossing_108):
            self.ui.wayside_elements_table.setItem(9,0, QTableWidgetItem("Green"))
        else:
            self.ui.wayside_elements_table.setItem(9,0, QTableWidgetItem("Red"))

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WaysideShell(app)
    