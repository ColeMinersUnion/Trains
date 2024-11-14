import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTabWidget, QLineEdit, QSpacerItem, QSizePolicy, QHBoxLayout, QGridLayout
from PyQt5.QtCore import QTimer, Qt, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtGui import QFont
from TrainModelClass import trainModel

class Worker(QObject):
    finished = pyqtSignal()

    def __init__(self, Train):
        super().__init__()
        self.Train = Train

    @pyqtSlot()
    def run(self):
        self.Train.speedCalculations()
        self.finished.emit()

class PassengerView(QWidget):
    def __init__(self, Train):
        super().__init__()

        self.Train = Train

        # Vertical layout for the main content
        layout = QVBoxLayout()

        top_spacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(top_spacer)

        next_station_label = QLabel("Next Station:")
        next_station_label.setAlignment(Qt.AlignCenter)
        next_station_label.setFont(QFont('Arial', 20))
        layout.addWidget(next_station_label)

        self.station_box = QLineEdit(self.Train.nextStation)
        self.station_box.setAlignment(Qt.AlignCenter)
        self.station_box.setFont(QFont('Arial', 30))
        self.station_box.setReadOnly(True)
        layout.addWidget(self.station_box)

        middle_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(middle_spacer)

        self.brake_button = QPushButton("Emergency Brake: OFF")
        self.brake_button.setFont(QFont('Arial', 20))
        self.brake_button.setStyleSheet("background-color: red; color: white; height: 50px;")
        self.brake_button.clicked.connect(self.toggle_emergency_brake)
        layout.addWidget(self.brake_button)

        bottom_spacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(bottom_spacer)

        # Horizontal layout with side spacers
        main_layout = QHBoxLayout()
        left_spacer = QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        right_spacer = QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        main_layout.addItem(left_spacer)
        main_layout.addLayout(layout)
        main_layout.addItem(right_spacer)

        self.setLayout(main_layout)

        self.update_station()
        self.update_emergency_brake_button()

    def update_station(self):
        if self.Train.signalFailure:
            return
        
        station_name = self.Train.nextStation
        self.station_box.setText(station_name)

    def toggle_emergency_brake(self):

        self.Train.eBrakeToggle()
        self.brake_button.setText("Emergency Brake: ON" if self.Train.emergencyBrake else "Emergency Brake: OFF")
        self.update_emergency_brake_button()

        main_window = self.parent()
        if isinstance(main_window, MainWindow):
            if not main_window.thread.isRunning():
                main_window.start_speed_calculation()
                self.Train.speedCalculations()

    def update_emergency_brake_button(self):
        if self.Train.brakeFailure:
            self.brake_button.setEnabled(False)
            self.brake_button.setText("Emergency Brake: N/A")
        else:
            self.brake_button.setEnabled(True)
            self.brake_button.setText("Emergency Brake: ON" if self.Train.emergencyBrake else "Emergency Brake: OFF")

