# app.py
import sys
from PyQt6.QtWidgets import QApplication
from HardwareShell import WaysideWindow
from TrackModelTest import TrackModelWindow
from CtcTest import CTCWindow
from wsh_view import WaysideHardwareView
from wsh_controller import WaysideHardwareController
from wsh_model import WaysideHardwareModel

def main():
    app = QApplication(sys.argv)

    ws_window = WaysideWindow()
    # Instantiate the windows
    tm_window = TrackModelWindow()
    ctc_window = CTCWindow()

    # Connect the signal from sender to the slot in receiver
    tm_window.tm_ws_occupancy.connect(ws_window.update_occupancy)
    ws_window.ws_tm_authority.connect(tm_window.update_authority)
    ctc_window.ctc_ws_sugg_switch.connect(ws_window.update_switch)
    ws_window.ws_ctc_switch_result.connect(ctc_window.update_track)
    #ws_window.ws_tm_update_track.connect(tm_window.update_track)
    ctc_window.ctc_ws_maintenance.connect(ws_window.update_maintenance)
    ws_window.ws_tm_maintenance.connect(tm_window.update_maintenance)
    ws_window.wsh_ctc_occupancy.connect(ctc_window.update_occupancy)
    ws_window.wsh_ctc_maintenance.connect(ctc_window.update_maintenance)
    ctc_window.ctc_ws_maint_switch.connect(ws_window.update_maint_switch)
    # Show both windows
    ws_window.show()
    tm_window.show()
    ctc_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
