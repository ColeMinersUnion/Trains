import sys
from CTC_Office.Frontend.app import CTCApplication
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSlot
from TM_TC_NewArch.TrainWrapper import Train
from Wayside_Controller.Software.SoftwareShell import WaysideShell as SoftwareShell
from Wayside_Controller.Hardware.HardwareShell import WaysideWindow as HardwareShell
from TrackModel.TrackModelMain import Map

trains = [] # holds trains

app = QApplication(sys.argv) #new application

ctc = CTCApplication() #makes CTC
wss_window = SoftwareShell() #makes wayside software
wsh_window = HardwareShell() #makes wayside hardware
tm_window = Map() #makes track model map
tm_signals = tm_window.signals #gets signals from track model

ctc.emitMaintenance.connect(wss_window.receive_maintenance)
ctc.emitMaintenanceSwitch.connect(wss_window.receive_maint_switch)
wss_window.wss_ctc_safetyCheck.connect(ctc.MaintenanceResponse)
wss_window.wss_ctc_safetySwitch.connect(ctc.MaintenanceSwitchResponse)

#!Commented out by Cole. Can't break track while WSH is not connected to hardware
ctc.emitMaintenance.connect(wsh_window.update_maintenance)
wsh_window.wsh_ctc_safetyCheck.connect(ctc.MaintenanceResponse)
ctc.emitMaintenanceSwitch.connect(wsh_window.update_maint_switch)
#Emit Connect Slot
wss_window.wss_ctc_occupancy.connect(ctc.updateOccupancy) #wayside software send occupancies to CTC
wsh_window.wsh_ctc_occupancy.connect(ctc.updateOccupancy) #wayside hardware send occupancies to CTC
#wsh_window.ws_ctc_switch_result.connect(ctc.handleGreenOutputSwitch)





@pyqtSlot(list, str)
def trainFactory(routeInfo: list, authority: str):
    try:
        trains.append(Train(routeInfo, authority))
        trains[-1].train_model_view.show()
        trains[-1].train_controller_view.show()
        trains[-1].train_controller_model.train_at_yard.connect(deleteTrain)
        trains[-1].train_model.block_change.connect(tm_signals.toggleOcc)
        # sends authorities as list of booleans
        tm_signals.sendAuthorities.connect(trains[-1].train_model.boolean_authority)
        # sends list as station block number and passengers boarding
        tm_signals.sendPassengers.connect(trains[-1].train_model.addPassengersToTrain)
        # sends list as station block number and passengers unboarding
        trains[-1].train_model.unboarding_list_signal.connect(tm_signals.getPassengers)
        # sends request for beacon data as block number
        trains[-1].train_model.current_block_ID.connect(tm_signals.getBeacon)
        # sends beacon data as list with block number and beacon data
        tm_signals.sendBeacon.connect(trains[-1].train_model.beaconInformation)
    except TypeError:
        print('Oops')


@pyqtSlot()
def deleteTrain():
    try:
        trains[-1].train_model_view.close()
        trains[-1].train_controller_view.close()
        del trains[-1]
    except IndexError:
        print('No trains to delete')
    
    


# Show both windows

#track model sends occupancies to wayside software...
tm_signals.sendOccupancies.connect(wss_window.update_occupancy)
#... and hardware
tm_signals.sendOccupancies.connect(wsh_window.update_occupancy)
#wayside messages to track model
wss_window.wss_tm_authority.connect(tm_signals.getSoftwareAuthority) #software authority (0 to 40, 77 to 151) as list of booleans

wss_window.wss_tm_switch_13.connect(tm_signals.getSwitch13) #switch 13
wss_window.wss_tm_switch_28.connect(tm_signals.getSwitch28) #switch 28
wss_window.wss_tm_switch_77.connect(tm_signals.getSwitch77) #switch 77
wss_window.wss_tm_switch_85.connect(tm_signals.getSwitch85) #switch 85
wsh_window.wsh_tm_switch_58.connect(tm_signals.getSwitch58) #switch 58
wsh_window.wsh_tm_switch_62.connect(tm_signals.getSwitch62) #switch 62

wss_window.wss_tm_signal_13.connect(tm_signals.getSignal13) #signal 13
wss_window.wss_tm_signal_28.connect(tm_signals.getSignal28) #signal 28
wss_window.wss_tm_signal_77.connect(tm_signals.getSignal77) #signal 77
wss_window.wss_tm_signal_85.connect(tm_signals.getSignal85) #signal 85
wsh_window.wsh_tm_sig58.connect(tm_signals.getSignal58) #signal 58
wsh_window.wsh_tm_sig62.connect(tm_signals.getSignal62) #signal 62
wsh_window.wsh_tm_maint.connect(tm_signals.toggleOcc) 

wsh_window.wsh_tm_authority.connect(tm_signals.getHardwareAuthority) #hardware authority (41 to 76) as list of booleans
wss_window.wss_tm_authority.connect(tm_signals.getSoftwareAuthority) #software authority (0 to 40, 77 to 151) as list of booleans

#connects CTC to train command
ctc.emitTrain.connect(trainFactory)


wss_window.show() #show wayside software
tm_window.show() #show track model
wsh_window.show() #show wayside ahrdware
ctc.show() #show CTC

#allow exit
sys.exit(app.exec())