class MurphyView(QWidget):
    def __init__(self, train):
        super().__init__()
        self.Train = Train

        layout = QVBoxLayout()

        # Engine failure toggle
        self.add_failure_section(layout, "Engine Failure", self.train.engineFailure, self.toggle_engine_failure)

        # Signal failure toggle
        self.add_failure_section(layout, "Signal Failure", self.train.signalFailure, self.toggle_signal_failure)

        # Brake failure toggle
        self.add_failure_section(layout, "Brake Failure", self.train.brakeFailure, self.toggle_brake_failure)

        self.setLayout(layout)

    def add_failure_section(self, layout, label_text, initial_state, toggle_function):
        label = QLabel(f"{label_text}:")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont('Arial', 20))
        layout.addWidget(label)

        status_label = QLabel("Active" if initial_state else "Inactive")
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setFont(QFont('Arial', 16))

        if initial_state:
            status_label.setStyleSheet("color: green;")
        else:
            status_label.setStyleSheet("color: red;")

        layout.addWidget(status_label)


        middle_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(middle_spacer)

        button = QPushButton(f"Toggle {label_text}")
        button.setFont(QFont('Arial', 18))
        button.clicked.connect(lambda: toggle_function(status_label))
        layout.addWidget(button)

        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(bottom_spacer)

    def toggle_engine_failure(self, status_label):
        self.Train.activateEngineFailure()
        if self.Train.engineFailure:
            status_label.setText("Active")
            status_label.setStyleSheet("color: green;")
        else:
            status_label.setText("Inactive")
            status_label.setStyleSheet("color: red;")


    def toggle_signal_failure(self, status_label):
        self.Train.activateSignalFailure()
        if self.Train.signalFailure:
            status_label.setText("Active")
            status_label.setStyleSheet("color: green;")
        else:
            status_label.setText("Inactive")
            status_label.setStyleSheet("color: red;")


    def toggle_brake_failure(self, status_label):
        self.Train.activateBrakeFailure()
        if self.Train.brakeFailure:
            status_label.setText("Active")
            status_label.setStyleSheet("color: green;")
        else:
            status_label.setText("Inactive")
            status_label.setStyleSheet("color: red;")


        main_window = self.parent()
        if isinstance(main_window, MainWindow):
            main_window.Train_tab.update_emergency_brake_button()

class MetricsTab(QWidget):
    def __init__(self, Train):
        super().__init__()
        
        self.Train = Train

        main_layout = QHBoxLayout()
        col1_layout = QVBoxLayout()
        col2_layout = QVBoxLayout()

        self.currentSpeed_label = QLabel()
        self.currentSpeed_label.setAlignment(Qt.AlignCenter)
        self.currentSpeed_label.setFont(QFont('Arial', 14))
        col1_layout.addWidget(self.currentSpeed_label)

        self.acceleration_label = QLabel()
        self.acceleration_label.setAlignment(Qt.AlignCenter)
        self.acceleration_label.setFont(QFont('Arial', 14))
        col1_layout.addWidget(self.acceleration_label)

        self.passenger_count_label = QLabel()
        self.passenger_count_label.setAlignment(Qt.AlignCenter)
        self.passenger_count_label.setFont(QFont('Arial', 14))
        col1_layout.addWidget(self.passenger_count_label)

        self.weight_label = QLabel()
        self.weight_label.setAlignment(Qt.AlignCenter)
        self.weight_label.setFont(QFont('Arial', 14))
        col1_layout.addWidget(self.weight_label)

        self.temperature_label = QLabel()
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setFont(QFont('Arial', 14))
        col2_layout.addWidget(self.temperature_label)

        self.light_status_label = QLabel()
        self.light_status_label.setAlignment(Qt.AlignCenter)
        self.light_status_label.setFont(QFont('Arial', 14))
        col2_layout.addWidget(self.light_status_label)

        self.left_door_status_label = QLabel()
        self.left_door_status_label.setAlignment(Qt.AlignCenter)
        self.left_door_status_label.setFont(QFont('Arial', 14))
        col2_layout.addWidget(self.left_door_status_label)

        self.right_door_status_label = QLabel()
        self.right_door_status_label.setAlignment(Qt.AlignCenter)
        self.right_door_status_label.setFont(QFont('Arial', 14))
        col2_layout.addWidget(self.right_door_status_label)

        self.service_brake_status_label = QLabel()
        self.service_brake_status_label.setAlignment(Qt.AlignCenter)
        self.service_brake_status_label.setFont(QFont('Arial', 14))
        col2_layout.addWidget(self.service_brake_status_label)

        main_layout.addLayout(col1_layout)
        main_layout.addLayout(col2_layout)

        self.setLayout(main_layout)

        self.update_labels()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(500) 

    def update_labels(self):
        currentSpeed = self.Train.getCurrentSpeedImperial()
        acceleration = self.Train.getAccelerationImperial()
        passenger_count = self.Train.currentCapacity
        weight = self.Train.getWeightImperial()
        temperature = self.Train.getTemp()
        light_status = "On" if self.Train.lightStatus else "Off"
        left_door_status = "Open" if self.Train.leftDoorStatus else "Closed"
        right_door_status = "Open" if self.Train.rightDoorStatus else "Closed"
        service_brake_status = "On" if self.Train.serviceBrake else "Off"

        self.currentSpeed_label.setText(f"Current Speed: {currentSpeed:.2f} mph")
        self.acceleration_label.setText(f"Acceleration: {acceleration:.2f} ft/s²")
        self.passenger_count_label.setText(f"Passenger Count: {passenger_count} passengers")
        self.weight_label.setText(f"Weight: {weight:.2f} lbs")
        self.temperature_label.setText(f"Temperature: {temperature:.2f} °F")
        self.light_status_label.setText(f"Light Status: {light_status}")
        self.left_door_status_label.setText(f"Left Door Status: {left_door_status}")
        self.right_door_status_label.setText(f"Right Door Status: {right_door_status}")
        self.service_brake_status_label.setText(f"Service Brake: {service_brake_status}")


