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
    sys.path.insert(1, os.getcwd() + '/TM_TC_NewArch')
    from TMmodel import TrainModel
    from TMview import TrainModelView
    from TMcontroller import TrainModelController
    from TCmodel import TCmodel
    from TCview import TCView
    from TCcontroller    import TCcontroller


class Train(QWidget):
    def __init__(self, routeInfo):
        super().__init__()

        # Create the train model and view
        self.train_model = TrainModel(routeInfo)
        self.train_model_view = TrainModelView()
        self.train_model_controller = TrainModelController(self.train_model, self.train_model_view)

        # Create the train controller model and view
        self.train_controller_model = TCmodel()
        self.train_controller_view = TCView()
        self.train_controller_controller = TCcontroller  (self.train_controller_model, self.train_controller_view)

        # Connect the train controller to the train model
        self.train_controller_model.power_command.connect(self.train_model.set_power)
        self.train_model.velocity_updated.connect(self.train_controller_model.set_current_speed)