# LightsAndDoorsUI.py
import sys
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QCheckBox, QApplication, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, pyqtSignal
#from Backend import Backend  
from CombinedBackend import Train

class LightsAndDoorsUI(QWidget):
    lds_updated = pyqtSignal()
    def __init__(self, Train):
        super().__init__()
        self.backend = Train
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Lights and Doors Control")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Train Image
        self.train_scene = QGraphicsScene(self)
        self.train_view = QGraphicsView(self.train_scene)
        
        image_path = "LightsAndDoors.png"
        if not os.path.exists(image_path):
            print("Image file not found.")
        else:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                print("Failed to load image.")
            else:
                print(f"Image size: {pixmap.size()}")
                self.train_pixmap_item = QGraphicsPixmapItem(pixmap)
                self.train_scene.addItem(self.train_pixmap_item)
                self.train_scene.setSceneRect(self.train_pixmap_item.boundingRect())  # Set scene rect to the image size
                self.train_view.setFixedSize(600, 400)  # Set a fixed size for the view
                self.train_scene.setBackgroundBrush(QColor(255, 255, 255))  # Set a white background

        layout.addWidget(self.train_view)

        # Lights Control
        self.lights_checkbox = QCheckBox("Turn On Lights")
        self.lights_checkbox.stateChanged.connect(self.toggle_lights)
        layout.addWidget(self.lights_checkbox)

        # Headlights Control
        self.headlights_checkbox = QCheckBox("Turn On Headlights")
        self.headlights_checkbox.stateChanged.connect(self.toggle_headlights)
        layout.addWidget(self.headlights_checkbox)

        # Brake Control
        self.brake_button = QPushButton("Toggle Brake Status")
        self.brake_button.setFixedSize(200, 100)  # Set a fixed size for the button (width, height)
        self.brake_button.setStyleSheet("background-color: red; color: white; font-size: 16px;")  # Set background color to red and text color to white
        self.brake_button.clicked.connect(self.toggle_brake)
        layout.addWidget(self.brake_button)

        # Door Control
        self.door_button = QPushButton("Toggle Door Status")
        self.door_button.clicked.connect(self.toggle_door)
        layout.addWidget(self.door_button)

        self.setLayout(layout)

    def toggle_lights(self, state):
        if state == Qt.Checked:
            # Change the train image or highlight it
            #self.train_pixmap_item.setOpacity(1)  # Make it fully visible or change color
            self.backend.set_lights(True)  # Update backend status
            print(f"lights set to ON")
            self.lds_updated.emit()

        else:
            #self.train_pixmap_item.setOpacity(0.5)  # Dim the image to indicate lights off
            self.backend.set_lights(False)  # Update backend status
            print(f"lights set to OFF")
            self.lds_updated.emit()

    def toggle_headlights(self, state):
        if state == Qt.Checked:
            self.backend.set_headlights_status(True)  # Update backend status
            print(f"headlights set to ON")
            self.lds_updated.emit()

        else:
            self.backend.set_headlights_status(False)  # Update backend status
            print(f"headlights set to OFF")
            self.lds_updated.emit()


    def toggle_brake(self):
        current_status = self.backend.get_brake()
        new_status = not current_status
        self.backend.set_brake_status(new_status, 0)  # Update backend status
        print(f"Brake status set to: {'ON' if new_status else 'OFF'}")
        self.lds_updated.emit()

    def toggle_door(self):
        current_status = self.backend.get_doors()
        new_status = not current_status
        self.backend.set_door_status(new_status)  # Update backend status
        print(f"Door status set to: {'Open' if new_status else 'Closed'}")
        self.lds_updated.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    backend = Train()  # Replace with actual backend instance
    lights_and_doors_ui = LightsAndDoorsUI(backend)
    lights_and_doors_ui.show()
    sys.exit(app.exec())