import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
import backend

class LightsAndDoorsUI(QWidget):
    LDS_Updated  = pyqtSignal()

    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Button to toggle lights
        self.lights_button = QPushButton("Lights: Off", self)
        self.lights_button.clicked.connect(self.toggle_lights)
        layout.addWidget(self.lights_button)

        # Button to toggle doors
        self.doors_button = QPushButton("Doors: Closed", self)
        self.doors_button.clicked.connect(self.toggle_doors)
        layout.addWidget(self.doors_button)

        # Button to toggle headlights
        self.headlights_button = QPushButton("Headlights: Off", self)
        self.headlights_button.clicked.connect(self.toggle_headlights)
        layout.addWidget(self.headlights_button)

        self.setLayout(layout)

    def toggle_lights(self):
        current_status = self.backend.get_lights_status()
        new_status = not current_status
        self.backend.set_lights_status(new_status)
        self.lights_button.setText(f"Lights: {'On' if new_status else 'Off'}")

    def toggle_doors(self):
        current_status = self.backend.get_door_status()
        new_status = not current_status
        self.backend.set_door_status(new_status)
        self.doors_button.setText(f"Doors: {'Open' if new_status else 'Closed'}")

    def toggle_headlights(self):
        current_status = self.backend.get_headlights_status()
        new_status = not current_status
        self.backend.set_headlights_status(new_status)
        self.headlights_button.setText(f"Headlights: {'On' if new_status else 'Off'}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = LightsAndDoorsUI()
    widget.show()
    sys.exit(app.exec_())