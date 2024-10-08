from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from Components.SchedulePreviewer import SchedulePreviewer
from datetime import datetime
import asyncio #To move the trains without halting the execution of my application. 


class CTCApplication(QMainWindow):
    def __init__(self, Office):
        super().__init__()
        self.Office = Office
        

        self.setWindowTitle("CTC Office")
        widget = SchedulePreviewer()
        id = Office.nextID - 1
        print(id)
        train = Office.Schedule.trains[id]
        train.move()
        widget.update(id, str(train.location), train.Next_Stop, datetime.now())
        # Set the central widget of the Window.
        self.setCentralWidget(widget.widget)



