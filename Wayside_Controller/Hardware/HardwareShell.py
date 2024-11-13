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
    ws_ctc_switch_result = pyqtSignal(dict)
    ws_tm_update_track = pyqtSignal(dict)
    ws_tm_maintenance = pyqtSignal(list)
    ws_ctc_occupancy = pyqtSignal(list)
    ws_ctc_maintenance = pyqtSignal(list)
    
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



        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = '192.168.137.222'
        self.server_port = 9000

        start = time()
        self.client_socket.connect((self.server_ip, self.server_port))
        end = time()    
        print(f"Connected to server {end - start} seconds") 
        data = {
            "input" : "say_hi"
        }
        self.send(data)
        decoded_json = self.receive()
        #reads inputs from the user
        #self.user_inputs()

        


        # Setup the periodic update
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)  # Function to update the UI
        self.timer.start(15)  # Updates every 1.5 seconds 


    def send(self, data):
        json_data = json.dumps(data)
        length_prefix = f"{len(json_data):<10}"  # Fixed 10-byte length prefix
        self.client_socket.sendall(length_prefix.encode('utf-8') + json_data.encode('utf-8'))


    def receive(self):
        length_prefix = self.client_socket.recv(10).decode('utf-8').strip()
        message_length = int(length_prefix)
        message_data = self.client_socket.recv(message_length).decode('utf-8')
        decoded_json = ""

        try:
            decoded_json = json.loads(message_data)
            return decoded_json

        except json.JSONDecodeError:
            print("failed to decode Json", message_data)
    


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
        self.send_occupancy(new_occ)
        self.ws_tm_authority.emit(self.authority)


    def send_occupancy(self, occupancy):
        self.occupancy = occupancy
        data = {
            "input" : "tm_occupancy",
            "occupancy": occupancy
        }
        self.send(data)
        decoded_json = self.receive()
        self.authority = decoded_json["auth"]
        self.signal_58 = decoded_json["sig58"]
        self.signal_62 = decoded_json["sig62"]
        self.ws_tm_authority.emit(self.authority)

   
    @pyqtSlot(list)
    def update_maintenance(self, maint_prop):
        data = {
            "input" : "ctc_maintenance",
            "maint": maint_prop
        }
        self.send(data)
        decoded_json = self.receive()
        self.maintenance = decoded_json["maint"]
        self.ws_tm_maintenance.emit(self.maintenance)
        self.ws_ctc_maintenance.emit(self.maintenance)

    @pyqtSlot(int)
    def update_switch(self, exit_block):
        sw = False
        if exit_block == 0:
            sw = False
        elif exit_block == 76:
            sw = True
        
        data = {
            "input" : "ctc_suggested_switch",
            "switch": sw
        }
        self.send(data)
        decoded_json = self.receive()
        result = decoded_json["result"]
        self.switch_58 = decoded_json["sw58"]
        self.switch_62 = decoded_json["sw62"]
        self.signal_58 = decoded_json["sig58"]
        self.signal_62 = decoded_json["sig62"]
        self.ws_ctc_switch_result.emit({"result": result, "switch_58": self.switch_58, "switch_62": self.switch_62, "signal_58": self.signal_58, "signal_62": self.signal_62})
        self.ws_tm_update_track.emit({"switch_58": self.switch_58, "switch_62": self.switch_62, "signal_58": self.signal_58, "signal_62": self.signal_62})
        self.ws_tm_authority.emit(self.authority)



if __name__ == "__main__":
    ws = WaysideWindow()
    ws.client_socket.sendall("Hello, World!")