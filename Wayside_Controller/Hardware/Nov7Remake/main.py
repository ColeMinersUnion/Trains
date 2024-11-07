# app.py
import sys
from PyQt6.QtWidgets import QApplication
from Shell import WaysideWindow
from TrackModelTest import TrackModelWindow

def main():
    app = QApplication(sys.argv)

    # Instantiate the windows
    ws_window  = WaysideWindow()
    tm_window = TrackModelWindow()

    # Connect the signal from sender to the slot in receiver
    tm_window.tm_ws_occupancy.connect(ws_window.update_occupancy)
    ws_window.ws_tm_authority.connect(tm_window.update_authority)
    # Show both windows
    ws_window.show()
    tm_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
