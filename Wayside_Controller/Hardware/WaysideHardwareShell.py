import importlib.util
import copy
import socket
import json
from PyQt6.QtCore import pyqtSignal, QObject
import sys
from time import time

class WaysideShell:
    tm_ws_occupancy = pyqtSignal(list)
    ws_tm_authority = pyqtSignal(list)
    ws_tm_switch_58 = pyqtSignal(bool)
    ws_tm_switch_62 = pyqtSignal(bool)
    ws_tm_signal_58 = pyqtSignal(bool)
    ws_tm_signal_62 = pyqtSignal(bool)
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

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = '192.168.137.222'
        self.server_port = 12345

        start = time()
        self.client_socket.connect((self.server_ip, self.server_port))
        end = time()    
        print(f"Connected to server {end - start} seconds") 

    def send(self):
        data = {
        "authority": self.authority,
        "occupancy": self.occupancy,
        "switch_bool": self.switch_bool,
        "maintenance": self.maintenance,
        "exit": self.exit
        }
   

        self.client_socket.sendall(json.dumps(data).encode('utf-8'))

        response = self.client_socket.recv(4096)
        print("data received")
        return json.loads(response.decode('utf-8'))
        



if __name__ == "__main__":
    wayside = WaysideShell()
    while True:
        message = input("Press enter to send data, press q to quit: ")
        if message == "q":
            wayside.exit = True
            wayside.send()
            break
        else:
            wayside.send()
