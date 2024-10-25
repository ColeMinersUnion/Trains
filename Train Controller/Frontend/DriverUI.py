import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QApplication
from PyQt5.QtCore import pyqtSignal
from TCBackend import TCBackend
from TestbenchUI import TestbenchUI


class DriverUI(QWidget):
    update_values = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Driver UI")
        self.backend = TCBackend()
        self.testbench =  TestbenchUI(DriverUI)

        self.backend.result_updated.connect(self.updateUIWithResult)
        self.curr_status = 0
        self.curr_pwr = 0
        self.curr_brake = 0


        self.layout = QVBoxLayout()

        # Initialize status def
        self.statusLabel = QLabel("Enter Status:")
        self.statusInput = QLineEdit()
        self.layout.addWidget(self.statusLabel)
        self.layout.addWidget(self.statusInput)

        #power ui 
        self.powerLabel = QLabel("Enter Power:")
        self.powerInput = QLineEdit()
        self.layout.addWidget(self.powerLabel)
        self.layout.addWidget(self.powerInput)

        #brake ui
        self.brakeLabel = QLabel("Enter Brake:")
        self.brakeInput = QLineEdit()
        self.layout.addWidget(self.brakeLabel)
        self.layout.addWidget(self.brakeInput)


        
        self.calculateButton = QPushButton("Calculate")
        self.layout.addWidget(self.calculateButton)
        self.layout.addWidget(self.resultLabel)

        self.setLayout(self.layout)

        self.calculateButton.clicked.connect(self.onCalculateButtonClicked)

    def updateUIWithResult(self, result):
        # Update the UI with the received result
        self.resultLabel.setText(f"Result: {result['result']}")

    def onCalculateButtonClicked(self):
        # Get the input values from the UI
        #new value
        status = self.statusInput.text()
        power = self.powerInput.text()
        brake = self.brakeInput.text()

        # Set the values in the backend using the setters
        self.backend.status = status
        self.backend.power = power
        self.backend.brake = brake

        # Call the calculate_and_update method to process the values
        self.backend.calculate_and_update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    driverui = DriverUI()
    driverui.show()
    sys.exit(app.exec_())