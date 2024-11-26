# train_controller/controller.py
from PyQt6.QtCore import QObject

class TCcontroller (QObject):
    def __init__(self, model, view, authority):
        super().__init__()
        self.model = model
        self.view = view
        self.model.set_full_authority(authority)

        # Connect the power command signal from the view to the model's power command
        self.view.setpoint_command_signal.connect(self.model.set_commanded_speed)  
        self.view.pid_tick_signal.connect(self.model.pid_tick)
        self.view.ebrake_signal.connect(self.model.set_ebrake)
        self.view.kp_signal.connect(self.model.set_Kp)
        self.view.ki_signal.connect(self.model.set_Ki)
        
        self.model.power_command.connect(self.view.pwr_updated)
        self.model.update_auth.connect(self.view.full_auth)
