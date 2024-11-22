# train_controller/controller.py
from PyQt5.QtCore import QObject

class TCcontroller (QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        # Connect the power command signal from the view to the model's power command
        self.view.setpoint_command_signal.connect(self.model.set_setpoint)  
        self.view.pid_tick_signal.connect(self.model.pid_tick)
