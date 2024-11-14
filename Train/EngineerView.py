import PyQt5
import sys
from PyQt5.QtWidgets import QApplication, QCheckBox, QMainWindow, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLayout
#from backend import Backend #importing backend logic
from PyQt5.QtCore import pyqtSignal
#from Backend import Backend
from .CombinedBackend import Train

class EngineerView(QWidget):
    Kp_Ki_updated = pyqtSignal()

    def __init__(self, Train):
      super().__init__()
      self.backend = Train
      self.initUI()

    def initUI(self):
        # Layout and Widgets
        self.setWindowTitle("Engineer View")
        self.setGeometry(150, 150, 400, 350)
        layout = QVBoxLayout()

        # Input field for Kp
        self.Kp_input = QLineEdit(self)
        self.Kp_input.setPlaceholderText("Enter Kp Value")
        layout.addWidget(QLabel("Kp: "))
        layout.addWidget(self.Kp_input)

        # Input field for Ki
        self.Ki_input = QLineEdit(self)
        self.Ki_input.setPlaceholderText("Enter Ki Value")
        layout.addWidget(QLabel("Ki: "))
        layout.addWidget(self.Ki_input)

        # Button to submit command
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_inputs)
        layout.addWidget(self.submit_button)

        # Set the main layout of the window
        self.setLayout(layout)

    def submit_inputs(self):
        # Get the input text
        Kp = int(self.Kp_input.text()) if self.Kp_input.text() != "" else 0
        Ki =  int(self.Ki_input.text()) if self.Ki_input.text() != "" else 0
        print(f"testing bench")
        self.backend.set_Kp_Ki(Kp, Ki)
        #self.status_label.setText(
        #f"Speed: {self.backend.commanded_speed}\n"
        #f"Authority: {self.backend.authority}\n"
        #f"Brake Status: {'Applied' if self.backend.brake_status else 'Released'}"
        #)
        self.Kp_Ki_updated.emit()

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