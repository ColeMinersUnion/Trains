  # train_controller/view.py
from PyQt5.QtWidgets import QWidget, QSlider, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal as Signal, QTimer

class TCView(QWidget):
    setpoint_command_signal = Signal(float)
    pid_tick_signal = Signal()

    def __init__(self):
        super().__init__()

        self.label = QLabel("Setpoint Speed: 0")
        self.setpoint_slider = QSlider(Qt.Orientation.Horizontal)
        self.setpoint_slider.setRange(0, 100)  # Range from 0 to 100
        self.setpoint_slider.setValue(50)  # Default value
        self.setpoint_slider.valueChanged.connect(self.emit_setpoint_command)

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
        self.setLayout(layout)
        self.setWindowTitle("Train Controller View")

    def emit_setpoint_command(self, value):
        """ Emit power command when the slider value changes. """
        self.label.setText(f"Setpoint Speed: {value}")
        self.setpoint_command_signal.emit(value)

    def tick(self):
        """ Emit a PID tick signal. """
        self.pid_tick_signal.emit()