import sys
from CTC_Office.Frontend.app import CTCApplication
from PyQt6.QtWidgets import QApplication
from Wayside_Controller.Software.SoftwareShell import WaysideShell as SoftwareShell
from Wayside_Controller.Hardware.HardwareShell import WaysideWindow as HardwareShell
if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = CTCApplication()
    ex2 = SoftwareShell()
    ex3 = HardwareShell()
    
    #Emit Connect Slot
    ex2.wss_ctc_occupancy.connect(ex.updateOccupancy)
    ex3.ws_ctc_occupancy.connect(ex.updateOccupancy)
    ex3.update_switch.connect(ex.handleGreenOutputSwitch)

    ex.show()
    ex2.ui.show()
    ex3.ui.show()


    sys.exit(app.exec())

