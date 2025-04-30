import sys
from PyQt6.QtWidgets import QApplication
from SoftwareShell import WaysideShell
#from TrackModelFrontend import Map 
from TM_test import Track

def main():

    app = QApplication(sys.argv)

    wayside = WaysideShell()
    #insert obj from track model
    tm=Track()
    #insert connection to track model that updates occupancy in WaysideShell
    tm.tm_ws_occupancy.connect(wayside.update_occupancy)

    wayside.show()

    sys.exit(app.exec())
    
if __name__== "__main__":
    main()
