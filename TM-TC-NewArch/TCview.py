  # train_controller/view.py
from PyQt5.QtWidgets import QWidget, QSlider, QVBoxLayout, QLabel, QButtonGroup, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal as Signal, QTimer, pyqtSlot as Slot

class TCView(QWidget):
    setpoint_command_signal = Signal(float)
    pid_tick_signal = Signal()
    ebrake_signal = Signal(bool)

    def __init__(self):
        super().__init__()
        self.ebrake = False
        self.setStyleSheet("""
        QWidget {
            background-color: #f0f0f0;  /* Light background color for the entire widget */
            font-family: Arial, sans-serif;  /* Use a clean font */
            font-size: 14px;  /* Standard font size */
            color: #333;  /* Dark text color for readability */
        }

        QLabel {
            font-weight: bold;  /* Bold labels for emphasis */
            margin-bottom: 10px;  /* Space between label and slider */
        }

        QSlider {
            background: #ddd;  /* Background for the slider */
            border-radius: 5px;  /* Rounded corners */
        }

        QSlider::groove:horizontal {
            background: #aaa;  /* Groove background color */
            height: 10px;  /* Height of the groove */
            border-radius: 5px;  /* Rounded corners */
        }

        QSlider::handle:horizontal {
            background: #007BFF;  /* Handle color */
            border: 2px solid #0056b3;  /* Handle border color */
            width: 20px;  /* Width of the handle */
            margin: -5px 0;  /* Center the handle */
            border-radius: 10px;  /* Rounded handle */
        }

        QSlider::handle:horizontal:hover {
            background: #0056b3;  /* Darker handle color on hover */
        }

        QSlider::sub-page:horizontal {
            background: #007BFF;  /* Color of the slider's filled portion */
            border-radius: 5px;  /* Rounded corners */
        }

        QVBoxLayout {
            margin: 20px;  /* Margin around the layout */
        }
        """)

        self.label = QLabel("Setpoint Speed: 0")
        self.setpoint_slider = QSlider(Qt.Orientation.Horizontal)
        self.setpoint_slider.setRange(0, 100)  # Range from 0 to 100
        self.setpoint_slider.setValue(50)  # Default value
        self.setpoint_slider.valueChanged.connect(self.emit_setpoint_command)

        self.ebrake_button = QPushButton("Emergency Brake: OFF")
        self.ebrake_button.clicked.connect(self.ebrake_toggle)
        # Create a QTimer instance
        self.timer = QTimer(self)

        # Set the timer interval to 125 ms
        self.timer.setInterval(125)

        # Connect the timer's timeout signal to the function
        self.timer.timeout.connect(self.tick)

        # Start the timer
        self.timer.start()

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.setpoint_slider)
        layout.addWidget(self.ebrake_button)
        self.setLayout(layout)
        self.setWindowTitle("Train Controller View")

    def emit_setpoint_command(self, value):
        """ Emit power command when the slider value changes. """
        self.label.setText(f"Setpoint Speed: {value}")
        self.setpoint_command_signal.emit(value)

    def tick(self):
        """ Emit a PID tick signal. """
        self.pid_tick_signal.emit()
    def ebrake_toggle(self):
        """ Toggle the emergency brake. """
        self.ebrake = not self.ebrake
        self.ebrake_signal.emit(self.ebrake)
        #update ui
        self.ebrake_button.setText("Emergency Brake: ON" if self.ebrake else "Emergency Brake: OFF")
    @Slot(bool)
    def ebrake_changed(self, e):
        self.ebrake = e
        self.ebrake_button.setText("Emergency Brake: ON" if self.ebrake else "Emergency Brake: OFF")
