  # train_controller/view.py
from PyQt6.QtWidgets import QWidget, QSlider, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal as Signal, QTimer, pyqtSlot as Slot

class TCView(QWidget):
    setpoint_command_signal = Signal(float)
    pid_tick_signal = Signal()
    ebrake_signal = Signal(bool)
    kp_signal = Signal(float)
    ki_signal = Signal(float)

    def __init__(self):
        super().__init__()
        self.ebrake = False
        self.acceleration = 0.0
        self.current_speed = 0.0
        self.pwr = 0.0

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

        self.auth_label = QLabel("Authority: ")

        top_layout = QVBoxLayout()
        top_layout.addWidget(self.label)
        top_layout.addWidget(self.setpoint_slider)
        top_layout.addWidget(self.ebrake_button)
        top_layout.addWidget(self.auth_label)

        self.kp_input = QLineEdit()
        self.kp_input.setPlaceholderText("Enter Kp value")
        self.ki_input = QLineEdit()
        self.ki_input.setPlaceholderText("Enter Ki value")

        self.set_kp_button = QPushButton("Set Kp")
        self.set_kp_button.clicked.connect(self.emit_kp_value)

        self.set_ki_button = QPushButton("Set Ki")
        self.set_ki_button.clicked.connect(self.emit_ki_value)

        self.a_label = QLabel(f"Acceleration: 0.00 m/s^2")
        self.current_speed_label = QLabel(f"Current Speed: 0.00 m/s")
        self.pwr_label = QLabel(f"Power: 0.00W")

        middle_layout = QVBoxLayout()
        middle_layout.addWidget(self.a_label)

        middle_layout.addWidget(QLabel("Kp:"))
        middle_layout.addWidget(self.kp_input)
        middle_layout.addWidget(self.set_kp_button)
        middle_layout.addWidget(QLabel("Ki:"))
        middle_layout.addWidget(self.ki_input)
        middle_layout.addWidget(self.set_ki_button)
        middle_layout.addWidget(self.current_speed_label)
        middle_layout.addWidget(self.pwr_label)
        middle_layout.addWidget(self.a_label)


        #self.tick_button = QPushButton("Tick")
        #self.tick_button.clicked.connect(self.tick)
        # Create a QTimer instance
        self.timer = QTimer(self)

        # Set the timer interval to 125 ms
        self.timer.setInterval(125)

        # Connect the timer's timeout signal to the function
        self.timer.timeout.connect(self.tick)

        # Start the timer
        self.timer.start()

        layout = QVBoxLayout(self)
        layout.addLayout(top_layout)
        layout.addLayout(middle_layout)
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

    @Slot (str)
    def full_auth(self, auth):
        self.auth_label = QLabel(f"Authority String: {auth}")
    @Slot(bool)
    def ebrake_changed(self, e):
        self.ebrake = e
        self.ebrake_button.setText("Emergency Brake: ON" if self.ebrake else "Emergency Brake: OFF")

    @Slot (float)
    def acceleration_changed(self, a):
        self.a_label = QLabel(f"Acceleration: {a} m/s^2")

    @Slot (float)
    def current_speed_updated(self, c):
        self.current_speed_label = QLabel(f"Current Speed: {c} m/s")   
     
    @Slot (float)
    def pwr_updated(self, p):
        self.pwr_label = QLabel(f"Power: {p}W")


    def emit_kp_value(self):
        """ Emit Kp value signal. """
        try:
            kp_value = float(self.kp_input.text())
            self.kp_signal.emit(kp_value)
        except ValueError:
            pass  # Handle invalid input if necessary

    def emit_ki_value(self):
        """ Emit Ki value signal. """
        try:
            ki_value = float(self.ki_input.text())
            self.ki_signal.emit(ki_value)
        except ValueError: 
            pass  # Handle invalid input if necessary
