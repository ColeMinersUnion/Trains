#this file is to be used exclusively for testing UI functionality
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import * 
import importlib
import copy
import sys
from time import time

#from Wayside_Controller.Software.GreenMainPLC import GreenPLC
#uncomment this to test/run wayside software UI by itself:
from GreenMainPLC import GreenPLC

class WaysideShell(QMainWindow):
    wss_tm_authority = pyqtSignal(list)
    wss_ctc_occupancy = pyqtSignal(list)
    #ws_tm_dispatch = pyqtSignal(tuple)

    wss_tm_switch_13 = pyqtSignal(bool)
    wss_tm_switch_28 = pyqtSignal(bool)
    wss_tm_switch_77 = pyqtSignal(bool)
    wss_tm_switch_85 = pyqtSignal(bool)

    wss_tm_signal_13 = pyqtSignal(bool)
    wss_tm_signal_28 = pyqtSignal(bool)
    wss_tm_signal_77 = pyqtSignal(bool)
    wss_tm_signal_85 = pyqtSignal(bool) 

    wss_tm_crossing_19 = pyqtSignal(bool)
    wss_tm_crossing_108 = pyqtSignal(bool)

    def __init__(self, app):
        super().__init__()
        self.app = app
        uic.loadUi('Wayside_Controller/Software/app.ui', self)

        self.plc = GreenPLC()
        #occupancies and authority to fill green line
        #self.occupancy = [False for i in range(151)]
        self.occupancy = [False,False,True,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,True,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,False]
        self.authority = [True for i in range(151)]
        #occupancies and authority for red line
        self.occ_red = [False for i in range(77)]
        self.auth_red = [True for i in range(77)]
        '''self.occ_red = [False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,True,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,False,False]'''
       
        #switches
        self.switch_13 = True
        self.switch_28 = False
        self.switch_77 = False
        self.switch_85 = True
        #self.maintenance = [False for i in range(151)]   
        #signals
        self.signal_13 = True
        self.signal_28 = True
        self.signal_77 = True
        self.signal_85 = True
        #crossings
        self.crossing_19 = False
        self.crossing_108 = False

        #red line switches, signals and crossings
        self.switch_27=True
        self.switch_33=True
        self.switch_38=True
        self.switch_44=True

        self.signal_27=True
        self.signal_33=True
        self.signal_38=True
        self.signal_44=True

        self.switch_52=True
        self.signal_52=True
        self.crossing_47=False

        #lets user toggle buttons manually
        self.manual_inputs()

        self.update_occupancy(self.occupancy)
        
        #occupancy:
        for i in range(47):
            self.wayside_block_table.setItem(i-0, 0, QTableWidgetItem(""))   
        for i in range(69,151):
            self.wayside_block_table.setItem(i-0,0, QTableWidgetItem(""))
        #authority:
        for i in range(41):
            self.wayside_block_table.setItem(i-0,1, QTableWidgetItem(""))
        for i in range(69,151):
            self.wayside_block_table.setItem(i-0,1, QTableWidgetItem(""))

        #red line occupancy
        for i in range(21,45):
            self.wayside_block_table_2.setItem(i-0, 0, QTableWidgetItem(""))   
        for i in range(67,77):
            self.wayside_block_table_2.setItem(i-0,0, QTableWidgetItem(""))

        self.wayside_block_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.wayside_block_table_2.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

        self.update_ui()

        self.show()
        self.app.exec()

    
    #slot to receive updated occupancy from track model
    #which then updates the plc
    #then sends out updated authority, switches, signals, crossings 
    @pyqtSlot(list)
    def update_occupancy(self, new_occupancy):
        new_occupancy=new_occupancy
        #self.authority,self.switch_77,self.switch_85,self.switch_28,self.switch_13 = self.plc.update_values(new_occupancy) 
        self.authority,self.switch_77,self.switch_85,self.switch_28,self.switch_13,self.signal_77, self.signal_85, self.signal_28, self.signal_13, self.crossing_19, self.crossing_108 = self.plc.update_values(new_occupancy)
        #emitting updated authority and switch, signal, crossing states:
        self.wss_tm_authority.emit(self.authority) #sends updated authority to track model
        self.wss_ctc_occupancy.emit(self.occupancy) #sends track occ to ctc

        self.wss_tm_switch_77.emit(self.switch_77)
        self.wss_tm_switch_85.emit(self.switch_85)
        self.wss_tm_switch_28.emit(self.switch_28)
        self.wss_tm_switch_13.emit(self.switch_13)

        self.wss_tm_signal_77.emit(self.signal_77)
        self.wss_tm_signal_85.emit(self.signal_85)
        self.wss_tm_signal_28.emit(self.signal_28)
        self.wss_tm_signal_13.emit(self.signal_13)

        self.wss_tm_crossing_19.emit(self.crossing_19)
        self.wss_tm_crossing_108.emit(self.crossing_108)

        self.update_ui()
        #uncomment this when testing the shell:
        #return self.authority,self.switch_77,self.switch_85,self.switch_28,self.switch_13,self.signal_77,self.signal_85,self.signal_28,self.signal_13,self.crossing_19,self.crossing_108

    #slot to receive dispatch info from ctc
    '''@pyqtSlot(tuple)
    def send_dispatch(self, dispatch):
        #sending dispatch info signal (to track model):
        self.ws_tm_dispatch.emit(dispatch)'''

    def toggle_switch_13(self):
        self.switch_13 = not self.switch_13
        self.wss_tm_switch_13.emit(self.switch_13)
        self.update_ui()
    
    def toggle_switch_28(self):
        self.switch_28 = not self.switch_28
        self.wss_tm_switch_28.emit(self.switch_28)
        self.update_ui()

    def toggle_switch_77(self):
        self.switch_77 = not self.switch_77
        self.wss_tm_switch_77.emit(self.switch_77)
        self.update_ui()
    
    def toggle_switch_85(self):
        self.switch_85 = not self.switch_85
        self.wss_tm_switch_85.emit(self.switch_85)
        self.update_ui()

    def toggle_signal_13(self):
        self.signal_13 = not self.signal_13
        self.wss_tm_signal_13.emit(self.signal_13)
        self.update_ui()
    
    def toggle_signal_28(self):
        self.signal_28 = not self.signal_28
        self.wss_tm_signal_28.emit(self.signal_28)
        self.update_ui()
    
    def toggle_signal_77(self):
        self.signal_77 = not self.signal_77
        self.wss_tm_signal_77.emit(self.signal_77)
        self.update_ui()

    def toggle_signal_85(self):
        self.signal_85 = not self.signal_85
        self.wss_tm_signal_85.emit(self.signal_85)
        self.update_ui()
    
    def toggle_crossing_19(self):
        self.crossing_19 = not self.crossing_19
        self.wss_tm_crossing_19.emit(self.crossing_19)
        self.update_ui()
    
    def toggle_crossing_108(self):
        self.crossing_108 =  not self.crossing_108
        self.wss_tm_crossing_108.emit(self.crossing_108)
        self.update_ui()

    def toggle_switch_27(self):
        self.switch_27 = not self.switch_27
        self.update_ui()
    
    def toggle_switch_33(self):
        self.switch_33 = not self.switch_33
        self.update_ui()
    
    def toggle_switch_38(self):
        self.switch_38 = not self.switch_38
        self.update_ui()

    def toggle_switch_44(self):
        self.switch_44 = not self.switch_44
        self.update_ui()
    
    def toggle_switch_52(self):
        self.switch_52 = not self.switch_52
        self.update_ui()
    
    def toggle_signal_27(self):
        self.signal_27 = not self.signal_27
        self.update_ui()
    
    def toggle_signal_33(self):
        self.signal_33 = not self.signal_33
        self.update_ui()

    def toggle_signal_38(self):
        self.signal_38 = not self.signal_38
        self.update_ui()
    
    def toggle_signal_44(self):
        self.signal_44 = not self.signal_44
        self.update_ui()

    def toggle_signal_52(self):
        self.signal_52 = not self.signal_52
        self.update_ui()

    def toggle_crossing_47(self):
        self.crossing_47 =  not self.crossing_47
        self.update_ui()

    def manual_inputs(self):
        #green line switches
        self.manual_sw13_button.clicked.connect(self.toggle_switch_13)
        self.manual_sw28_button.clicked.connect(self.toggle_switch_28)
        self.manual_sw77_button.clicked.connect(self.toggle_switch_77)
        self.manual_sw85_button.clicked.connect(self.toggle_switch_85)
        #green line signals
        self.manual_sig13_button.clicked.connect(self.toggle_signal_13)
        self.manual_sig28_button.clicked.connect(self.toggle_signal_28)
        self.manual_sig77_button.clicked.connect(self.toggle_signal_77)
        self.manual_sig85_button.clicked.connect(self.toggle_signal_85)
        #green line crossings
        self.manual_cr19_button.clicked.connect(self.toggle_crossing_19)
        self.manual_cr108_button.clicked.connect(self.toggle_crossing_108)
        #red line switches
        self.manual_sw27_button.clicked.connect(self.toggle_switch_27)
        self.manual_sw33_button.clicked.connect(self.toggle_switch_33)
        self.manual_sw38_button.clicked.connect(self.toggle_switch_38)
        self.manual_sw44_button.clicked.connect(self.toggle_switch_44)

        self.manual_sw52_button.clicked.connect(self.toggle_switch_52)
        #red line signals
        self.manual_sig27_button.clicked.connect(self.toggle_signal_27)
        self.manual_sig33_button.clicked.connect(self.toggle_signal_33)
        self.manual_sig38_button.clicked.connect(self.toggle_signal_38)
        self.manual_sig44_button.clicked.connect(self.toggle_signal_44)

        self.manual_sig52_button.clicked.connect(self.toggle_signal_52)
        #red line crossings
        self.manual_cr47_button.clicked.connect(self.toggle_crossing_47)
    #confirm PLC is uploaded
    def say_hi(self):
        print("PLC Uploaded Successfully")

    def upload_plc(self):
        self.manual_plc_button.clicked.connect(self.say_hi)
    
    def update_ui(self):
        #update green line wayside block table state and authority from Track Model
        for i in range(47):
            self.wayside_block_table.setItem(i-0,0, QTableWidgetItem(str(self.occupancy[i])))

        for i in range(41):
            self.wayside_block_table.setItem(i-0,1, QTableWidgetItem(str(self.authority[i])))
        
        for i in range(68, 151):
            self.wayside_block_table.setItem(i-0,0, QTableWidgetItem(str(self.occupancy[i])))
        
        for i in range(68, 151):
            self.wayside_block_table.setItem(i-0,1, QTableWidgetItem(str(self.authority[i])))
        #update red line wayside 1 block table state and authority
        '''for i in range(21,46):
            self.wayside_block_table_2.setItem(i-21,0, QTableWidgetItem(str(self.occ_red[i])))
        for i in range(67,77):
            self.wayside_block_table_2.setItem(i-21,0, QTableWidgetItem(str(self.occ_red[i])))
        for i in range(21,46):
            self.wayside_block_table_2.setItem(i-21,1, QTableWidgetItem(str(self.auth_red[i])))
        for i in range(67,77):
            self.wayside_block_table_2.setItem(i-21,1, QTableWidgetItem(str(self.auth_red[i])))'''
        #update red line wayside 2 block table state and authority
        for i in range(46,67):
            self.wayside_block_table_3.setItem(i-46,0, QTableWidgetItem(str(self.occ_red[i])))
        for i in range(46,67):
            self.wayside_block_table_3.setItem(i-46,1, QTableWidgetItem(str(self.auth_red[i])))
        
        #update occupancy in table to have colors
        '''for i in range(47):
            block=self.wayside_block_table.item(i-0, 0)
            if self.occupancy[i]:
                block.setBackground(QtGui.QColor(0, 0, 255))
            else:
                block.setBackground(QtGui.QColor(16, 16, 16))
        for i in range(69,151):
            block = self.wayside_block_table.item(i-0, 0)
            if self.occupancy[i]:
                block.setBackground(QtGui.QColor(0, 0, 255))
            else:
                block.setBackground(QtGui.QColor(16, 16, 16))'''
        #block47=self.wayside_block_table.item(90,0)
        #block47.setBackground(QtGui.QColor(0, 255, 255))

        #update authority in table with colors
        '''for i in range(41):
            block = self.wayside_block_table.item(i-0, 1)
            if self.authority[i]:
                block.setBackground(QtGui.QColor(0, 255, 0))
            else:
                block.setBackground(QtGui.QColor(255, 0, 0))
        for i in range(69,151):
            block = self.wayside_block_table.item(i-0, 1)
            if self.authority[i]:
                block.setBackground(QtGui.QColor(0, 255, 0))
            else:
                block.setBackground(QtGui.QColor(255, 0, 0))'''

        '''for i in range(21,46):
            block=self.wayside_block_table_2.item(i-0, 0)
            if self.occ_red[i]:
                block.setBackground(QtGui.QColor(0, 0, 255))
            else:
                block.setBackground(QtGui.QColor(16, 16, 16))
        for i in range(67,77):
            block = self.wayside_block_table_2.item(i-0, 0)
            if self.occ_red[i]:
                block.setBackground(QtGui.QColor(0, 0, 255))
            else:
                block.setBackground(QtGui.QColor(16, 16, 16))'''
        #update green line switches 
        if(self.switch_13):
            self.wayside_elements_table.setItem(0,0, QTableWidgetItem("True"))
        else:
            self.wayside_elements_table.setItem(0,0, QTableWidgetItem("False"))
        if(self.switch_28):
            self.wayside_elements_table.setItem(1,0, QTableWidgetItem("True"))
        else:
            self.wayside_elements_table.setItem(1,0, QTableWidgetItem("False"))
        if(self.switch_77):
            self.wayside_elements_table.setItem(2,0, QTableWidgetItem("True"))
        else:
            self.wayside_elements_table.setItem(2,0, QTableWidgetItem("False"))
        if(self.switch_85):
            self.wayside_elements_table.setItem(3,0, QTableWidgetItem("True"))
        else:
            self.wayside_elements_table.setItem(3,0, QTableWidgetItem("False"))
        #update green line signals
        if(self.signal_13):
            self.wayside_elements_table.setItem(4,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table.setItem(4,0, QTableWidgetItem("Red"))
        if(self.signal_28):
            self.wayside_elements_table.setItem(5,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table.setItem(5,0, QTableWidgetItem("Red"))
        if(self.signal_77):
            self.wayside_elements_table.setItem(6,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table.setItem(6,0, QTableWidgetItem("Red"))
        if(self.signal_85):
            self.wayside_elements_table.setItem(7,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table.setItem(7,0, QTableWidgetItem("Red"))
        #update crossings
        if(self.crossing_19):
            self.wayside_elements_table.setItem(8,0, QTableWidgetItem("Down"))
        else:
            self.wayside_elements_table.setItem(8,0, QTableWidgetItem("Up"))
        if(self.crossing_108):
            self.wayside_elements_table.setItem(9,0, QTableWidgetItem("Down"))
        else:
            self.wayside_elements_table.setItem(9,0, QTableWidgetItem("Up"))
        #update red line switches
        if(self.switch_27):
            self.wayside_elements_table_2.setItem(0,0, QTableWidgetItem("True"))
        else:
            self.wayside_elements_table_2.setItem(0,0, QTableWidgetItem("False"))
        if(self.switch_33):
            self.wayside_elements_table_2.setItem(1,0, QTableWidgetItem("True"))
        else:
            self.wayside_elements_table_2.setItem(1,0, QTableWidgetItem("False"))
        if(self.switch_38):
            self.wayside_elements_table_2.setItem(2,0, QTableWidgetItem("True"))
        else:
            self.wayside_elements_table_2.setItem(2,0, QTableWidgetItem("False"))
        if(self.switch_44):
            self.wayside_elements_table_2.setItem(3,0, QTableWidgetItem("True"))
        else:
            self.wayside_elements_table_2.setItem(3,0, QTableWidgetItem("False"))

        if(self.switch_52):
            self.wayside_elements_table_3.setItem(0,0, QTableWidgetItem("True"))
        else:
            self.wayside_elements_table_3.setItem(0,0, QTableWidgetItem("False"))
        #update red line signals
        if(self.signal_27):
            self.wayside_elements_table_2.setItem(4,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table_2.setItem(4,0, QTableWidgetItem("Red"))
        if(self.signal_33):
            self.wayside_elements_table_2.setItem(5,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table_2.setItem(5,0, QTableWidgetItem("Red"))
        if(self.signal_38):
            self.wayside_elements_table_2.setItem(6,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table_2.setItem(6,0, QTableWidgetItem("Red"))
        if(self.signal_44):
            self.wayside_elements_table_2.setItem(7,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table_2.setItem(7,0, QTableWidgetItem("Red"))
        
        if(self.signal_52):
            self.wayside_elements_table_3.setItem(1,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table_3.setItem(1,0, QTableWidgetItem("Red"))
        #update red line crossings
        if(self.crossing_47):
            self.wayside_elements_table_3.setItem(2,0, QTableWidgetItem("Down"))
        else:
            self.wayside_elements_table_3.setItem(2,0, QTableWidgetItem("Up"))
        

        #Manual mode not permitted unless track is unoccuppied
        if(any(self.occupancy[1:41])==True or any(self.occupancy[69:151])==True):
            #disable green line switches, signals and crossings if track is occuppied
            self.manual_sw13_button.setEnabled(False)
            self.manual_sw28_button.setEnabled(False)
            self.manual_sw77_button.setEnabled(False)
            self.manual_sw85_button.setEnabled(False)

            self.manual_sig13_button.setEnabled(False)
            self.manual_sig28_button.setEnabled(False)
            self.manual_sig77_button.setEnabled(False)
            self.manual_sig85_button.setEnabled(False)

            self.manual_cr19_button.setEnabled(False)
            self.manual_cr108_button.setEnabled(False)

        else:
            self.manual_sw13_button.setEnabled(True)
            self.manual_sw28_button.setEnabled(True)
            self.manual_sw77_button.setEnabled(True)
            self.manual_sw85_button.setEnabled(True)

            self.manual_sig13_button.setEnabled(True)
            self.manual_sig28_button.setEnabled(True)
            self.manual_sig77_button.setEnabled(True)
            self.manual_sig85_button.setEnabled(True)

            self.manual_cr19_button.setEnabled(True)
            self.manual_cr108_button.setEnabled(True)

        #Manual Mode disabled for red line wayside 2
        if(any(self.occ_red[21:45])==True or any(self.occ_red[67:76])==True):
        #disable red line switches, signals and crossings if track is occuppied
            self.manual_sw27_button.setEnabled(False)
            self.manual_sw33_button.setEnabled(False)
            self.manual_sw38_button.setEnabled(False)
            self.manual_sw44_button.setEnabled(False)
            #self.manual_sw52_button.setEnabled(False)

            self.manual_sig27_button.setEnabled(False)
            self.manual_sig33_button.setEnabled(False)
            self.manual_sig38_button.setEnabled(False)
            self.manual_sig44_button.setEnabled(False)
            #self.manual_sig52_button.setEnabled(False)

            #self.manual_cr47_button.setEnabled(False)

        else:
            self.manual_sw27_button.setEnabled(True)
            self.manual_sw33_button.setEnabled(True)
            self.manual_sw38_button.setEnabled(True)
            self.manual_sw44_button.setEnabled(True)
            #self.manual_sw52_button.setEnabled(True)

            self.manual_sig27_button.setEnabled(True)
            self.manual_sig33_button.setEnabled(True)
            self.manual_sig38_button.setEnabled(True)
            self.manual_sig44_button.setEnabled(True)
            #self.manual_sig52_button.setEnabled(True)

            #self.manual_cr47_button.setEnabled(True)

        #Manual Mode disabled in red line wayside 3
        if(any(self.occ_red[45:66])==True):
            self.manual_sw52_button.setEnabled(False)
            self.manual_sig52_button.setEnabled(False)
            self.manual_cr47_button.setEnabled(False)
        else:
            self.manual_sw52_button.setEnabled(True)
            self.manual_sig52_button.setEnabled(True)
            self.manual_cr47_button.setEnabled(True)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WaysideShell(app)
    