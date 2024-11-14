import sys
from PyQt6.QtWidgets import QApplication
from Hardware.HardwareShell import WaysideWindow
from TrackModel.TrackModelFrontend import Map
# from Train.combined import combined

def main():
    app = QApplication(sys.argv)
    tm = Map()
    wshw = WaysideWindow()
    # tr = combined()
    # tr.CC.show()
    # tr.main_window.show()
    wshw.show()
    tm.show()



    

    sys.exit(app.exec())


if __name__ == "__main__":
    main()