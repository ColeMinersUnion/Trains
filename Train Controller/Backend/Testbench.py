import PyQt5
import sys
from PyQt5.QtWidgets import QApplication, QCheckBox, QMainWindow, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLayout
from PyQt5.QtCore import pyqtSignal, QTimer
#from Backend import Backend
from test import Train

class TestbenchUI(QWidget):
    inputs_updated = pyqtSignal()

    def __init__(self, Train):
      super().__init__()
      self.backend = Train
      self.initUI()

    def initUI(self):
        # Layout and Widgets
        self.setWindowTitle("Testbench")
        self.setGeometry(150, 150, 400, 350)
        layout = QVBoxLayout()

        # Input field for entering commands
        self.commanded_speed_input = QLineEdit(self)
        self.commanded_speed_input.setPlaceholderText("Enter Speed in kmph")
        layout.addWidget(QLabel("Commanded Speed:"))
        layout.addWidget(self.commanded_speed_input)

        # Input field for Authority
        self.authority_input = QLineEdit(self)
        self.authority_input.setPlaceholderText("Enter Authority")
        layout.addWidget(QLabel("Authority:"))
        layout.addWidget(self.authority_input)

        #change block status
        self.toggle_change_blocks_button = QPushButton("Toggle Change Blocks", self)
        self.toggle_change_blocks_button.clicked.connect(self.toggle_change_blocks)
        layout.addWidget(self.toggle_change_blocks_button)


        # Checkbox for Brake Status
        self.brake_checkbox = QCheckBox("Brake Applied", self)
        layout.addWidget(QLabel("Brake Status:"))
        layout.addWidget(self.brake_checkbox)

        #input fielf for current speed
        self.currentSpeed_input = QLineEdit(self)
        self.currentSpeed_input.setPlaceholderText("Enter Current Speed")
        layout.addWidget(QLabel("Current Speed:"))
        layout.addWidget(self.currentSpeed_input)

        #input field for door status
        self.door_checkbox = QCheckBox("Door Open", self)
        layout.addWidget(QLabel("Door Status: "))
        layout.addWidget(self.door_checkbox)

        #input field for lights status
        self.light_checkbox = QCheckBox("Lights On", self)
        layout.addWidget(QLabel("Lights Status: "))
        layout.addWidget(self.light_checkbox)

        #input field for internal temp
        self.internal_temp_input = QLineEdit(self)
        self.internal_temp_input.setPlaceholderText("Enter Internal Temp")
        layout.addWidget(QLabel("Internal Temp:"))
        layout.addWidget(self.internal_temp_input)

        #input field for headlights status
        self.hl_checkbox = QCheckBox("Headlights On", self)
        layout.addWidget(QLabel("Headlights Status: "))
        layout.addWidget(self.hl_checkbox)

        #input for speed limit
        self.speed_limit_input = QLineEdit(self)
        self.speed_limit_input.setPlaceholderText("Enter Speed Limit")
        layout.addWidget(QLabel("Speed Limit:"))
        layout.addWidget(self.speed_limit_input)

        #Beacon Data Input spot
        self.beacon_input = QLineEdit(self)
        self.beacon_input.setPlaceholderText("Enter Beacon")
        layout.addWidget(QLabel("Beacon:"))
        layout.addWidget(self.beacon_input)

        # Button to submit command
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_inputs)
        layout.addWidget(self.submit_button)

        # Output area to show results from the backend
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        layout.addWidget(QLabel("Testbench Output:"))
        layout.addWidget(self.output_area)

        # Set the main layout of the window
        self.setLayout(layout)

    def submit_inputs(self):
        # Get the input text
        commanded_speed = int(self.commanded_speed_input.text()) if self.commanded_speed_input.text() != "" else 0
        full_authority = self.authority_input.text()
        self.backend.add_to_authority(full_authority, self.backend.full_authority, self.backend.curr_authority)
        #if authority value is zero then dont send it?
        #if full  auth already exists as a value (like isnt empty) then do append, otherwise set original or just have one function 
        brake_status = (self.backend.currentSpeed > self.backend.speed_limit) or self.brake_checkbox.isChecked()
        currentSpeed = int(self.currentSpeed_input.text()) if self.currentSpeed_input.text() != "" else 0
        door_status = self.door_checkbox.isChecked()
        lights_status = self.light_checkbox.isChecked()
        internal_temperature = int(self.internal_temp_input.text()) if self.internal_temp_input.text() != "" else 0
        headlights_status = self.hl_checkbox.isChecked()
        speed_limit = int(self.speed_limit_input.text()) if self.speed_limit_input.text() != "" else 0
        beacon = self.beacon_input.text()

        self.backend.update_testbench_status(commanded_speed, full_authority, brake_status, currentSpeed, door_status, lights_status, internal_temperature, headlights_status, speed_limit, beacon)
        #self.status_label.setText(
        #f"Speed: {self.backend.commanded_speed}\n"
        #f"Authority: {self.backend.authority}\n"
        #f"Brake Status: {'Applied' if self.backend.brake_status else 'Released'}"
        #)
        self.inputs_updated.emit()

    def toggle_change_blocks(self):
        self.backend.change_blocks = not self.backend.change_blocks
        print("block switch")
        self.backend.next_authority(self.backend.curr_authority, self.backend.change_blocks, self.backend.prev_block)



"""""
def main():
   # Create the application instance
   app = QApplication(sys.argv)

   testbench = Testbench()
   frontend = TestbenchUI(testbench)
   frontend.show()
   # Create the main window
   #window = QMainWindow()
   #window.setWindowTitle("Simple PyQt Example")
   #window.setGeometry(100, 100, 400, 200)

   # Create a label widget
   #label = QLabel("Hello, PyQt!", window)
   #label.move(150, 80)

   # Show the window
   #window.show()

   # Execute the application
   sys.exit(app.exec())

if __name__ == "__main__":
   main()
   """