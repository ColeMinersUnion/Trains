import sys
from CTC_Office.Frontend.app import CTCApplication
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSlot
from TM_TC_NewArch.TrainWrapper import Train
from Wayside_Controller.Software.SoftwareShell import WaysideShell as SoftwareShell
from Wayside_Controller.Hardware.HardwareShell import WaysideWindow as HardwareShell
from TrackModel.TrackModelMain import Map, SignalHandler

trains = []

@pyqtSlot(list, str)
def trainFactory(routeInfo: list, authority: str, tm_signals: SignalHandler):
    try:
        trains.append(Train(routeInfo, authority))
        trains[-1].train_model_view.show()
        trains[-1].train_controller_view.show()
        trains[-1].block_change.connect(tm_signals.addOcc)
    except TypeError:
        print('Oops')

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ctc = CTCApplication()
    wss_window = SoftwareShell()
    wsh_window = HardwareShell()
    
    #Emit Connect Slot
    wss_window.wss_ctc_occupancy.connect(ctc.updateOccupancy)
    wsh_window.wsh_ctc_occupancy.connect(ctc.updateOccupancy)
    #wsh_window.ws_ctc_switch_result.connect(ctc.handleGreenOutputSwitch)

    tm_window = Map()   
    tm_signals = SignalHandler()

    # Show both windows
    wss_window.show()
    tm_window.show()
    wsh_window.show()

    #tk sending occupancies to wss
    tm_signals.sendOccupancies.connect(wss_window.update_occupancy)
    #wss sending updated authority to tk:
    wss_window.wss_tm_authority.connect(tm_signals.getAuthority)
    wss_window.wss_tm_switch_13.connect(tm_signals.getSwitch13)
    wss_window.wss_tm_switch_28.connect(tm_signals.getSwitch28)
    wss_window.wss_tm_switch_77.connect(tm_signals.getSwitch77)
    wss_window.wss_tm_switch_85.connect(tm_signals.getSwitch85)
    wsh_window.wsh_tm_switch_58.connect(tm_signals.getSwitch58)
    wsh_window.wsh_tm_switch_62.connect(tm_signals.getSwitch62)
    wsh_window.wsh_tm_authority.connect(tm_signals.getAuthority)

    ctc.emitTrain.connect(lambda: trainFactory(tm_signals))

    ctc.show()
    wsh_window.show()
    wss_window.show()
    
    
    #Emit Connect Slot
    sys.exit(app.exec())

