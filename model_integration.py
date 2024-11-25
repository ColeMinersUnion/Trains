from TrackModel.TrackModelMain import Map
from TMTCNewArch.TMmodel import TrainModel
from TMTCNewArch.TMview import TrainModelView
from TMTCNewArch.TMcontroller import TrainModelController
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)

    train_model = TrainModel()
    train_model_view = TrainModelView()
    train_model_controller = TrainModelController(train_model, train_model_view)

    tm_window = Map()   
    tm_signals = tm_window.signals

    # show windows
    train_model_view.show()
    tm_window.show()

    #.connect(tm_signals.addOcc)
    #.connect(tm_signals.removeOcc)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()