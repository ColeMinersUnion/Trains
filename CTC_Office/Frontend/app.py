from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from Components.SchedulePreviewer import SchedulePreviewer
from Backend.CTC import CTC_Office
from datetime import datetime


Office = CTC_Office()
Office.addBlueLine()
Office.addTrain(['Station C'])

class CTCApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CTC Office")
        widget = SchedulePreviewer()
        id = Office.nextID - 1
        train = Office.Schedule.trains[id]
        widget.update(id, train.location, train.Next_stop, datetime.now())
        # Set the central widget of the Window.
        self.setCentralWidget(widget)