class TestBench(QWidget):
    def __init__(self, Train, metrics_tab, Train_tab):
        super().__init__()
        self.Train = Train
        self.metrics_tab = metrics_tab
        self.Train_tab = Train_tab

        layout = QGridLayout()

        # Power Command
        power_command_label = QLabel("Power Command (Watts):")
        self.power_command_input = QLineEdit()
        self.power_command_button = QPushButton("Set Power Command")
        self.power_command_button.clicked.connect(self.set_power_command)

        # Temperature
        temperature_label = QLabel("Temperature (°F):")
        self.temperature_input = QLineEdit()
        self.temperature_button = QPushButton("Set Temperature")
        self.temperature_button.clicked.connect(self.set_temperature)

        # Authority
        authority_label = QLabel("Authority:")
        self.authority_input = QLineEdit()
        self.authority_button = QPushButton("Set Authority")
        self.authority_button.clicked.connect(self.set_authority)

        # Next Station
        next_station_label = QLabel("Next Station:")
        self.next_station_input = QLineEdit()
        self.next_station_button = QPushButton("Set Next Station")
        self.next_station_button.clicked.connect(self.set_next_station)

        # Add Passengers
        add_passengers_label = QLabel("Add Passengers:")
        self.add_passengers_input = QLineEdit()
        self.add_passengers_button = QPushButton("Add Passengers")
        self.add_passengers_button.clicked.connect(self.add_passengers)

        # Service Brake Toggle
        self.service_brake_button = QPushButton("Toggle Service Brake")
        self.service_brake_button.clicked.connect(self.toggle_service_brake)

        # Light Status
        light_toggle_button = QPushButton("Toggle Lights")
        light_toggle_button.clicked.connect(self.toggle_lights)

        # Left Door Status
        left_door_toggle_button = QPushButton("Toggle Left Doors")
        left_door_toggle_button.clicked.connect(self.toggle_left_doors)

        # Left Door Status
        right_door_toggle_button = QPushButton("Toggle Right Doors")
        right_door_toggle_button.clicked.connect(self.toggle_right_doors)

        # Layout for input fields and buttons
        layout.addWidget(power_command_label, 0, 0)
        layout.addWidget(self.power_command_input, 0, 1)
        layout.addWidget(self.power_command_button, 0, 2)

        layout.addWidget(temperature_label, 1, 0)
        layout.addWidget(self.temperature_input, 1, 1)
        layout.addWidget(self.temperature_button, 1, 2)

        layout.addWidget(authority_label, 3, 0)
        layout.addWidget(self.authority_input, 3, 1)
        layout.addWidget(self.authority_button, 3, 2)

        layout.addWidget(next_station_label, 4, 0)
        layout.addWidget(self.next_station_input, 4, 1)
        layout.addWidget(self.next_station_button, 4, 2)

        layout.addWidget(add_passengers_label, 5, 0)
        layout.addWidget(self.add_passengers_input, 5, 1)
        layout.addWidget(self.add_passengers_button, 5, 2)

        layout.addWidget(light_toggle_button, 6, 0, 1, 2)
        layout.addWidget(left_door_toggle_button, 6, 1, 1, 2)
        layout.addWidget(right_door_toggle_button, 6, 2, 1, 2)
        layout.addWidget(self.service_brake_button, 7, 0, 1, 2)

        self.setLayout(layout)

    def update_inputs(self):
        self.power_command_input.setText(f"{self.Train.getPowerCommand():.2f}")
        self.temperature_input.setText(f"{self.Train.getTemp():.2f}")
        self.authority_input.setText(f"{self.Train.getAuthority():.2f}")
        self.next_station_input.setText(self.Train.nextStation)
        self.add_passengers_input.setText(f"{self.Train.currentCapacity}")

    def set_power_command(self):
        if self.Train.signalFailure:
            return
        try:
            power_command = float(self.power_command_input.text())
            self.Train.setPowerCommand(power_command)
            self.metrics_tab.update_labels()

            main_window = self.parent()
            if isinstance(main_window, MainWindow):
                main_window.start_speed_calculation()

        except ValueError:
            print("Invalid input for Power Command")

    def set_temperature(self):
        temp = float(self.temperature_input.text())
        self.Train.setTemp(temp)
        self.metrics_tab.update_labels()

    def set_command_speed(self):
        if self.Train.signalFailure:
            return

        command_speed = float(self.command_speed_input.text())
        self.Train.setCommandSpeed(command_speed)
        self.metrics_tab.update_labels()
        print(command_speed)

    def set_authority(self):
        if self.Train.signalFailure:
            return
        
        authority = float(self.authority_input.text())
        self.Train.setAuthority(authority)
        self.metrics_tab.update_labels()
        print(authority)

    def set_next_station(self):
        if self.Train.signalFailure:
            return
        
        next_station = self.next_station_input.text()
        self.Train.setNextStation(next_station)
        self.Train_tab.update_station() 

    def add_passengers(self):
        passengers = int(self.add_passengers_input.text())
        self.Train.addPassengers(passengers)
        self.metrics_tab.update_labels()

    def toggle_lights(self):
        self.Train.lightToggle()
        self.metrics_tab.update_labels()

    def toggle_left_doors(self):
        self.Train.leftDoorToggle()
        self.metrics_tab.update_labels()

    def toggle_right_doors(self):
        self.Train.rightDoorToggle()
        self.metrics_tab.update_labels()

    def toggle_service_brake(self):
        if self.Train.brakeFailure:
            return

        self.Train.servBrakeToggle()
        self.metrics_tab.update_labels()

        main_window = self.parent()
        if isinstance(main_window, MainWindow):
            if not main_window.thread.isRunning():
                main_window.start_speed_calculation()
                self.Train.speedCalculations()

