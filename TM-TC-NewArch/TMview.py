# train_model/view.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class TrainModelView(QWidget):
    def __init__(self):
        super().__init__()

        # Create labels
        self.v_label = QLabel("Train Velocity: 0.0 m/s")
        self.a_label = QLabel("Train Acceleration: 0.0 m/s^2")
        self.passengers_label = QLabel("Passengers: 0 people")
        self.trainMass_label = QLabel("Current Mass: 0 lbs")
        self.temperature_label = QLabel("Cabin Temperature: 65.0 °F")
        self.intLight_label = QLabel("Interior Lights: OFF")
        self.extLight_label = QLabel("Headlights: OFF")
        self.left_door_label = QLabel("Left Doors: Closed")
        self.right_door_label = QLabel("Right Doors: Closed")
        self.service_brake_label = QLabel("Service Brake: OFF")

        # Create a single layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.v_label)         # Add velocity label
        layout.addWidget(self.a_label)        # Add acceleration label
        layout.addWidget(self.passengers_label) # Add passenger label
        layout.addWidget(self.trainMass_label) # Add mass of train label
        layout.addWidget(self.temperature_label) # Add label for temperature
        layout.addWidget(self.intLight_label) # Add label for interior lights
        layout.addWidget(self.extLight_label) # Add exterior light status label
        layout.addWidget(self.left_door_label)
        layout.addWidget(self.right_door_label)
        layout.addWidget(self.service_brake_label)

        # Set the layout and window title
        self.setLayout(layout)
        self.setWindowTitle("Train Model View")

    def update_velocity(self, velocity: float):
        """ Update the velocity display. """
        self.v_label.setText(f"Train Velocity: {velocity:.2f} m/s")

    def update_acceleration(self, acceleration: float):
        """ Update the acceleration display """
        self.a_label.setText(f"Train Acceleration: {acceleration:.2f} m/s^2")

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