# train_controller/model.py
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot
T = 0.125  #Period of control loop in seconds
P_MAX = 120000  #Maximum power output
class TCmodel(QObject):
    power_command = Signal(float)  # Signal to send power command

    def __init__(self):
        super().__init__()
        self.uk = 0
        self.uk_1 = 0
        self.ek = 0
        self.ek_1 = 0
        self.kp = 20
        self.ki = 500
        self.p = 0
        self.setpoint = 0
        self.velocity = 0
    
    @Slot(float)
    def set_setpoint(self, setpoint: float):
        """ Set the setpoint speed. """
        self.setpoint = setpoint
    @Slot(float)
    def set_velocity(self, velocity: float):
        """ Set the current velocity. """
        self.velocity = velocity
        
    @Slot()
    def pid_tick(self):
        """ Perform a PID control loop iteration. """
        self.control_law(self.setpoint, self.velocity)
        self.power_command.emit(self.p)

    def control_law(self, setpoint: float, velocity: float):
        """ Calculate power command based on control law. """
        self.ek = setpoint - velocity
        if self.p < P_MAX:
            self.uk = self.uk_1 + (T/2)*(self.ek + self.ek_1)
        else:
            self.uk = self.uk_1

        self.uk_1 = self.uk
        self.ek_1 = self.ek

        self.p = self.kp*self.ek + self.ki * self.uk
        

