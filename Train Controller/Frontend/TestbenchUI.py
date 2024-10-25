import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QApplication
from PyQt5.QtCore import pyqtSignal

class TestbenchUI(QWidget):
    values_updated = pyqtSignal(str, str, str)

    def __init__(self, driver_ui):
        super().__init__()
        self.setWindowTitle("Testbench UI")
        self.driver_ui = driver_ui

        self.statusLabel = QLabel("Status:")
        self.statusInput = QLineEdit()
        self.powerLabel = QLabel("Power:")
        self.powerInput = QLineEdit()
        self.brakeLabel = QLabel("Brake:")
        self.brakeInput = QLineEdit()
        self.sendButton = QPushButton("Send to Driver UI")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.statusLabel)
        self.layout.addWidget(self.statusInput)
        self.layout.addWidget(self.powerLabel)
        self.layout.addWidget(self.powerInput)
        self.layout.addWidget(self.brakeLabel)
        self.layout.addWidget(self.brakeInput)
        self.layout.addWidget(self.sendButton)

        self.setLayout(self.layout)

        self.sendButton.clicked.connect(self.onSendButtonClicked)

        self.values_updated.connect(self.driver_ui.update_values)

    def onSendButtonClicked(self):
        status = self.statusInput.text()
        power = self.powerInput.text()
        brake = self.brakeInput.text()

        self.values_updated.emit(status, power, brake)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    testbench_ui = TestbenchUI()
    testbench_ui.show()
    sys.exit(app.exec_())