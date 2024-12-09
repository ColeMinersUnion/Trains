from PyQt6.QtWidgets import QWidget
try:
    from TMmodel import TrainModel
    from TMview import TrainModelView
    from TMcontroller import TrainModelController
    from TCmodel import TCmodel
    from TCview import TCView
    from TCcontroller    import TCcontroller
except:
    import os, sys
    sys.path.insert(1, os.path.join(os.getcwd(), 'TM_TC_NewArch'))
    from TMmodel import TrainModel
    from TMview import TrainModelView
    from TMcontroller import TrainModelController
    from TCmodel import TCmodel
    from TCview import TCView
    from TCcontroller    import TCcontroller


class Train(QWidget):
    def __init__(self, routeInfo:list, authority:str):
        super().__init__()

        # Create the train model and view
        self.train_model = TrainModel(routeInfo)
        self.train_model_view = TrainModelView()
        self.train_model_controller = TrainModelController(self.train_model, self.train_model_view)

        # Create the train controller model and view
        self.train_controller_model = TCmodel()
        self.train_controller_view = TCView()
        self.train_controller_controller = TCcontroller(self.train_controller_model, self.train_controller_view, authority)

        # Connect the train controller to the train model for calculating velocity
        self.train_controller_model.power_command.connect(self.train_model.set_power)
        self.train_model.velocity_updated.connect(self.train_controller_model.set_current_speed)

        #added by hannah
        self.train_controller_model.left_doors_signal.connect(self.train_model.toggleLeftDoors)
        self.train_controller_model.right_doors_signal.connect(self.train_model.toggleRightDoors)
        self.train_controller_model.lights_signal.connect(self.train_model.toggleInteriorLights)
        self.train_controller_model.headlights_change.connect(self.train_model.toggleExteriorLights)
        self.train_model.block_change.connect(self.train_controller_model.block_switch)
        self.train_model.speed_limits.connect(self.train_controller_model.set_speed_limits)

        self.train_model.acceleration_updated.connect(self.train_controller_model.update_acceleration)
        self.train_controller_model.sbrake_change.connect(self.train_model.toggleServiceBrake)
        self.train_model.acceleration_updated.connect(self.train_controller_view.acceleration_changed)

        #parse route info 
        self.train_model.parseRouteInfo()

        # Connect the train controller to the train model for brake inputs and outputs
        self.train_controller_model.ebrake_change.connect(self.train_model.toggleEmergencyBrake)
