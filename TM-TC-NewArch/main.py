# main.py
from PyQt6.QtWidgets import QApplication
from TrainWrapper import Train

if __name__ == "__main__":
    app = QApplication([])

    train = Train()

    # Show the views
    train.train_model_view.show()
    train.train_controller_view.show()

    app.exec()
