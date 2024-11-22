import sys
from CTC_Office.Frontend.app import CTCApplication
from PyQt6.QtWidgets import QApplication
from Wayside_Controller.Software.SoftwareShell import WaysideShell

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = CTCApplication()
    ex2 = WaysideShell()
    
    ex2.wss_ctc_occupancy.connect(ex.updateOccupancy)

    ex.show()
    ex2.ui.show()


    sys.exit(app.exec())

