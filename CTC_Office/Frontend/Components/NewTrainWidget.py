#
# from datetime import datetime
from PyQt6.QtWidgets import QWidget, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal

#?List of track lines
lines = ['Red', 'Green', 'Blue']

#?List of stations on each line
Blue = ['Station B', 'Station C']
Red = ['Shadyside', 'Herron Ave', 'Swissville', 
       'Penn Station', 'Steel Plaza', 'First Ave',
       'Station Square', 'South Hills Junction']
Green = ['Glenbury', 'Dormont', 'Mt. Lebanon', 
         'Poplar', 'Castle Shanon', 'Poplar',
         'Dormont', 'Glenbury', 'Overbrook',
         'Inglewood', 'Central', 'Whited',
         'Station D', 'Whited', 'Sout Bank',
         'Central', 'Inglewood', 'Overbrook']

class Station:
    def __init__(self, stations: list):
        self.allStations = stations
        self.stationsLeft = stations

    def useStation(self, station: str):
        for i in self.stationsLeft:
            if i != station:
                self.stationsLeft.remove(station)
            else:
                self.stationsLeft.remove(station)
                break

    def addLoop(self):
        self.stationsLeft.extend(self.allStations)        

class NewTrainWidget(QWidget):

    emitTrain = pyqtSignal(dict)
    emitYardSwitch = pyqtSignal(int)
    def __init__(self, stations: list = []):
        super().__init__()
        self.layout = QVBoxLayout()
        
        self.title = QLabel()
        self.title.setText("Dispatch New Train")
        self.layout.addWidget(self.title)

        self.submit = QPushButton()
        self.submit_state = True
        self.submit.setText("Submit")
        self.submit.released.connect(self.onSubmit)
        self.submit.setChecked(self.submit_state)

        self.station = QComboBox()
        self.stationList = Station(stations)
        self.updateDropdown()

        self.timebox = QHBoxLayout()
        self.hour = QComboBox()
        self.hour.setStyleSheet("QComboBox { combobox-popup: 0; }");
        self.hour.setMaxVisibleItems(5)
        self.hour.addItems([str(i) for i in range(24)])
        self.minute = QComboBox()
        self.minute.setStyleSheet("QComboBox { combobox-popup: 0; }");
        self.minute.setMaxVisibleItems(5)
        self.minute.addItems([str(i) for i in range(60)])
        self.second = QComboBox()
        self.second.setStyleSheet("QComboBox { combobox-popup: 0; }");

        self.second.setMaxVisibleItems(5)
        self.second.addItems([str(i) for i in range(60)])

        self.timebox.addWidget(self.hour)
        self.timebox.addWidget(self.minute)
        self.timebox.addWidget(self.second)

        self.layout.addWidget(self.station)
        self.layout.addWidget(QLabel("Time: (HH:MM:SS)"))
        self.layout.addLayout(self.timebox)
        self.layout.addWidget(self.submit)

        #This is for the string that goes to the train on creation. 
        
        self.setLayout(self.layout)


    def updateDropdown(self):
        self.station.clear()
        self.station.addItems(self.stationList.stationsLeft)
    
    def onSubmit(self):
        #! emit proper data to the main file which interracts with the schedule


        self.submit_state = False

        output = {self.station.currentIndex(): [int(self.hour.currentText()), int(self.minute.currentText()), int(self.second.currentText())]}
        self.emitTrain.emit(output)
        self.emitYardSwitch.emit(0) #! When a train is scheduled to only go to one station
                                    #! It will be sent to the yard after it reaches the station
        self.submit_state = True

        

        
        
        
        



        



