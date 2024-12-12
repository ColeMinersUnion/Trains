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

        #all new connects for lights/doors/sbrake
        self.train_controller_view.manual_left_doors.connect(self.train_model.toggleLeftDoors) #connect driver left doors to tm toggle function to ask for value change
        self.train_controller_view.manual_right_doors.connect(self.train_model.toggleRightDoors) #connect driver right doors
        self.train_controller_view.manual_lights.connect(self.train_model.toggleInteriorLights) #connect driver lights
        self.train_controller_view.manual_hl.connect(self.train_model.toggleExteriorLights) #connect driver headlights
        self.train_controller_view.sbrake_signal.connect(self.train_model.toggleServiceBrake) #connect driver sbrake
        self.train_controller_view.manual_temperature.connect(self.train_model.setTemperature) #connect driver temp

        #if train model approves, then these are sent 
        self.train_model.left_door_updated.connect(self.train_controller_model.left_doors_slot)
        self.train_model.right_door_updated.connect(self.train_controller_model.right_doors_slot)
        self.train_model.intLights_updated.connect(self.train_controller_model.lights_slot)
        self.train_model.extLights_updated.connect(self.train_controller_model.headlights_slot)
        self.train_model.service_brake_updated.connect(self.train_controller_model.sbrake_slot)

        # Connect the train controller to the train model for brake inputs and outputs
        self.train_controller_model.ebrake_change.connect(self.train_model.toggleEmergencyBrake)
        self.train_model.emergency_brake_updated.connect(self.train_controller_model.set_ebrake)

        #go nogo signal connect
        self.train_model.boolean_authority_signal.connect(self.train_controller_model.wayside_stop)
        
        #display station name
        self.train_controller_model.station_name_display.connect(self.train_model.updateStationName)


