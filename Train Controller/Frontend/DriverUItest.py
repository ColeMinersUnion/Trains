# CommandCenter.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from Testbench import TestbenchUI
from backend import Backend
from EngineerView import EngineerView
from LightsAndDoorsUI import LightsAndDoorsUI

class DriverUI(QWidget):
    def __init__(self):
        super().__init__()
        self.backend = Backend()
        self.testbench_ui = TestbenchUI(self.backend)
        self.testbench_ui.inputs_updated.connect(self.update_values)
        self.engineer_view = EngineerView(self.backend)
        self.engineer_view.Kp_Ki_updated.connect(self.update_values)
        self.lights_and_doors_ui = LightsAndDoorsUI(self.backend)
        self.lights_and_doors_ui.inputs_updated.connect(self.update_values)
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_values)
        self.timer.start(1000)  # 1000ms = 1s
        self.authority_timer = QTimer()
        self.authority_timer.timeout.connect(self.update_authority)
        self.authority_timer.start(1000)  # 1000ms = 1s
        self.brake_applied = False
        self.speed_decrease_timer = QTimer()
        self.speed_decrease_timer.timeout.connect(self.update_speed)
        # ... (rest of your code)

    def initUI(self):
        self.setWindowTitle("Command Center")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        font = QFont()
        font.setPointSize(12)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial;
            }
            QPushButton {
                background-color: #35c0db;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton#emergency_brake {
                background-color: #FF0000;
                color: white;
                border: none;
                padding: 16px 32px;
                font-size: 12px;
                border-radius: 8px;
            }
            QPushButton#service_brake {
                background-color: #FFFF00;
                color: black;
                border: none;
                padding: 16px 32px;
                font-size: 24px;
                border-radius: 8px;
            }
            QPushButton {
                min-width: 150px;
                min-height: 40px;
            }
            QLabel {
                min-height: 30px;
            }
        """)

        # Button to open Testbench UI
        self.testbench_button = QPushButton("Open Testbench", self)
        self.testbench_button.setFixedHeight(40)
        self.testbench_button.setFont(font)
        self.testbench_button.clicked.connect(self.open_testbench)
        layout.addWidget(self.testbench_button)

        # Button to open Engineer View
        self.engineer_button = QPushButton("Open Engineer View", self)
        self.engineer_button.clicked.connect(self.open_engineer_view)
        layout.addWidget(self.engineer_button)

        self.LDS_button = QPushButton("Open Lights and Doors Mod", self)
        self.LDS_button.clicked.connect(self.open_lds)
        layout.addWidget(self.LDS_button)

        # Button to open LDS
        # self.lds_button = QPushButton("Open Lights and Doors Override", self)
        # self.lds_button.clicked.connect(self.open_lds)
        # layout.addWidget(self.lds_button)

        # Labels to display speed, authority, and brake status
        self.speed_label = QLabel(f"Commanded Speed: {self.backend.commanded_speed}")
        self.authority_label = QLabel(f"Authority: {self.backend.authority}")
        self.brake_status_label = QLabel(f"Brake Status: {self.backend.brake_status}")
        self.suggested_speed_label = QLabel(f"Suggested Speed: {self.backend.suggested_speed}")
        self.Kp_Label = QLabel(f"Kp: {self.backend.Kp}")
        self.Ki_Label = QLabel(f"Ki: {self.backend.Ki}")
        self.currentSpeed_label = QLabel(f"Current Speed: {self.backend.safe_speed()}")
        self.power_output_label = QLabel(f"Power Output: {self.backend.power_output}")
        self.door_status_label = QLabel(f"Door Status: {self.backend.door_status}")
        self.lights_status_label = QLabel(f"Lights Status: {self.backend.lights_status}")
        self.temperature_label = QLabel(f"Internal Temperature: {self.backend.internal_temperature}")
        self.hl_status_label = QLabel(f"Headlights Status: {self.backend.headlights_status}")
        self.speed_limit_label = QLabel(f"Speed Limit: {self.backend.speed_limit}")

        for label in [self.speed_label, self.authority_label, self.brake_status_label, self.suggested_speed_label, self.Kp_Label, self.Ki_Label, self.power_output_label, self.door_status_label, self.lights_status_label, self.temperature_label, self.hl_status_label, self.speed_limit_label]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)

        # Brake buttons
        brake_layout = QHBoxLayout()
        self.emergency_brake_button = QPushButton("Emergency Brake")
        self.emergency_brake_button.setFixedHeight(100)
        self.emergency_brake_button.setFixedWidth(200)
        self.emergency_brake_button.setFont(font)
        self.emergency_brake_button.setStyleSheet("background-color: #FF0000; color: white; border: none; padding: 16px 32px; font-size: 16px; border-radius: 8px;")
        #self.emergency_brake_button.clicked.connect(self.backend.brake_status)
        brake_layout.addWidget(self.emergency_brake_button)

        self.service_brake_button = QPushButton("Service Brake")
        self.service_brake_button.setFixedHeight(100)
        self.service_brake_button.setFixedWidth(200)
        self.service_brake_button.setFont(font)
        self.service_brake_button.setStyleSheet("background-color: #db6740; color: white;  border: none; padding: 16px 32px; font-size: 16px;  border-radius: 8px;")

        #self.service_brake_button.clicked.connect(self.backend.brake_status)
        brake_layout.addWidget(self.service_brake_button)

        layout.addLayout(brake_layout)

        self.setLayout(layout)

    def open_testbench(self):
        # Open the Testbench UI
        #self.testbench_ui = TestbenchUI(self.backend)
        #self.testbench_ui.inputs_updated.connect(self.update_values)
        self.testbench_ui.show()

    def  open_engineer_view(self):
        # Open the Engineer View UI
        #self.engineer_view = EngineerView(self.backend)
        #self.engineer_view.Kp_Ki_updated.connect(self.update_values)
        self.engineer_view.show()

    def open_lds(self):
        # Open the LDS UI
     #   self.lds_ui = LightsAndDoorsUI(self.backend)
        self.lights_and_doors_ui.show()

    def update_authority(self):
        speed = self.backend.commanded_speed
        if speed > 0:
            self.backend.authority -= speed / 10  # decrease authority proportional to speed
            self.update_values()
            if self.backend.authority < 10:
                self.backend.brake_status = 1
                self.update_values()
            if self.backend.authority < 0:
                self.backend.authority = 0
                self.update_values()
            self.authority_label.setText(f"Authority: {self.backend.authority:.2f}")
        else:
            self.timer.stop()  # stop the timer when speed is 0
    def update_speed(self):
        if self.brake_applied:
            currentSpeed = self.backend.safe_speed()
            self.update_values()
            if currentSpeed > 0:
                self.backend.set_safe_speed(currentSpeed - 1)  # decrease speed by 1 unit every second
                self.update_values()
            else:
                self.backend.set_safe_speed(0)  # set speed to 0 when it reaches 0
                self.brake_applied = False
                self.speed_decrease_timer.stop()
                self.update_values()
    def update_values(self):
        commanded_speed, authority, brake_status, suggested_speed, currentSpeed, power_output, door_status, lights_status, internal_temperature, headlights_status, speed_limit = self.backend.get_testbench_status()
        Kp, Ki =  self.backend.get_Kp_Ki()
        #TODO figure out how to put LightsAndDoorsUI here

        # Get the latest values from the backend and update the labels
        #result = Backend.get_testbench_status()
        self.speed_label.setText(f"Speed: {commanded_speed}")
        self.authority_label.setText(f"Authority: {authority:.2f}")
        self.brake_status_label.setText(f"Brake Status: {'ON' if brake_status else 'OFF'}")
        self.suggested_speed_label.setText(f"Suggested Speed: {suggested_speed}")
        self.Kp_Label.setText(f"Kp: {Kp}")
        self.Ki_Label.setText(f"Ki: {Ki}")
        self.currentSpeed_label.setText(f"Current Speed: {currentSpeed}")
        self.power_output_label.setText(f"Power Output: {power_output}")
        self.door_status_label.setText(f"Door Status: {'Open'if door_status else 'Closed'}")
        self.lights_status_label.setText(f"Lights Status: {'ON' if lights_status else 'OFF'}")
        self.temperature_label.setText(f"Internal Temperature: {internal_temperature}")
        self.hl_status_label.setText(f"Headlights Status: {'ON' if headlights_status else 'OFF'}")
        self.speed_limit_label.setText(f"Speed Limit: {speed_limit}")

def main():
    app = QApplication(sys.argv)

    # Create and show the main CommandCenter window
    command_center = CommandCenter()
    command_center.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
