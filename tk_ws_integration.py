from TrackModel.TrackModelMain import Map, SignalHandler
from Wayside_Controller.Software.SoftwareShell import WaysideShell
from Wayside_Controller.Hardware.HardwareShell import WaysideWindow
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)

    wss_window = WaysideShell()
    wsh_window = WaysideWindow()
    tm_window = Map()   
    tm_signals = tm_window.signals

    # Show both windows
    wss_window.show()
    tm_window.show()
    wsh_window.show()

    wss_window.wss_tm_switch_13.connect(tm_signals.getSwitch13)
    wss_window.wss_tm_switch_28.connect(tm_signals.getSwitch28)
    wss_window.wss_tm_switch_77.connect(tm_signals.getSwitch77)
    wss_window.wss_tm_switch_85.connect(tm_signals.getSwitch85)
    wsh_window.wsh_tm_switch_58.connect(tm_signals.getSwitch58)
    wsh_window.wsh_tm_switch_62.connect(tm_signals.getSwitch62)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()