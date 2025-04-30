from PyQt6.QtWidgets import QApplication
import sys
import os
from app import CTCApplication
import importlib

print(os.getcwd())
sys.path.insert(1, os.getcwd() + '/CTC_Office/Backend')
from CTC import CTC_Office

CTC = CTC_Office()
CTC.addGreenLine()

from GetGreen import Green
green = Green()
from Default import greenDefault
from TrainSchedule import TrainSchedule
from Train import Train
green = CTC.line["Green"]
Thomas = TrainSchedule(green)
I, O = greenDefault()
from Route import Route
Incoming = Route(63, 2, green)
Incoming.paths = I
#print(I)
#print(Incoming.paths[0])
#import numpy as np
Outgoing = Route(1, 58, green)
Outgoing.paths = O
Thomas.routes = [Incoming, Outgoing]

James = Train(line=green, schedule=Thomas, id=101, location=green.graph[0])
#print(James.schedule.routes[1].paths)
from Schedule import Schedule
CTC.Schedule["Green"] = Schedule("Green")
CTC.Schedule["Green"].addTrain(James)

app = QApplication(sys.argv)

window = CTCApplication(Office=CTC)
window.show()

app.exec()