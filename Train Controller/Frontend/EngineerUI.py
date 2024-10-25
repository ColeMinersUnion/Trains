import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from TCBackend import TCBackend

class EngineerUI(QWidget):
    Kp_Ki_Updated = pyqtSignal(int)
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('Engineer UI')

        layout = QVBoxLayout()

        self.statusLabel = QLabel('Status: ')
        self.brakeLabel = QLabel('Brake: ')
        self.powerOutputLabel = QLabel('Power Output: ')

        layout.addWidget(self.statusLabel)
        layout.addWidget(self.brakeLabel)
        layout.addWidget(self.powerOutputLabel)

        self.setLayout(layout)

        self.TCBackend = TCBackend()
        self.TCBackend.result_updated.connect(self.update_values)
        self.TCBackend.values_updated.connect(self.update_values)

    @pyqtSlot(dict)
    def update_values(self, values):
        self.statusLabel.setText(f'Status: {values["status"]}')
        self.brakeLabel.setText(f'Brake: {values["brake"]}')
        self.powerOutputLabel.setText(f'Power Output: {values["power_output"]}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    engineer_ui = EngineerUI()
    engineer_ui.show()
    sys.exit(app.exec_())