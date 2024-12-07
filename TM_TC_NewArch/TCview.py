  # train_controller/view.py
from PyQt6.QtWidgets import QWidget, QSlider, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QLineEdit, QGroupBox, QFormLayout, QGridLayout, QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton
from PyQt6.QtCore import Qt, pyqtSignal as Signal, QTimer, pyqtSlot as Slot

class TCView(QWidget):
    setpoint_command_signal = Signal(float)
    pid_tick_signal = Signal()
    ebrake_signal = Signal(bool)
    kp_signal = Signal(float)
    ki_signal = Signal(float)
    manual_left_doors = Signal(bool)
    manual_right_doors = Signal(bool)
    manual_lights = Signal(bool)
    manual_hl = Signal(bool)
    temperature = Signal(float)

    def __init__(self):
        super().__init__()
        self.ebrake = False
        self.acceleration = 0.0
        self.current_speed = 0.0
        self.pwr = 0.0
        self.left_doors = False
        self.right_doors = False
        self.lights = False
        self.headlights = False

        self.setStyleSheet("""
        QWidget {
            background-color: #f8f9fa;
            font-family: Arial, sans-serif;
            font-size: 14px;
            
        }
        QLabel {
            font-weight: bold;
            margin-bottom: 5px;
            color: black;
        }
        QPushButton {
            background-color: #007BFF;
            color: white;
            padding: 5px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
        QSlider::handle:horizontal {
            background: #007BFF;
            border-radius: 10px;
        }
        """)
        self.init_ui()

    def init_ui(self):
        setpoint_layout = QVBoxLayout()
        self.setpoint_label = QLabel("Setpoint Speed: 50")
        try:
            self.setpoint_slider = QSlider(Qt.Horizontal)
        except:
            self.setpoint_slider = QSlider(Qt.Orientation.Horizontal)
        self.setpoint_slider.setRange(0, 100)
        self.setpoint_slider.setValue(50)
        self.setpoint_slider.valueChanged.connect(self.emit_setpoint_command)
        self.setpoint_slider.setToolTip("Adjust the target speed (0-100)")
        
        setpoint_layout.addWidget(self.setpoint_label)
        setpoint_layout.addWidget(self.setpoint_slider)
        setpoint_group = QGroupBox("Setpoint Controls")
        setpoint_group.setLayout(setpoint_layout)

        # Emergency Brake Section
        self.ebrake_button = QPushButton("Emergency Brake: OFF")
        self.ebrake_button.clicked.connect(self.ebrake_toggle)
        self.ebrake_button.setToolTip("Toggle the emergency brake")
        ebrake_layout = QVBoxLayout()
        ebrake_layout.addWidget(self.ebrake_button)
        ebrake_group = QGroupBox("Emergency Controls")
        ebrake_group.setLayout(ebrake_layout)

        self.auth_label = QLabel("Authority: 0")

        # PID Controls Section
        pid_layout = QFormLayout()
        self.kp_input = QLineEdit()
        self.kp_input.setPlaceholderText("Enter Kp value")
        self.ki_input = QLineEdit()
        self.ki_input.setPlaceholderText("Enter Ki value")
        self.set_kp_button = QPushButton("Set Kp")
        self.set_kp_button.clicked.connect(self.emit_kp_value)
        self.set_ki_button = QPushButton("Set Ki")
        self.set_ki_button.clicked.connect(self.emit_ki_value)
        pid_layout.addRow("Kp:", self.kp_input)
        pid_layout.addRow(self.set_kp_button)
        pid_layout.addRow("Ki:", self.ki_input)
        pid_layout.addRow(self.set_ki_button)
        pid_group = QGroupBox("PID Settings")
        pid_group.setLayout(pid_layout)

        # Manual Controls Section
        manual_layout = QGridLayout()
        self.left_door_button = QPushButton("Left Doors: CLOSED")
        self.left_door_button.clicked.connect(self.toggle_left_doors)

        self.right_door_button = QPushButton("Right Doors: CLOSED")
        self.right_door_button.clicked.connect(self.toggle_right_doors)

        self.lights_button = QPushButton("Lights: OFF")
        self.lights_button.clicked.connect(self.toggle_lights)

        self.headlights_button = QPushButton("Headlights: OFF")
        self.headlights_button.clicked.connect(self.toggle_headlights)

        self.temp_input = QLineEdit()
        self.temp_input.setPlaceholderText("Enter temperature value ")
        self.set_temp_button = QPushButton("Set Temperature")
        self.set_temp_button.clicked.connect(self.emit_temp_value)

        manual_layout.addWidget(self.left_door_button, 0, 0)
        manual_layout.addWidget(self.right_door_button, 0, 1)
        manual_layout.addWidget(self.lights_button, 1, 0)
        manual_layout.addWidget(self.headlights_button, 1, 1)
        manual_layout.addWidget(self.temp_input)
        manual_layout.addWidget(self.set_temp_button)
        manual_group = QGroupBox("Manual Controls")
        manual_group.setLayout(manual_layout)

        # Status Section
        status_layout = QVBoxLayout()
        self.a_label = QLabel("Acceleration: 0.00 m/s²")
        self.current_speed_label = QLabel("Current Speed: 0.00 m/s")
        self.pwr_label = QLabel("Power: 0.00 W")
        self.auth_label = QLabel("Authority: 0")
        status_layout.addWidget(self.a_label)
        status_layout.addWidget(self.current_speed_label)
        status_layout.addWidget(self.pwr_label)
        status_layout.addWidget(self.auth_label)
        status_group = QGroupBox("Status Information")
        status_group.setLayout(status_layout)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(setpoint_group)
        main_layout.addWidget(ebrake_group)
        main_layout.addWidget(pid_group)
        main_layout.addWidget(status_group)
        main_layout.addWidget(manual_group)
        self.setLayout(main_layout)
        self.setWindowTitle("Train Controller View")
        self.resize(400, 600)

        #top_layout = QVBoxLayout()
        #top_layout.addWidget(self.label)
        #top_layout.addWidget(self.setpoint_slider)
        #top_layout.addWidget(self.ebrake_button)
        #top_layout.addWidget(self.auth_label)

        #self.kp_input = QLineEdit()
        #self.kp_input.setPlaceholderText("Enter Kp value")
        #self.ki_input = QLineEdit()
        #self.ki_input.setPlaceholderText("Enter Ki value")

        #self.set_kp_button = QPushButton("Set Kp")
        #self.set_kp_button.clicked.connect(self.emit_kp_value)

        #self.set_ki_button = QPushButton("Set Ki")
        #self.set_ki_button.clicked.connect(self.emit_ki_value)

        #self.a_label = QLabel(f"Acceleration: 0.00 m/s^2")
        #self.current_speed_label = QLabel(f"Current Speed: 0.00 m/s")
        #self.pwr_label = QLabel(f"Power: 0.00W")
        #self.hl_label = QLabel(f"Headlights: OFF")
        #self.ldoor_label = QLabel(f"Left Doors: CLOSED")
        #self.rdoor_label = QLabel(f"Right Doors: CLOSED")
        #self.lights_label = QLabel(f"Lights: OFF")

        #middle_layout = QVBoxLayout()
        #middle_layout.addWidget(QLabel("Kp:"))
        #middle_layout.addWidget(self.kp_input)
        #middle_layout.addWidget(self.set_kp_button)
        #middle_layout.addWidget(QLabel("Ki:"))
        #middle_layout.addWidget(self.ki_input)
        #middle_layout.addWidget(self.set_ki_button)
        #middle_layout.addWidget(self.current_speed_label)
        #middle_layout.addWidget(self.pwr_label)
        #middle_layout.addWidget(self.a_label)


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

        #layout = QVBoxLayout(self)
        #layout.addLayout(top_layout)
        #layout.addLayout(middle_layout)
        #self.setLayout(layout)
        #self.setWindowTitle("Train Controller View")

    def toggle_left_doors(self):
        #change value internally
        self.left_doors = not self.left_doors
        #emit signal
        self.manual_left_doors.emit(self.left_doors)
        #change label

    def toggle_right_doors(self):
        #change value internally
        self.right_doors = not self.right_doors
        #emit signal
        self.manual_right_doors.emit(self.right_doors)
        #change label
        #

    def toggle_headlights(self):
        #change value internally
        self.headlights = not self.headlights
        #emit signal
        self.manual_hl.emit(self.headlights)
        #change label
        #

    def toggle_lights(self):
        #change value internally
        self.lights = not self.lights
        #emit signal
        self.manual_lights.emit(self.lights)
        #change label
        #

    def update_lights_label(self):
        self.lights_button.setText(f"Lights: {'ON' if self.lights else 'OFF'}")

    def update_hl_label(self):
        self.headlights_button.setText(f"Headlights: {'ON' if self.headlights else 'OFF'}")
    def update_rd_label(self):
        self.right_door_button.setText(f"Right Doors: {'OPEN' if self.right_doors else 'CLOSED'}")
    def update_ld_label(self):
        self.left_door_button.setText(f"Left Doors: {'OPEN' if self.left_doors else 'CLOSED'}")

    @Slot (bool)
    def headlights_status(self, hl):
        self.headlights_button.setText(f"Headlights: {'ON' if hl else 'OFF'}")
        #change value
        self.headlights = hl
    
    @Slot (bool)
    def left_door_status(self, ldoor):
        self.left_door_button.setText(f"Left Doors: {'OPEN' if ldoor else 'CLOSE'}")
        #change value
        self.left_doors = ldoor
    
    @Slot (bool)
    def right_door_status(self, rdoor):
        self.right_door_button.setText(f"Right Doors: {'OPEN' if rdoor else 'CLOSE'}")
        #change value
        self.right_doors = rdoor

    @Slot (bool)
    def lights_status(self, lights):
        self.lights_button.setText(f"Lights: {'ON' if lights else 'OFF'}")
        #change value
        self.lights = lights

    def emit_setpoint_command(self, value):
        """ Emit power command when the slider value changes. """
        self.setpoint_label.setText(f"Setpoint Speed: {value}")
        self.setpoint_command_signal.emit(value)

    def tick(self):
        """ Emit a PID tick signal. """
        self.pid_tick_signal.emit()
    
    def ebrake_toggle(self):
        #ATTEMPT to toggle ebrake
        self.ebrake = not self.ebrake
        self.ebrake_signal.emit(self.ebrake)
        self.update_ebrake_ui()
    def emit_temp_value(self):
        self.temperature_label.setText(f"Temperature: {self.temperature}°C")
        self.temperature_signal.emit(self.temperature)
        
    def update_ebrake_ui(self):
        self.ebrake_button.setText("Emergency Brake: ON" if self.ebrake else "Emergency Brake: OFF")

    @Slot(bool)
    def ebrake_changed(self, e):
        self.ebrake = e
        self.update_ebrake_ui()

    @Slot (float)
    def acceleration_changed(self, a):
        self.a_label.setText(f"Acceleration: {a:.2f} m/s^2")

    @Slot (float)
    def current_speed_updated(self, c):
        self.current_speed_label.setText(f"Current Speed: {c:.2f} m/s")
    @Slot (float)
    def pwr_updated(self, p):
        self.pwr_label.setText(f"Power: {p:.2f}W")

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
    @Slot (float)
    def update_authority_display(self, auth):
        self.auth_label.setText(f"Authority value: {auth}")
