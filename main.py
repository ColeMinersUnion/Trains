import sys
from CTC_Office.Frontend.app import CTCApplication
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSlot
from TM_TC_NewArch.TrainWrapper import Train
from Wayside_Controller.Software.SoftwareShell import WaysideShell as SoftwareShell
from Wayside_Controller.Hardware.HardwareShell import WaysideWindow as HardwareShell
from TrackModel.TrackModelMain import Map

trains = []

app = QApplication(sys.argv)

ctc = CTCApplication()
wss_window = SoftwareShell()
wsh_window = HardwareShell()
tm_window = Map()   
tm_signals = tm_window.signals

ctc.emitMaintenance.connect(wss_window.receive_maintenance)

#Emit Connect Slot
wss_window.wss_ctc_occupancy.connect(ctc.updateOccupancy)
wsh_window.wsh_ctc_occupancy.connect(ctc.updateOccupancy)
#wsh_window.ws_ctc_switch_result.connect(ctc.handleGreenOutputSwitch)



@pyqtSlot(list, str)
def trainFactory(routeInfo: list, authority: str):
    try:
        trains.append(Train(routeInfo, authority))
        trains[-1].train_model_view.show()
        trains[-1].train_controller_view.show()
        trains[-1].train_model.block_change.connect(tm_signals.toggleOcc)
        # sends authorities as list of booleans
        #tm_signals.sendAuthorities.connect(trains[-1].)
        # sends list as station block number and passengers boarding
        #tm_signals.sendPassengers.connect(trains[-1].)
        # sends list as station block number and passengers unboarding
        #trains[-1].train_model.###.connect(tm_signals.getPassengers)
        # sends request for beacon data as block number
        #trains[-1].train_model.###.connect(tm_signals.getBeacon)
        # sends beacon data as list with block number and beacon data
        #tm_signals.sendBeacon.connect(trains[-1].beaconIntake)
    except TypeError:
        print('Oops')
    except IndexError:
        print('Train reach end of line. Went back to the yard')


# Show both windows

#tk sending occupancies to wss
tm_signals.sendOccupancies.connect(wss_window.update_occupancy)
tm_signals.sendOccupancies.connect(wsh_window.update_occupancy)
#wss sending updated authority to tk:
wss_window.wss_tm_authority.connect(tm_signals.getSoftwareAuthority)
wss_window.wss_tm_switch_13.connect(tm_signals.getSwitch13)
wss_window.wss_tm_switch_28.connect(tm_signals.getSwitch28)
wss_window.wss_tm_switch_77.connect(tm_signals.getSwitch77)
wss_window.wss_tm_switch_85.connect(tm_signals.getSwitch85)
wsh_window.wsh_tm_switch_58.connect(tm_signals.getSwitch58)
wsh_window.wsh_tm_switch_62.connect(tm_signals.getSwitch62)
wsh_window.wsh_tm_authority.connect(tm_signals.getHardwareAuthority)
#tk passes authority to tm


ctc.emitTrain.connect(trainFactory)


wss_window.show()
tm_window.show()
wsh_window.show()
ctc.show()


#Emit Connect Slot
sys.exit(app.exec())

