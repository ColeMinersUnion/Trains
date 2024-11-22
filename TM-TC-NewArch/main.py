# main.py
from PyQt5.QtWidgets import QApplication
from TMmodel import TrainModel
from TMview import TrainModelView
from TMcontroller import TrainModelController
from TCmodel import TCmodel
from TCview import TCView
from TCcontroller    import TCcontroller  

if __name__ == "__main__":
    app = QApplication([])

    # Create the train model and view
    train_model = TrainModel()
    train_model_view = TrainModelView()
    train_model_controller = TrainModelController(train_model, train_model_view)

    # Create the train controller model and view
    train_controller_model = TCmodel()
    train_controller_view = TCView()
    train_controller_controller = TCcontroller  (train_controller_model, train_controller_view)

    # Connect the train controller to the train model
    train_controller_model.power_command.connect(train_model.set_power)
    train_model.velocity_updated.connect(train_controller_model.set_velocity)

    # Show the views
    train_model_view.show()
    train_controller_view.show()

    app.exec()
