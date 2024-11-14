# CommandCenter.py
#from PyQt5 import uic
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont
from Testbench import TestbenchUI
from Backend import Backend
from EngineerView import EngineerView
from LightsAndDoorsUI  import LightsAndDoorsUI


class CommandCenter(QWidget):
    driver_commands_updated = pyqtSignal()
    def __init__(self):
        super().__init__()
        #uic.loadUi('Train Controller\Backend\cc.ui', self)

        self.backend = Backend()
        self.testbench_ui = TestbenchUI(self.backend)
        self.testbench_ui.inputs_updated.connect(self.update_values)
        self.engineer_view = EngineerView(self.backend)
        self.engineer_view.Kp_Ki_updated.connect(self.update_values)
        self.lights_and_doors_ui = LightsAndDoorsUI(self.backend)
        self.lights_and_doors_ui.lds_updated.connect(self.update_values)
        #self.lights_and_doors_ui = LightsAndDoorsUI(self.backend)
        #self.lights_and_doors_ui.inputs_updated.connect(self.update_values)
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_values)
        self.timer.start(1000)  # 1000ms = 1s
        #self.authority_timer = QTimer()
        #self.authority_timer.timeout.connect(self.update_authority)
        #self.authority_timer.start(1000)  # 1000ms = 1s
        self.brake_applied = False


    def initUI(self):
        self.setWindowTitle("Command Center")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        font = QFont()
        font.setPointSize(12)

        self.setStyleSheet("""
        QWidget {
            background-color: #ecf0f1; 
            font-family: Arial;
            color: black;  /* Text color */
        }
        QPushButton {
            background-color: #3498db;  /* Button color */
            color: white;
            border: none;
            padding: 12px 20px;
            font-size: 14px;
            border-radius: 5px;
            transition: background-color 0.3s;
            font-weight: bold; 

        }
        QPushButton:hover {
            background-color: #2980b9;  
        }
        QLabel {
            font-size: 16px;
            font-weight: bold;
            color: black;  /*  text color */
            border: 1px solid #34495e;  
            padding: 10px;
            border-radius: 5px;
        }
        QHBoxLayout, QVBoxLayout {
            margin: 10px;  
        }
        #emergency_brake, #service_brake {
            min-width: 150px;
            min-height: 50px;
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
        self.engineer_button.setFixedHeight(80)
        self.engineer_button.setFont(font)
        self.engineer_button.clicked.connect(self.open_engineer_view)
        layout.addWidget(self.engineer_button)

        #Button  to open Lights and Doors Module Brake

        self.LDS_button = QPushButton("Open Driver UI", self)
        self.engineer_button.setFixedHeight(120)
        self.engineer_button.setFont(font)
        self.LDS_button.clicked.connect(self.open_lds)
        layout.addWidget(self.LDS_button)

        # Button to open LDS
        # self.lds_button = QPushButton("Open Lights and Doors Override", self)
        # self.lds_button.clicked.connect(self.open_lds)
        # layout.addWidget(self.lds_button)

        # Labels to display speed, authority, and brake status
        self.speed_label = QLabel(f"Commanded Speed: {self.backend.commanded_speed}") #change so it displays in mph
        self.authority_label = QLabel(f"Authority: {self.backend.curr_authority.split(';')[0]}")
        self.brake_status_label = QLabel(f"Brake Status: {self.backend.brake_status}")
        self.currentSpeed_label = QLabel(f"Current Speed: {self.backend.currentSpeed}")
        self.power_output_label = QLabel(f"Power Output: {self.backend.power_output}")
        self.door_status_label = QLabel(f"Door Status: {self.backend.door_status}")
        self.lights_status_label = QLabel(f"Lights Status: {self.backend.lights_status}")
        self.temperature_label = QLabel(f"Internal Temperature: {self.backend.internal_temperature}")
        self.hl_status_label = QLabel(f"Headlights Status: {self.backend.headlights_status}")
        self.speed_limit_label = QLabel(f"Speed Limit: {self.backend.speed_limit}")
        self.Kp_Label = QLabel(f"Kp: {self.backend.Kp}")
        self.Ki_Label = QLabel(f"Ki: {self.backend.Ki}")

        for label in [self.speed_label, self.authority_label, self.brake_status_label, self.Kp_Label, self.Ki_Label, self.power_output_label, self.door_status_label, self.lights_status_label, self.temperature_label, self.hl_status_label, self.speed_limit_label]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)

        self.setLayout(layout)

    def open_testbench(self):
        # Open the Testbench UI
        self.testbench_ui.show()
        

    def  open_engineer_view(self):
        # Open the Engineer View UI
        self.engineer_view.show()

    def open_lds(self):
        # Open the LDS UI
        self.lds_ui = LightsAndDoorsUI(self.backend)
        self.lights_and_doors_ui.show()
        

    def update_values(self):
        #commanded_speed, authority, brake_status, suggested_speed, currentSpeed, power_output, door_status, lights_status, internal_temperature, headlights_status, speed_limit = self.backend.get_testbench_status()
        Kp, Ki =  self.backend.get_Kp_Ki()
        commanded_speed = self.backend.get_commanded_speed()
        authority = self.backend.curr_authority.split(';')[0]
        brake_status = self.backend.get_brake()
        currentSpeed = self.backend.get_currentSpeed()
        self.backend.set_power_output()
        power_output = self.backend.get_power_output()
        door_status = self.backend.get_doors()
        lights_status = self.backend.get_lights()
        internal_temperature = self.backend.get_internal_temp()
        headlights_status = self.backend.get_hl()
        speed_limit = self.backend.get_speed_limit()
        #TODO figure out how to put LightsAndDoorsUI here

        # Get the latest values from the backend and update the labels
        #result = Backend.get_testbench_status()
        self.speed_label.setText(f"Speed: {commanded_speed}")
        self.authority_label.setText(f"Authority: {authority}")
        self.brake_status_label.setText(f"Brake Status: {'ON' if brake_status else 'OFF'}")
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
    import sys
    app = QApplication(sys.argv)

    # Create and show the main CommandCenter window
    command_center = CommandCenter()
    command_center.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()