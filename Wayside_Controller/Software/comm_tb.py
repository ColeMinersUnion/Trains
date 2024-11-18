import sys
from PyQt6.QtWidgets import QApplication
from SoftwareShell2 import Wayside_Shell
from TM_test import Track

def main():
    
    tm=Track()
    ws=Wayside_Shell()

    #connect track model input of updated occupancy to wayside shell's update_occupancy function
    tm.tm_ws_occupancy.connect(ws.update_occupancy)
    print("success!")

if __name__ == "__main__":
    main()