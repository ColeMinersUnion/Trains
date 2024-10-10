import PyQt5
import sys
from PyQt5.QtWidgets import QApplication, QCheckBox, QMainWindow, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLayout
#from backend import Backend #importing backend logic
from PyQt5.QtCore import pyqtSignal
from backend import Backend

class TestbenchUI(QWidget):
    inputs_updated = pyqtSignal()

    def __init__(self, backend):
      super().__init__()
      self.backend = backend
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

        # Checkbox for Brake Status
        self.brake_checkbox = QCheckBox("Brake Applied", self)
        layout.addWidget(QLabel("Brake Status:"))
        layout.addWidget(self.brake_checkbox)

        #input field for suggested speed
        self.suggested_speed_input = QLineEdit(self)
        self.suggested_speed_input.setPlaceholderText("Enter Suggested Speed")
        layout.addWidget(QLabel("Suggested Speed:"))
        layout.addWidget(self.suggested_speed_input)

        #input fielf for current speed
        self.current_speed_input = QLineEdit(self)
        self.current_speed_input.setPlaceholderText("Enter Current Speed")
        layout.addWidget(QLabel("Current Speed:"))
        layout.addWidget(self.current_speed_input)

        #input field for current power output
        self.current_power_input = QLineEdit(self)
        self.current_power_input.setPlaceholderText("Enter Current Power Output")
        layout.addWidget(QLabel("Current Power Output:"))
        layout.addWidget(self.current_power_input)

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
        authority = int(self.authority_input.text()) if self.authority_input.text() != "" else 0
        brake_status = self.brake_checkbox.isChecked()
        suggested_speed = int(self.suggested_speed_input.text()) if self.suggested_speed_input.text() != "" else 0
        current_speed = int(self.current_speed_input.text()) if self.current_speed_input.text() != "" else 0
        power_output = int(self.current_power_input.text()) if self.current_power_input.text() != "" else 0
        door_status = self.door_checkbox.isChecked()
        lights_status = self.light_checkbox.isChecked()
        internal_temperature = int(self.internal_temp_input.text()) if self.internal_temp_input.text() != "" else 0
        headlights_status = self.hl_checkbox.isChecked()

        self.backend.update_testbench_status(commanded_speed, authority, brake_status, suggested_speed, current_speed, power_output, door_status, lights_status, internal_temperature, headlights_status)
        #self.status_label.setText(
        #f"Speed: {self.backend.commanded_speed}\n"
        #f"Authority: {self.backend.authority}\n"
        #f"Brake Status: {'Applied' if self.backend.brake_status else 'Released'}"
        #)
        self.inputs_updated.emit()

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