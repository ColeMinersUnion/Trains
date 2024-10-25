from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QObject
from TestbenchUI import TestbenchUI
from DriverUI import DriverUI
from TCBackend import TCBackend
from EngineerUI import EngineerUI

import sys

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.driverUI = DriverUI()
        self.testbenchUI = TestbenchUI(DriverUI)
        self.backend = TCBackend()
        self.engineer = EngineerUI()

        self.driver_ui.values_sent.connect(self.backend.calculate_and_update)

        # Add the UIs to the main window

        # Show the main window
        self.driverUI.show()
        self.testbenchUI.show()
        self.engineer.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main()
    sys.exit(app.exec_())