#from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from Components.SchedulePreviewer import SchedulePreviewer
from datetime import datetime


class CTCApplication(QMainWindow):
    def __init__(self, Office):
        super().__init__()
        self.Office = Office
        self.scheduleWidget = SchedulePreviewer()
        self.button = QPushButton("Move")
        self.layout = QVBoxLayout()
        self.main = QWidget()
        self.button_state = True



        self.setWindowTitle("CTC Office")
        id = self.Office.nextID - 1
        #print(id)
        train = self.Office.Schedule.trains[id]
        train.move()
        self.scheduleWidget.update(train.id, str(train.location), train.Next_Stop, datetime.now())
        # Set the central widget of the Window.
        self.button.setCheckable(True)
        self.button.released.connect(self.onClick)
        self.button.setChecked(self.button_state)

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.scheduleWidget.widget)

        self.main.setLayout(self.layout)

        self.setCentralWidget(self.main)
    
    def onClick(self):
        id = self.Office.nextID - 1
        #print(id)
        train = self.Office.Schedule.trains[id]
        train.move()
        self.scheduleWidget.update(train.id, str(train.location), train.Next_Stop, datetime.now())

        self.button_state = self.button.isChecked()

        
    
    

         



