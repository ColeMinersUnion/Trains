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
        self.view.ebrake_signal.connect(self.model.set_ebrake_from_driver)
        self.view.sbrake_signal.connect(self.model.toggle_sbrake)
        self.view.kp_signal.connect(self.model.set_Kp)
        self.view.ki_signal.connect(self.model.set_Ki)
        
        self.model.power_command.connect(self.view.pwr_updated)
        self.model.internal_ebrake_signal.connect(self.view.ebrake_changed)
        self.model.headlights_change.connect(self.view.headlights_status)
        self.model.lights_signal.connect(self.view.lights_status)
        self.model.left_doors_signal.connect(self.view.left_door_status)
        self.model.right_doors_signal.connect(self.view.right_door_status)
        self.model.update_current_speed_signal.connect(self.view.current_speed_updated) 
        self.model.authority_display.connect(self.view.update_authority_display)
        self.model.speed_limit.connect(self.view.curr_speed_limit)

