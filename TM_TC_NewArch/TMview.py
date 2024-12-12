# train_model/view.py
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, QSlider, QButtonGroup,
                             QLineEdit, QGroupBox, QFormLayout, QGridLayout, QComboBox, QSpinBox,
                             QDoubleSpinBox, QCheckBox, QRadioButton, QHBoxLayout)
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtCore import pyqtSlot as Slot
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette, QPixmap
import os

class TrainModelView(QWidget):
    eBrake_toggle = Signal()
    eFailure_toggle = Signal()
    bFailure_toggle = Signal()
    sFailure_toggle = Signal()

    def __init__(self, ad_file_path: str = None):
        super().__init__()

        # Set global styling
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #007BFF;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
            }
        """)

        # Get the current script's directory
        current_directory = os.path.dirname(os.path.realpath(__file__))

        # Define the relative path to the 'images' folder
        ad_file_path = os.path.join(current_directory, 'images', 'dunkin_ad.jpg')
        self.ad_file_path = ad_file_path

        # Create labels with improved fonts
        self.v_label = QLabel("Train Velocity: 0.0 mph")
        self.a_label = QLabel("Train Acceleration: 0.0 m/s^2")
        self.length_label = QLabel("Train length: 105.6 ft")
        self.width_label = QLabel("Train width: 8.7 ft")
        self.height_label = QLabel("Train height: 11.2 ft")
        self.passengers_label = QLabel("Passengers/Crew: 2 people")
        self.trainMass_label = QLabel("Current Mass: 0 lbs")
        self.temperature_label = QLabel("Cabin Temperature: 65.0 °F")
        self.intLight_label = QLabel("Interior Lights: OFF")
        self.extLight_label = QLabel("Headlights: OFF")
        self.left_door_label = QLabel("Left Doors: Closed")
        self.right_door_label = QLabel("Right Doors: Closed")
        self.service_brake_label = QLabel("Service Brake: OFF")
        self.station_label = QLabel("Current Station: ")

        # Create buttons with consistent style
        self.emergencyBrakeButton = QPushButton("Emergency Brake: OFF")
        self.emergencyBrakeButton.clicked.connect(self.update_emergency_brake_status)

        self.engineFailureButton = QPushButton("Engine Failure: OFF")
        self.engineFailureButton.clicked.connect(self.update_engine_failure_status)

        self.signalFailureButton = QPushButton("Signal Failure: OFF")
        self.signalFailureButton.clicked.connect(self.update_signal_failure_status)

        self.brakeFailureButton = QPushButton("Brake Failure: OFF")
        self.brakeFailureButton.clicked.connect(self.update_brake_failure_status)

        # Main layout
        main_layout = QHBoxLayout(self)

        sections_layout = QVBoxLayout()

        # Section 1: Metrics View
        metrics_group = QGroupBox("Train Metrics")
        metrics_group.setMinimumWidth(400)
        metrics_layout = QVBoxLayout()
        metrics_labels = [self.v_label, self.a_label, self.length_label, self.width_label,
                          self.height_label, self.passengers_label, self.trainMass_label,
                          self.temperature_label, self.intLight_label, self.extLight_label,
                          self.left_door_label, self.right_door_label, self.service_brake_label]
        for label in metrics_labels:
            metrics_layout.addWidget(label)
        metrics_group.setLayout(metrics_layout)

        # Section 2: Passenger View
        passenger_group = QGroupBox("Passenger Controls")
        passenger_group.setMinimumWidth(400)
        passenger_layout = QVBoxLayout()
        passenger_layout.addWidget(self.station_label)
        passenger_layout.addWidget(self.emergencyBrakeButton)
        passenger_group.setLayout(passenger_layout)

        # Section 3: Murphy's View
        murphy_group = QGroupBox("System Failures")
        murphy_group.setMinimumWidth(400)
        murphy_layout = QVBoxLayout()
        murphy_layout.addWidget(self.engineFailureButton)
        murphy_layout.addWidget(self.signalFailureButton)
        murphy_layout.addWidget(self.brakeFailureButton)
        murphy_group.setLayout(murphy_layout)

        ad_group = QGroupBox("Advertisement")
        ad_layout = QVBoxLayout()

        self.ad_label = QLabel()
        self.ad_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the ad content
        ad_layout.addWidget(self.ad_label)
        ad_group.setLayout(ad_layout)

        # Check and load the advertisement if the path is provided
        if self.ad_file_path:
            self.update_advertisement(self.ad_file_path)

        # Add sections to the main layout
        sections_layout.addWidget(metrics_group)
        sections_layout.addWidget(passenger_group)
        sections_layout.addWidget(murphy_group)

        # Add the sections layout to the left of the main layout
        main_layout.addLayout(sections_layout)

        # Add the ad section to the right of the main layout
        main_layout.addWidget(ad_group)

        # Set the layout and window title
        self.setLayout(main_layout)
        self.setWindowTitle("Train Model View")

    def update_ebrake_ui(self, eBrake_status):
        if eBrake_status:
            self.emergencyBrakeButton.setStyleSheet("background-color: red; color: white; border: none; padding: 10px; border-radius: 5px;")
        else:
            self.emergencyBrakeButton.setStyleSheet("background-color: lightcoral; color: black; border: none; padding: 10px; border-radius: 5px;")

    def set_button_style(self, button, is_on):
        if is_on:
            button.setStyleSheet("background-color: red; color: white; border: none; padding: 10px; border-radius: 5px;")
        else:
            button.setStyleSheet("background-color: #007BFF; color: white; border: none; padding: 10px; border-radius: 5px;")


    def update_velocity(self, velocity: float):
        """ Update the velocity display. """
        velocity = 2.23694 * velocity
        self.v_label.setText(f"Train Velocity: {velocity:.2f} mph")

    def update_acceleration(self, acceleration: float):
        """ Update the acceleration display """
        acceleration = 2.23694 * acceleration
        self.a_label.setText(f"Train Acceleration: {acceleration:.2f} mi/hr^2")

    def update_passenger_label(self, passengers: int):
        """" Upadate display of passengers on board """
        self.passengers_label.setText(f"Passengers: {passengers} people")

    def update_trainMass_label(self, totalMass: float):
        """ Update display of the current mass of the train """
        self.trainMass_label.setText(f"Current Mass: {totalMass:.2f} kg")

    def update_temperature(self, temperature: float):
        """ Update the temperature label """
        self.temperature_label.setText(f"Cabin Temperature: {temperature:.1f} °F")

    def update_interior_light_status(self, intLight_status: bool):
        """ Update the status of the cabin (interior) lights """
        status = "ON" if intLight_status else "OFF"
        self.intLight_label.setText(f"Interior Lights: {status}")

    def update_exterior_light_status(self, extLight_status: bool):
        """ Update the status of the head lights """
        status = "ON" if extLight_status else "OFF"
        self.extLight_label.setText(f"Headlights: {status}")

    def update_left_door_status(self, leftDoor_status: bool):
        """ Update the status of the left doors """
        status = "Open" if leftDoor_status else "Closed"
        self.left_door_label.setText(f"Left Doors: {status}")

    def update_right_door_status(self, rightDoor_status: bool):
        """ Update the status of the right doors """
        status = "Open" if rightDoor_status else "Closed"
        self.right_door_label.setText(f"Right Doors: {status}")

    def update_service_brake_status(self, servBrake_status: bool):
        """ Update the status of the service brake """
        status = "ON" if servBrake_status else "OFF"
        self.service_brake_label.setText(f"Service Brake: {status}")

    def update_station_name(self, station_name: str):
        """ Update the name of the station being arrived at """
        self.station_label.setText(f"Current Station: {station_name}")

    @Slot()
    def update_emergency_brake_status(self):
        """ Update the emergency brake button """
        self.eBrake_toggle.emit()

    @Slot(bool)
    def update_eBrake_label(self, eBrake_status: bool):
        self.emergencyBrakeButton.setText("Emergency Brake: ON" if eBrake_status else "Emergency Brake: OFF")
        self.update_ebrake_ui(eBrake_status)

    @Slot()
    def update_engine_failure_status(self):
        """ Update the failure status """
        self.eFailure_toggle.emit()

    @Slot()
    def update_signal_failure_status(self):
        """ Update the failure status """
        self.sFailure_toggle.emit()
    
    @Slot()
    def update_brake_failure_status(self):
        """ Update the failure status """
        self.bFailure_toggle.emit()

    @Slot(bool)
    def update_eFailure_label(self, input: bool):
        """ Update button text """
        self.engineFailureButton.setText("Engine Failure: ON" if input else "Engine Failure: OFF")
        self.set_button_style(input)

    @Slot(bool)
    def update_sFailure_label(self, input: bool):
        """ Update button text """
        self.signalFailureButton.setText("Signal Failure: ON" if input else "Signal Failure: OFF")
        self.set_button_style(self.signalFailureButton, input)

    @Slot(bool)
    def update_bFailure_label(self, input: bool):
        """ Update button text """
        self.brakeFailureButton.setText("Brake Failure: ON" if input else "Brake Failure: OFF")
        self.set_button_style(self.brakeFailureButton, input)

    def update_advertisement(self, ad_file_path: str):
        """Load and display advertisement from a file path."""
        self.ad_file_path = ad_file_path
        pixmap = QPixmap(ad_file_path)
        if not pixmap.isNull():
            self.ad_label.setPixmap(pixmap.scaled(600, 400, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.ad_label.setText("Advertisement content not found!")
            self.ad_label.setStyleSheet("font-size: 14px; color: black;")