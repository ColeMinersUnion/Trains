# method to automtically make shapes and add to array, for loop to make new blocks with arrays of requests

import PyQt6
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QRadioButton
from PyQt6.QtGui import QIcon, QTransform
from PyQt6.QtCore import Qt
import sys 
import TrackModelBackend
from TrackModelBackend import linenames, lines      

class Map(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1280,720)
        self.setWindowTitle("Track Model Map")
        self.setStyleSheet("background-color: lightyellow;")

class Testbench(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400,400)
        self.setWindowTitle("Track Model Testbench")

        trainbutton = QPushButton("Run train", self)
        trainbutton.move(100,50)

        switchbutton = QPushButton("Flip switch", self)
        switchbutton.move(100,100)

        param2=QLabel("Line number",self)
        param2.move(100,150)
        self.input2 = QLineEdit(self)
        self.input2.move(100,200)

        param3=QLabel("Velocity # / Switch #",self)
        param3.move(100,250)
        self.input2 = QLineEdit(self)
        self.input2.move(100,300)

'''
class BlockIcon(QPushButton):
    

class SwitchIcon(QPushButton):


class CrossingIcon(QPushButton):


class TransponderIcon(QPushButton):


class StationIcon(QPushButton):
'''

app=QApplication(sys.argv)
TrackModelBackend.read('TrackModel/Blue Line.xlsx')
map=Map()
testbench=Testbench()
map.show()
testbench.show()
sys.exit(app.exec())