from TrackModel.TrackModelMain import Map, SignalHandler
from Wayside_Controller.Software.SoftwareShell import WaysideShell
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)

    ws_window = WaysideShell()
    tm_window = Map()   
    tm_signals = SignalHandler()

    # Show both windows
    ws_window.ui.show()
    tm_window.show()

    ws_window.wss_tm_switch_13.connect(tm_signals.getSwitch13)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()