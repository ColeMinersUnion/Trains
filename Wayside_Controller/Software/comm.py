import sys
from PyQt6.QtWidgets import QApplication
from SoftwareShell import WaysideShell
from TM_test import Track

def main():
    
    tm=Track()
    wss=WaysideShell()

    #connect track model input of updated occupancy to wayside shell's update_occupancy function
    tm.tm_wss_occupancy.connect(wss.update_occupancy)
    print("success!")

if __name__ == "__main__":
    main()