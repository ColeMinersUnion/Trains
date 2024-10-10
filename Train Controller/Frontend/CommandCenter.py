# CommandCenter.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from Testbench import TestbenchUI
from backend import Backend
from EngineerView import EngineerView
#from LightsAndDoorsUI import LightsAndDoorsUI


class CommandCenter(QWidget):
    def __init__(self):
        super().__init__()
        self.backend = Backend()
        self.testbench_ui = TestbenchUI(self.backend)
        self.testbench_ui.inputs_updated.connect(self.update_values)
        self.engineer_view = EngineerView(self.backend)
        self.engineer_view.Kp_Ki_updated.connect(self.update_values)
      #  self.lds_ui =  LightsAndDoorsUI(self.backend)
       # self.lds_ui.LDS_Updated.connect(self.update_values)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Command Center")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial;
            }
            QPushButton {
                background-color: #007BFF;
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
            }
        """)

        # Button to open Testbench UI
        self.testbench_button = QPushButton("Open Testbench", self)
        self.testbench_button.setFixedHeight(40)
        self.testbench_button.clicked.connect(self.open_testbench)
        layout.addWidget(self.testbench_button)

        #Button to open Engineer View
        self.engineer_button = QPushButton("Open Engineer View", self)
        self.engineer_button.clicked.connect(self.open_engineer_view)
        layout.addWidget(self.engineer_button)

        #Button to open LDS
        #self.lds_button = QPushButton("Open Lights and Doors Override", self)
        #self.lds_button.clicked.connect(self.open_lds)
        #layout.addWidget(self.lds_button)

        # Labels to display speed, authority, and brake status
        self.speed_label = QLabel(f"Speed: {self.backend.commanded_speed}")
        self.authority_label = QLabel(f"Authority: {self.backend.authority}")
        self.brake_status_label = QLabel(f"Brake Status: {self.backend.brake_status}")
        self.suggested_speed_label = QLabel(f"Suggested Speed: {self.backend.suggested_speed}")
        self.Kp_Label =  QLabel(f"Kp: {self.backend.Kp}")
        self.Ki_Label =  QLabel(f"Ki: {self.backend.Ki}")
        self.current_speed_label = QLabel(f"Current Speed: {self.backend.current_speed}")
        self.power_output_label = QLabel(f"Power Output: {self.backend.power_output}")
        self.door_status_label  = QLabel(f"Door Status: {self.backend.door_status}")
        self.lights_status_label =  QLabel(f"Lights Status: {self.backend.lights_status}")
        self.temperature_label = QLabel(f"Internal Temperature: {self.backend.internal_temperature}")
        self.hl_status_label =  QLabel(f"Headlights Status: {self.backend.headlights_status}")
        self.speed_limit_label = QLabel(f"Speed Limit: {self.backend.speed_limit}")

        for label in [self.speed_label, self.authority_label, self.brake_status_label, self.suggested_speed_label, self.Kp_Label, self.Ki_Label,  self.current_speed_label, self.power_output_label, self.door_status_label, self.lights_status_label, self.temperature_label, self.hl_status_label, self.speed_limit_label]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)

        # Set layout
        self.setLayout(layout)

    #def update_Kp_Ki_values(self):
     #   Kp, Ki = self.backend.get_Kp_Ki()
      #  self.Kp_Label.setText(f"Kp: {Kp}")
       # self.Ki_Label.setText(f"Ki: {Ki}")

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

    #def open_lds(self):
        # Open the LDS UI
     #   self.lds_ui = LightsAndDoorsUI(self.backend)
      #  self.lds_ui.LDS_Updated.connect(self.update_values)

    def update_values(self):
        commanded_speed, authority, brake_status, suggested_speed, current_speed, power_output, door_status, lights_status, internal_temperature, headlights_status, speed_limit = self.backend.get_testbench_status()
        Kp, Ki =  self.backend.get_Kp_Ki()
        #TODO figure out how to put LightsAndDoorsUI here

        # Get the latest values from the backend and update the labels
        #result = Backend.get_testbench_status()
        self.speed_label.setText(f"Speed: {commanded_speed}")
        self.authority_label.setText(f"Authority: {authority}")
        self.brake_status_label.setText(f"Brake Status: {'Applied' if brake_status else 'Released'}")
        self.suggested_speed_label.setText(f"Suggested Speed: {suggested_speed}")
        self.Kp_Label.setText(f"Kp: {Kp}")
        self.Ki_Label.setText(f"Ki: {Ki}")
        self.current_speed_label.setText(f"Current Speed: {current_speed}")
        self.power_output_label.setText(f"Power Output: {power_output}")
        self.door_status_label.setText(f"Door Status: {'Open'if door_status else 'Closed'}")
        self.lights_status_label.setText(f"Lights Status: {'On' if lights_status else 'Off'}")
        self.temperature_label.setText(f"Internal Temperature: {internal_temperature}")
        self.hl_status_label.setText(f"Headlights Status: {'On' if headlights_status else 'Off'}")
        self.speed_limit_label.setText(f"Speed Limit: {speed_limit}")

def main():
    app = QApplication(sys.argv)

    # Create and show the main CommandCenter window
    command_center = CommandCenter()
    command_center.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
