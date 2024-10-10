import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap, QFont
import backend
from PyQt5.QtCore import pyqtSignal

class LightsAndDoorsUI(QWidget):
    inputs_updated = pyqtSignal()
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Lights and Doors Module")
        self.setGeometry(100, 100, 800, 600)

        font = QFont()
        font.setPointSize(12)

        # Create a layout for the top row of buttons
        top_button_layout = QHBoxLayout()
        top_button1 = QPushButton("Right Doors")
        top_button1.setFont(font)
        top_button_layout.addWidget(top_button1)

        # Load the image
        image_path = os.path.join(os.path.dirname(__file__), "trains.png")
        image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Error: Unable to load image '{image_path}'.")
        else:
            image_label.setPixmap(pixmap)
            image_label.setScaledContents(True)
            image_label.setMinimumSize(400, 300)

        image_layout = QGridLayout()
        left_button = QPushButton("Headlights")
        left_button.setFont(font)
        right_button = QPushButton("Internal Lights")
        right_button.setFont(font)
        image_layout.addWidget(left_button, 0, 0)
        image_layout.addWidget(image_label, 0, 1, 2, 2)
        image_layout.addWidget(right_button, 1, 0)

        # Create a layout for the bottom row of buttons
        bottom_button_layout = QHBoxLayout()
        bottom_button1 = QPushButton("Left Doors")
        bottom_button1.setFont(font)
        bottom_button_layout.addWidget(bottom_button1)

        control_group_box = QGroupBox("Controls")
        control_layout = QVBoxLayout()
        control_layout.addLayout(top_button_layout)
        control_layout.addLayout(image_layout)
        control_layout.addLayout(bottom_button_layout)
        control_group_box.setLayout(control_layout)

        status_group_box = QGroupBox("Status")
        status_layout = QVBoxLayout()
        status_label = QLabel("Current Status:")
        status_label.setFont(font)
        status_layout.addWidget(status_label)
        status_group_box.setLayout(status_layout)

        # Create a main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(control_group_box)
        main_layout.addWidget(status_group_box)
        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = LightsAndDoorsUI()
    widget.show()
    sys.exit(app.exec_())