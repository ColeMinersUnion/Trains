from PyQt6 import*
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSlot , pyqtSignal, QObject
import socket
import time
import json

    


class WaysideHardwareBackend:

    wsh_tm_sw58 = pyqtSignal(bool)
    wsh_tm_sw62 = pyqtSignal(bool)
    wsh_tm_sig58 = pyqtSignal(bool)
    wsh_tm_sig62 = pyqtSignal(bool)

    def __init__(self):
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


    def connect(self):
        start = time()
        self.client_socket.connect((self.server_ip, self.server_port))
        end = time()    
        print(f"Connected to server {end - start} seconds") 
        data = {
            "input" : "say_hi"
        }

        self.send(data)
        decoded_json = self.receive()

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


    @pyqtSlot()
    def toggle_sw58(self):
        print("called toggle_sw58")
        data = {
            "input": "ws_sw58"
        }
        self.send(data)
        decoded_json = self.receive()
        self.switch_58 = decoded_json["sw58"]
        self.wsh_tm_sw58.emit(self.switch_58)

    @pyqtSlot()
    def toggle_sw62(self):
        print("called toggle_sw62")
        data = {
            "input": "ws_sw62"
        }
        self.send(data)
        decoded_json = self.receive()
        self.switch_62 = decoded_json["sw62"]
        self.wsh_tm_sw62.emit(self.switch_62)

    @pyqtSlot()
    def toggle_sig58(self):
        print("called toggle_sig58")
        data = {
            "input": "ws_sig58"
        }
        self.send(data)
        decoded_json = self.receive()
        self.signal_58 = decoded_json["sig58"]
        self.wsh_tm_sig58.emit(self.signal_58)

    @pyqtSlot()
    def toggle_sig62(self):
        print("called toggle_sig62")
        data = {
            "input": "ws_sig62"
        }
        self.send(data)
        decoded_json = self.receive()
        self.signal_62 = decoded_json["sig62"]
        self.wsh_tm_sig62.emit(self.signal_62)
