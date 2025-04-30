from PyQt6.QtWidgets import QWidget, QPushButton, QComboBox, QHBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal

greenSwitches = [(13, 1, 12), (28, 29, 150), (58, 57, 0), (62, 63, 0), (77, 76, 101), (85, 86, 100)]

class SwitchWidget(QWidget):
    emitSwitch = pyqtSignal(tuple)
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.switches = QComboBox()
        self.switches.addItems([f'Switch {i[0]}' for i in greenSwitches])
        self.layout.addWidget(self.switches)

        self.submit = QPushButton()
        self.submit.setText("Submit")
        self.submit.released.connect(self.onSubmit)
        self.submit_state = True
        self.layout.addWidget(self.submit)
        self.setLayout(self.layout)

    def onSubmit(self):
        self.submit_state = False
        self.submit.setChecked(self.submit_state)  
        switch= self.switches.currentIndex()
        self.emitSwitch.emit(greenSwitches[switch])
        self.submit_state = True