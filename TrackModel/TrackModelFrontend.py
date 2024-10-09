# method to automtically make shapes and add to array, for loop to make new blocks with arrays of requests

import PyQt6
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QSlider
from PyQt6.QtGui import QTransform, QPixmap, QIcon
from PyQt6.QtCore import Qt,QTimer
import sys 
import TrackModelBackend
from TrackModelBackend import lines,failmode,CLOCK_TIME, failnames,modelspeed      

passive = [] #no update method, do not react to backend changes
active = [] #update method, react to backend changes


SCL=100 #scale
YFF=360 #y-offset
#the below label styles are only used for widgets assigned transparent backgrounds in PyQT
labelstyle = """QLabel {
                background-color: transparent
                }"""
tooltipstyle = """QToolTip { 
                background-color: lightgray; 
                color: white; 
                border: white solid 1px
                }"""

class HeaterSystem(QWidget):
    def __init__(self,window):
        super().__init__()
        self.temp=70
        self.label = QLabel(window)
        self.label.move(405,0)
        self.label.setToolTip("Track heaters off")
        self.on=False
        pixmap = QPixmap('TrackModel/Icons/OffHeater.png')
        self.label.setPixmap(pixmap)
        
        self.slider = QSlider(Qt.Orientation.Horizontal, window)
        self.slider.setGeometry(450,0,180,45)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.update)
        
        self.number = QLabel(window)
        self.number.move(630,0)
        self.number.setText(str(self.temp) + " °F")

        self.slider.setValue(self.temp)

    def update(self):
        self.temp=self.slider.value()
        self.number.setText(str(self.temp) + " °F")
        self.number.adjustSize()

        if((not self.on) and self.temp<=32):
            self.label.setToolTip("Track heaters on")
            self.on=True
            pixmap = QPixmap('TrackModel/Icons/OnHeater.png')
            self.label.setPixmap(pixmap)

        if(self.on and self.temp>32):
            self.label.setToolTip("Track heaters off")
            self.on=False
            pixmap = QPixmap('TrackModel/Icons/OffHeater.png')
            self.label.setPixmap(pixmap)

class Failure(QWidget):
    def __init__(self,linenum,blocknum,window):
        global failmode
        super().__init__()
        self.linenum = linenum
        self.blocknum = blocknum
        self.pixmap = QPixmap('TrackModel/Icons/' + failnames[failmode] + 'Failure.png')
        self.label = QLabel(window)
        self.label.setPixmap(self.pixmap)
        self.label.setToolTip(failnames[failmode] + " Failure\n " + TrackModelBackend.linenames[linenum] + " Line, Block " + str(blocknum))
        center = lines[linenum].blocks[blocknum].center
        self.label.move(int(center[0]*SCL-25),int(YFF-center[1]*SCL-22.5))
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        
    def update(self):
        global active
        if(lines[self.linenum].blocks[self.blocknum].failure==0):
            active.remove(self)

class FailureSelect(QWidget):
    def __init__(self,window):
        super().__init__()
        self.label = QLabel(window)
        self.label.setPixmap(QPixmap('TrackModel/Icons/FailureSelect.png'))
        self.update()
    
    def update(self):
        if(failmode==0):
            self.label.move(-100,-100)
        else:
            self.label.move(180+failmode*45,50)
        

class FailureButton(QWidget):
    def __init__(self,failnum,window):
        super().__init__()
        self.failnum=failnum
        self.pixmap = QPixmap('TrackModel/Icons/' + failnames[failnum] + 'Failure.png')
        self.label = QLabel(window)
        self.label.setPixmap(self.pixmap)
        self.label.setToolTip(failnames[failnum] + " Failure")
        self.label.move(180+failnum*45,0)
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.label.mousePressEvent = self.changeFailMode

    def changeFailMode(self,event):
        global failmode
        if (failmode==self.failnum):
            failmode=0
        else:   
            failmode=self.failnum

class BlockIcon(QWidget):
    def __init__(self,obj,window): #line number and block number
        super().__init__()
        self.window=window
        self.obj=obj
        self.pixmap = QPixmap('TrackModel/Icons/BlueArrow.png')
        self.label=QLabel(window)
        self.pixmap = self.pixmap.transformed(QTransform().scale(obj.mag*SCL/100,1))
        self.pixmap = self.pixmap.transformed(QTransform().rotate(0-self.obj.angle))
        self.label.setPixmap(self.pixmap)
        self.label.setToolTip(obj.toString())
        offset = 92 if self.obj.angle==45 else 0
        self.label.move(self.obj.x1*SCL,YFF-self.obj.y1*SCL-13-offset)
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.label.mousePressEvent = self.setFailure
        self.setFailure(None)

    def update(self):
        self.label.setToolTip(self.obj.toString())
        self.label.show()


    def setFailure(self,event):
        global active, failmode
        if(failmode > 0):
            lines[self.obj.linenum].blocks[self.obj.number].failure = failmode
            active.append(Failure(self.obj.linenum,self.obj.number,self.window))

class SwitchIcon(QWidget):
    def __init__(self,obj,window):
        super().__init__()
        self.linenum=obj.linenum
        self.switchid=obj.switchid
        pixmap = QPixmap('TrackModel/Icons/OpenSwitch.png')
        self.openlabel=QLabel(window)
        self.openlabel.setPixmap(pixmap)
        self.openlabel.setToolTip("Switched open")
        self.openlabel.setStyleSheet(labelstyle)
        pixmap = QPixmap('TrackModel/Icons/ClosedSwitch.png')
        self.closedlabel=QLabel(window)
        self.closedlabel.setPixmap(pixmap)
        self.closedlabel.setToolTip("Switched closed")
        self.closedlabel.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        
    def update(self):
        global lines
        tempobj=lines[self.linenum].switches[self.switchid]
        opencenter=lines[tempobj.linenum].blocks[tempobj.getopen()].center
        closedcenter=lines[tempobj.linenum].blocks[tempobj.getclosed()].center
        self.openlabel.move(int((opencenter[0]-0.125)*SCL),int(YFF-(opencenter[1]+0.225)*SCL))
        self.closedlabel.move(int((closedcenter[0]-0.125)*SCL),int(YFF-(closedcenter[1]+0.225)*SCL))
        self.openlabel.show()
        self.closedlabel.show()
    
