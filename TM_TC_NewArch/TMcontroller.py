# train_model/controller.py
from PyQt6.QtCore import QObject

class TrainModelController(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        # Connect view inputs to model
        self.view.eBrake_toggle.connect(self.model.toggleEmergencyBrake)

        # Connect the model's signal to the view's update methods
        self.model.velocity_updated.connect(self.view.update_velocity)
        self.model.acceleration_updated.connect(self.view.update_acceleration)
        self.model.passengerCount_updated.connect(self.view.update_passenger_label)
        self.model.total_mass_updated.connect(self.view.update_trainMass_label)
        self.model.temperature_updated.connect(self.view.update_temperature)
        self.model.intLights_updated.connect(self.view.update_interior_light_status)
        self.model.extLights_updated.connect(self.view.update_exterior_light_status)
        self.model.left_door_updated.connect(self.view.update_left_door_status)
        self.model.right_door_updated.connect(self.view.update_right_door_status)
        self.model.service_brake_updated.connect(self.view.update_service_brake_status)
        self.model.emergency_brake_updated.connect(self.view.update_eBrake_label)
        self.model.station_name_updated.connect(self.view.update_station_name)
