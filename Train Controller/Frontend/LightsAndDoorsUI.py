import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QGridLayout, QSpacerItem, QSizePolicy
)
import backend
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import pyqtSignal, Qt

class LightsAndDoorsUI(QWidget):
    inputs_updated = pyqtSignal()

    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Lights and Doors Module")
        self.setGeometry(100, 100, 900, 600)

        # Font settings for buttons and labels
        font = QFont()
        font.setPointSize(12)

        # Create a layout for the top row of buttons
        top_button_layout = QHBoxLayout()
        right_doors_button = QPushButton("Open Right Doors")
        right_doors_button.setFont(font)
        right_doors_button.setStyleSheet("background-color: lightblue;")
        top_button_layout.addWidget(right_doors_button)

        # Create the image section
        image_path = os.path.join(os.path.dirname(__file__), "trains.png")
        image_label = QLabel(self)
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print(f"Error: Unable to load image '{image_path}'.")
        else:
            image_label.setPixmap(pixmap)
            image_label.setScaledContents(True)
            image_label.setFixedSize(400, 300)

        # Add buttons to the left and right of the image
        image_layout = QGridLayout()
        headlights_button = QPushButton("Toggle Headlights")
        headlights_button.setFont(font)
        headlights_button.setStyleSheet("background-color: lightgreen;")
        internal_lights_button = QPushButton("Toggle Internal Lights")
        internal_lights_button.setFont(font)
        internal_lights_button.setStyleSheet("background-color: lightgreen;")
        image_layout.addWidget(headlights_button, 0, 0, Qt.AlignTop)
        image_layout.addWidget(image_label, 0, 1, 2, 2, Qt.AlignCenter)
        image_layout.addWidget(internal_lights_button, 1, 0, Qt.AlignBottom)

        # Create a layout for the bottom row of buttons
        bottom_button_layout = QHBoxLayout()
        left_doors_button = QPushButton("Open Left Doors")
        left_doors_button.setFont(font)
        left_doors_button.setStyleSheet("background-color: lightblue;")
        bottom_button_layout.addWidget(left_doors_button)

        # Add spacing to make the UI look more professional
        bottom_button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Group the controls in a GroupBox
        control_group_box = QGroupBox("Controls")
        control_group_box.setStyleSheet("QGroupBox { font-size: 14pt; font-weight: bold; }")
        control_layout = QVBoxLayout()
        control_layout.addLayout(top_button_layout)
        control_layout.addLayout(image_layout)
        control_layout.addLayout(bottom_button_layout)
        control_group_box.setLayout(control_layout)

        # Status Section
        status_group_box = QGroupBox("Status")
        status_group_box.setStyleSheet("QGroupBox { font-size: 14pt; font-weight: bold; }")
        status_layout = QVBoxLayout()
        status_label = QLabel("Current Status: ")
        status_label.setFont(font)
        status_layout.addWidget(status_label)

        # Adding dynamic status for door and light states
        status_right_door = QLabel("Right Doors: Closed")
        status_right_door.setFont(font)
        status_layout.addWidget(status_right_door)

        status_left_door = QLabel("Left Doors: Closed")
        status_left_door.setFont(font)
        status_layout.addWidget(status_left_door)

        status_headlights = QLabel("Headlights: Off")
        status_headlights.setFont(font)
        status_layout.addWidget(status_headlights)

        status_internal_lights = QLabel("Internal Lights: Off")
        status_internal_lights.setFont(font)
        status_layout.addWidget(status_internal_lights)

        status_group_box.setLayout(status_layout)

        # Create a main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(control_group_box)
        main_layout.addWidget(status_group_box)

        self.setLayout(main_layout)

        # Connecting buttons to actions (just as examples)
        right_doors_button.clicked.connect(lambda: self.update_status(status_right_door, "Right Doors"))
        left_doors_button.clicked.connect(lambda: self.update_status(status_left_door, "Left Doors"))
        headlights_button.clicked.connect(lambda: self.update_status(status_headlights, "Headlights"))
        internal_lights_button.clicked.connect(lambda: self.update_status(status_internal_lights, "Internal Lights"))

    def update_status(self, label, component):
        current_text = label.text().split(": ")[1]
        if current_text == "Closed" or current_text == "Off":
            new_status = "Open" if "Doors" in component else "On"
        else:
            new_status = "Closed" if "Doors" in component else "Off"

        label.setText(f"{component}: {new_status}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Assuming backend exists, pass it here. For now using None.
    widget = LightsAndDoorsUI(backend=None)
    widget.show()
    
    sys.exit(app.exec_())
