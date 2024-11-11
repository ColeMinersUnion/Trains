# receiver.py
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSlot , pyqtSignal
import copy
import socket
import json
from time import time


class WaysideWindow(QMainWindow):
    ws_tm_authority = pyqtSignal(list)
    ws_tm_dispatch = pyqtSignal(tuple)
    
    def __init__(self):
        super().__init__()
        uic.loadUi("Wayside_Controller/Hardware/app.ui", self)

        self.occupancy = [False for i in range(151)]
        self.authority = [False for i in range(151)]
        self.switch_58 = False
        self.switch_62 = False
        self.maintenance = [False for i in range(151)]
        self.signal_58 = False
        self.signal_62 = False
        self.exit = False
        self.switch_bool = True

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = '192.168.137.222'
        self.server_port = 12345

        start = time()
        self.client_socket.connect((self.server_ip, self.server_port))
        end = time()    
        print(f"Connected to server {end - start} seconds") 


        #reads inputs from the user
        self.user_inputs()

        


        # Setup the periodic update
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)  # Function to update the UI
        self.timer.start(15)  # Updates every 1.5 seconds 
        
    def send(self, occupancy, switch_bool, maint_prop, maint_curr):
        data = {
        "occupancy": occupancy,
        "switch_bool": switch_bool,
        "proposed_maintenance": maint_prop,
        "current_maintenance": maint_curr,
        "exit": self.exit
        }
   

        self.client_socket.sendall(json.dumps(data).encode('utf-8'))

        response = self.client_socket.recv(8192)
        print("data received")
        received_data = json.loads(response.decode('utf-8'))
        self.occupancy = received_data["occupancy"]
        self.authority = received_data["authority"]
        self.switch_58 = received_data["switch_58"]
        self.switch_62 = received_data["switch_62"]
        self.maintenance = received_data["maintenance"]

    

    def user_inputs(self):
        self.manual_sw58_button.clicked.connect(self.toggle_switch_58)
        self.manual_sw62_button.clicked.connect(self.toggle_switch_62)
        self.manual_sig58_button.clicked.connect(self.toggle_signal_58)
        self.manual_sig62_button.clicked.connect(self.toggle_signal_62)

    
    def toggle_switch_58(self):
        self.switch_58 = not self.switch_58
    
    def toggle_switch_62(self):
        self.switch_62 = not self.switch_62

    def toggle_signal_58(self):
        self.signal_58 = not self.signal_58
    
    def toggle_signal_62(self):
        self.signal_62 = not self.signal_62



    def update_ui(self):
        for i in range(41, 77):
            self.wayside_block_table.setItem(i-41, 0, QTableWidgetItem(str(self.occupancy[i])))   

        for i in range(41, 69):
            self.wayside_block_table.setItem(i-41,1, QTableWidgetItem(str(self.authority[i])))

        if(self.switch_58):
            self.wayside_elements_table.setItem(0,0, QTableWidgetItem("57 -> 58"))
        else:
            self.wayside_elements_table.setItem(0,0, QTableWidgetItem("57 -> Yard"))

        if(self.switch_62): 
            self.wayside_elements_table.setItem(1,0, QTableWidgetItem("62 -> 63"))
        else:
            self.wayside_elements_table.setItem(1,0, QTableWidgetItem("Yard -> 63"))

        if(self.signal_58):
            self.wayside_elements_table.setItem(2,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table.setItem(2,0, QTableWidgetItem("Red"))
        
        if(self.signal_62):
            self.wayside_elements_table.setItem(3,0, QTableWidgetItem("Green"))
        else:
            self.wayside_elements_table.setItem(3,0, QTableWidgetItem("Red"))

        # Disables manual mode if the track is occupied
        if(any(self.occupancy[41:77])):
            self.manual_sw58_button.setEnabled(False)
            self.manual_sw62_button.setEnabled(False)
            self.manual_sig58_button.setEnabled(False)
            self.manual_sig62_button.setEnabled(False)
        else:
            self.manual_sw58_button.setEnabled(True)
            self.manual_sw62_button.setEnabled(True)
            self.manual_sig58_button.setEnabled(True)
            self.manual_sig62_button.setEnabled(True)

    @pyqtSlot(list)
    def update_occupancy(self, new_occ):
        # Slot to update the label text
        self.send(new_occ, self.switch_bool, self.maintenance, self.maintenance)
        self.ws_tm_authority.emit(self.authority)

    @pyqtSlot(tuple)
    def send_dispatch(self, dispatch):
        self.ws_tm_dispatch.emit(dispatch)
        

    @pyqtSlot(int)
    def update_switch(self, exit_block):
        if exit_block == 0:
            self.switch_bool = False
        else:
            self.switch_bool = True
        self.send(self.occupancy, self.switch_bool, self.maintenance, self.maintenance)
        self.ws_tm_authority.emit(self.authority)
        self.update_ui()


if __name__ == "__main__":
    ws = WaysideWindow()
    ws.client_socket.sendall("Hello, World!")