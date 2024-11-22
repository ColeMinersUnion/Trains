from TrackModel.TrackModelMain import Map
from Wayside_Controller.Software.SoftwareShell import WaysideShell
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)

    ws_window = WaysideShell()
    tm_window = Map()   
    tm_signals = tm_window.signals

    # Show both windows
    ws_window.ui.show()
    tm_window.show()

    ws_window.wss_tm_switch_13.connect(tm_signals.getSwitch13)
    ws_window.wss_tm_switch_28.connect(tm_signals.getSwitch28)
    ws_window.wss_tm_switch_77.connect(tm_signals.getSwitch77)
    ws_window.wss_tm_switch_85.connect(tm_signals.getSwitch85)
    ws_window.wss_tm_crossing_19.connect(tm_signals.getCrossing19)
    ws_window.wss_tm_crossing_108.connect(tm_signals.getCrossing108)
    tm_signals.sendOccupancies.connect(ws_window.update_occupancy)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()