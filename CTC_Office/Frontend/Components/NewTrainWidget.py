#
# from datetime import datetime
from PyQt6.QtWidgets import QWidget, QPushButton

#?List of track lines
lines = ['Red', 'Green', 'Blue']

#?List of stations on each line
Blue = ['Station B', 'Station C']
Red = ['Shadyside', 'Herron Ave', 'Swissville', 
       'Penn Station', 'Steel Plaza', 'First Ave',
       'Station Square', 'South Hills Junction']
Green = ['Pioneer', 'Edgebrook', 'Station D', 
         'Whited', 'South Bank', 'Central',
         'Inglewood', 'Overbrook', 'Glenbury',
         'Dormont', 'MT Lebanon', 'Poplar',
         'Castle Shannon', 'Dormont', 'Glenbury',
         'Overbrook', 'Inglewood', 'Central']

class NewTrainWidget(QWidget):
    def __init__(self):
        self.arrivalTime = ""
        self.stationsList = []
        self.line = []
        self.submit = QPushButton()
        self.submit_state = True
    