class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        self.Train = TrainModel()
        self.Train_tab = PassengerView(self.Train)
        self.failure_tab = MurphyView(self.Train)
        self.metrics_tab = MetricsTab(self.Train)
        self.test_bench = TestBench(self.Train, self.metrics_tab, self.Train_tab)

        self.addTab(self.Train_tab, "Passenger View")
        self.addTab(self.failure_tab, "Murphy View")
        self.addTab(self.metrics_tab, "Metrics")
        self.addTab(self.test_bench, "Test Bench")

        self.calculation_timer = QTimer(self)
        self.calculation_timer.timeout.connect(self.start_speed_calculation)
        self.calculation_timer.start(500)  # Every 500ms

        self.thread = QThread()
        self.worker = Worker(self.Train)
        self.worker.moveToThread(self.thread)

        self.worker.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.on_calculation_finished)

    def start_speed_calculation(self):
        if not self.thread.isRunning():
            self.thread = QThread()
            self.worker = Worker(self.Train)
            self.worker.moveToThread(self.thread)

            self.worker.finished.connect(self.thread.quit)
            self.thread.started.connect(self.worker.run)
            self.thread.finished.connect(self.on_calculation_finished)

            self.thread.start()

    def on_calculation_finished(self):
        #print("Speed calculation finished")
        self.metrics_tab.update_labels()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Train Model")
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