class CrossingIcon(QWidget):
    def __init__(self,obj,window):
        super().__init__()
        self.linenum=obj.linenum
        self.crossingid=obj.crossingid
        self.label=QLabel(window)
        center = lines[obj.linenum].blocks[obj.block].center
        self.label.move(int(center[0]*SCL-25),int(YFF-center[1]*SCL-22.5))
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.update()

    def update(self):
        tempobj = lines[self.linenum].crossings[self.crossingid]
        if (tempobj.on==True):
            self.pixmap = QPixmap('TrackModel/Icons/OnCrossing.png')
        else:
            self.pixmap = QPixmap('TrackModel/Icons/OffCrossing.png')
        self.label.setPixmap(self.pixmap)
        self.label.setToolTip(tempobj.toString())
        self.label.show()

class TransponderIcon(QWidget):
    def __init__(self,obj,window):
        super().__init__()
        self.obj=obj
        self.pixmap = QPixmap('TrackModel/Icons/Transponder.png')
        self.label=QLabel(window)
        self.label.setPixmap(self.pixmap)
        self.label.setToolTip(obj.msg) #no toString, transponder message is static
        center = lines[obj.linenum].blocks[obj.block].center
        self.label.move(int(center[0]*SCL-5),int(YFF-center[1]*SCL-12.5))
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)

class StationIcon(QWidget):
    def __init__(self,obj,window):
        super().__init__()
        self.obj=obj
        if(self.obj.name=="YARD"):
            pixmap = QPixmap('TrackModel/Icons/Yard.png')
        else:
            pixmap = QPixmap('TrackModel/Icons/Station.png')
        self.label=QLabel(window)
        self.label.setPixmap(pixmap)
        self.label.setToolTip(obj.msg) #no toString, station message is static
        center = lines[obj.linenum].blocks[obj.block].center
        self.label.move(int(center[0]*SCL-5),int(YFF-center[1]*SCL-12.5))
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)

class Map(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1280,720)
        self.move(0,0)
        self.setWindowTitle("Track Model Map")
        self.setStyleSheet("background-color: lightyellow;")
        TrackModelBackend.read('TrackModel/Blue Line.xlsx')
        active.append(FailureSelect(self))
        passive.append(HeaterSystem(self))
        for i in range(3):
            passive.append(FailureButton((i+1),self)) #add failure buttons
        for line in lines:
            for block in line.blocks:
                active.append(BlockIcon(block,self)) #updates for view
            for switch in line.switches: #biggest components to smallest so all can be hovered
                active.append(SwitchIcon(switch,self))
            for crossing in line.crossings:
                active.append(CrossingIcon(crossing,self))
            for transponder in line.transponders:
                passive.append(TransponderIcon(transponder,self))  
            for station in line.stations:
                passive.append(StationIcon(station,self))
        self.timer=QTimer() #timer for active components
        self.timer.timeout.connect(self.update) #connect timer to update method
        self.timer.start(int(CLOCK_TIME*1000)) #set clock speed of timer

        self.tenBaud=QTimer() #timer for active components
        self.tenBaud.timeout.connect(self.tenBaudClock) #connect timer to update method
        self.tenBaud.start(int(CLOCK_TIME*1000)) #set clock speed of timer
    
    def tenBaudClock(self):
        print("10 baud passed")
        for l in lines:
            for t in l.trains:
                t.tenBaudMessage

        
    
    def update(self): 
        for a in active:
            a.update() #update every active component

class Testbench(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400,400)
        self.move(1500,0)
        self.setWindowTitle("Track Model Testbench")

        param1=QLabel("Line number",self)
        param1.move(100,150)
        self.input1 = QLineEdit(self)
        self.input1.move(100,200)

        param2=QLabel("Component #",self)
        param2.move(100,250)
        self.input2 = QLineEdit(self)
        self.input2.move(100,300)

        occupybutton = QPushButton("Set occupancy", self)
        occupybutton.move(100,50)
        occupybutton.clicked.connect(self.switchOccupancy)

        switchbutton = QPushButton("Flip switch", self)
        switchbutton.move(100,75)
        switchbutton.clicked.connect(self.flipSwitch)

        crossingbutton = QPushButton("Change crossing", self)
        crossingbutton.move(100,100)
        crossingbutton.clicked.connect(self.flipCrossing)

        param1=QLabel("Line number",self)
        param1.move(100,150)
        self.input1 = QLineEdit(self)
        self.input1.move(100,200)

        param2=QLabel("Component #",self)
        param2.move(100,250)
        self.input2 = QLineEdit(self)
        self.input2.move(100,300)

    def switchOccupancy(self):
        line = int(self.input1.text())
        comp = int(self.input2.text())
        lines[line].blocks[comp].switchOccupancy()
    def flipSwitch(self):
        line = int(self.input1.text())
        comp = int(self.input2.text())
        lines[line].switches[comp].switch()
    def flipCrossing(self):
        line = int(self.input1.text())
        comp = int(self.input2.text())
        lines[line].crossings[comp].switch()



app=QApplication(sys.argv)
map=Map()
testbench=Testbench()
map.show()
testbench.show()
sys.exit(app.exec())

