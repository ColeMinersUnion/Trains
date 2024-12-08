import sys
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QSlider, QApplication, QFileDialog
from PyQt6.QtGui import QTransform, QPixmap
from PyQt6.QtCore import Qt,QTimer,QObject, pyqtSignal, pyqtSlot
import pandas as pd #reading the excel file
from math import atan2,pi,sqrt,pow,sin,cos

#offsets are multiplied by scl
XOFFSET = 0
YOFFSET = 3
SCL=20 #scale
occflag = True
linenames=["Green","Red"]
lines=[]
switchid=[] #track switch numbers for pinging
crossingid=[] #track crossing numbers for pinging
failmode = 0
failnames = ["No","Rail","Circuit","Power"]
heaters = False
speed = 1
fileselected = False
class Block:
    #instantiation
    def __init__(self, linenum, section, number, length, grade, speed, twoway, elevation, underground,x1,y1,x2,y2):
        self.linenum = linenum
        self.section = section
        self.number = number
        self.length = length
        self.grade = grade
        self.speed = speed
        self.twoway = twoway
        self.elevation = elevation
        self.underground = underground
        self.x=x1
        self.y=y1
        self._occupied = False
        self.center = [(x1+x2)/2,(y1+y2)/2] #center for front end
        self.mag = sqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1))) #magnitude for front end
        self.angle = atan2((y2-y1),(x2-x1))*180/pi #angle for front end
        self.failure=0
        self.authority = True 
        if(self.angle<0):
            self.angle = self.angle+360
        r = linenames[linenum] + " Line"
        r = r + "\nSection " + section
        r = r + "\nBlock " + str(number)
        r = r + "\n" + str(round(length*3.28084)) + " feet long\n"
        r = r + str(grade) + "% grade\n"
        r = r + str(round(speed*0.621371)) + " mph speed limit\n"
        r = r + "\nBidirectional: " + str(twoway)
        r = r + "\nUnderground: " + str(underground) 
        r = r + "\nOccupied: "
        self.msg = r    

    @property
    def occupied(self):
        return self._occupied
    
    @occupied.setter
    def occupied(self,newocc):
        self._occupied = newocc
        self.onOccChange()

    def onOccChange(self):
        global occflag
        occflag = True    

    def toString(self):
        return self.msg + str(self.occupied) + "\nAuthority: " + str(self.authority) + "\nFailure: " + failnames[self.failure] 
    
    def switchOccupancy(self):
        self.occupied = not self.occupied
class Switch:
#note, structuring switch depends on section, include that?)
    #instantiation
    #note, no three way switches; think V, not Δ
    def __init__(self,linenum,blocks):
        global lines
        self.linenum = linenum
        self.blocks = blocks
        self.switchid = switchid[linenum]
        switchid[linenum] = switchid[linenum]+1
        self.leftside=True #the first block is the central

    #check if  matches central vertex
    #ALL TRAINS GOING 
    def isVertex(self,block):
        return (block==self.blocks[0])
    
    #check if it has a block (USE THIS ONE TO CHECK REPEATING SWITCHES)
    def hasBlock(self,block):
        ret = False
        for blockToCheck in self.blocks:
            ret = (ret or (blockToCheck==block))
        return ret
    
    #switch the switch
    def switch(self):
        self.leftside = not self.leftside

    #set switch to left
    def setToLeft(self,bool):
        self.leftside = bool
    
    #get the open block
    def getopen(self):
        if(self.leftside):
            return self.blocks[1]
        else:
            return self.blocks[2]

    #get the closed block
    def getclosed(self):
        if(self.leftside):
            return self.blocks[2]
        else:
            return self.blocks[1]
class Crossing:
    #instantiation
    def __init__(self,linenum,block):
        self.linenum = linenum
        self.block = block
        self.on = False
        self.crossingid = crossingid[linenum]
        crossingid[linenum] = crossingid[linenum]+1
        self.msg = "Crossing (" + linenames[linenum] + " Line, Block " + str(block) + ")\nClosed: "
    def toString(self):
        return self.msg + str(self.on)

    #change state of crossing
    def switch(self):
        self.on = not self.on
class Transponder:
    #instantiation
    def __init__(self,linenum,block,data):
        self.linenum = linenum
        self.block = block 
        self.data = data
        self.msg = "Beacon (" + linenames[linenum] + " Line, Block " + str(block) + ")\n" + data
class Station: #yard also
    #instantiation
    def __init__(self,linenum,block,name,side):
        self.linenum = linenum
        self.block = block
        self.name = name
        self.side = side
        self.msg = ""
        self.passengers = 5
        if(name=="YARD"):  
            self.msg = "YARD"
        else:
            self.msg = "Station " + str(name) + "\nSide " + str(side) + "\n" + linenames[linenum] + " Line, Block " + str(block)


class Train:
    def __init__(self,linenum,block1):
        global lines
        self.linenum = linenum
        self.blocks = {block1}
        lines[self.linenum].blocks[self.block1].occupied = True
        '''
        msgqueue = 10 Baud messages passed by wayside to train via track
        tenbaud = 10 bauds available after processing the bud limit
        possible inputs through here: speed, authority, train temp, doors,
        '''
        self.msgqueue = []
        self.tenbaud = [False,False,False,False,False,False,False,False,False,False]
        self.beacondata = ""

    def toggleOcc(self,block):
        lines[self.linenum].blocks[block].occupied = not lines[self.linenum].blocks[block].occupied

    def addOcc(self,block):
        self.blocks.add(block)
        lines[self.linenum].blocks[block].occupied = True
    
    def removeOcc(self,block):
        if(block in self.blocks):
            self.blocks.remove(block)
        lines[self.linenum].blocks[block].occupied = False
    
    def queueMessage(self,bool):
        self.msgqueue.append(bool)
    def tenBaudMessage(self):
        if(len(self.msgqueue)>0):
            self.tenbaud.append(self.msgqueue[0])
            while(len(self.tenbaud>10)):
                self.tenbaud.remove(0)

        

class Line:
    def __init__(self,linenum):
        self.linenum = linenum
        self.blocks = []
        self.switches = []
        self.crossings = []
        self.transponders = []
        self.stations = []
        self.trains = []



    def getSwitch(self,block):
        for x in self.switches:
            if x.hasBlock(block):
                return x
        return None
            
    def getCrossing(self,block):
        for x in self.crossings:
            if (x.block==block):
                return x
        return None
    
    def stationByBlock(self,block):
        for x in self.stations:
            if (x.block==block):
                return x
        return None
    
    def stationByName(self,name):
        for x in self.stations:
            if (x.name==name):
                return Station
        return None

lines=[Line(0),Line(1)]

def readX(string): #return cross marks
    return (string=="X")
def read(file):
    data=pd.read_excel(file,engine='openpyxl')       
    tempswitch=[] #instantiate switches last to make sure everything is there
    i=1 #for loop doesnt work idk why
    while(i<len(data.index)): #go through all blocks/rows
        linename=data.iat[i,0] #get first line
        linenum=len(linenames)
        if linename in linenames: #if linename already added
            linenum= linenames.index(linename) #get line if already in
        else: #if linename not added
            linenames.append(linename)
            lines.append(Line(linenum))
        while len(lines[linenum].blocks) <= data.iat[i,2]:
            lines[linenum].blocks.append(None) #add values to list to fit block
            crossingid.append(0)
            switchid.append(0)
        lines[linenum].blocks[data.iat[i,2]]=Block(linenum,
                                                data.iat[i,1], #section
                                                data.iat[i,2], #block
                                                data.iat[i,3], #length
                                                data.iat[i,4], #grade
                                                data.iat[i,5], #speed
                                                readX(data.iat[i,6]), #2-way
                                                data.iat[i,7], #elevation
                                                readX(data.iat[i,8]), #undeground
                                                XOFFSET+data.iat[i,15], #x1-coord
                                                YOFFSET+data.iat[i,16], #y1-coord
                                                XOFFSET+data.iat[i,17], #x2-coord
                                                YOFFSET+data.iat[i,18]) #y2-coord
        if(not (pd.isnull(data.iat[i,9]) or pd.isnull(data.iat[i,10]))):
            tempswitch.append([linenum,data.iat[i,2],data.iat[i,9],data.iat[i,10]])
        if(not pd.isnull(data.iat[i,11])):
            lines[linenum].transponders.append(Transponder(linenum,data.iat[i,2],data.iat[i,11]))
        if(not pd.isnull(data.iat[i,12])):
            lines[linenum].stations.append(Station(linenum,data.iat[i,2],data.iat[i,12],data.iat[i,13]))
        if(readX(data.iat[i,14])):
            lines[linenum].crossings.append(Crossing(linenum,data.iat[i,2]))
        i=i+1 #increment
    for s in tempswitch: #add switches now, blocks should update
        lines[s[0]].switches.append(Switch(s[0],[s[1],s[2],s[3]])) #add switch to appropriate line number
    return
class SignalHandler(QObject):

    sendOccupancies = pyqtSignal(list)
    sendAuthorities = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def callOccSend(self, occupancies: list):
        self.sendOccupancies.emit(occupancies)

    def callAuthSend(self): # call to send authorities to train
        authorities=[]
        for b in lines[0].blocks:
            authorities.append(b.authority) 
        self.sendAuthorities.emit(authorities)

    @pyqtSlot(int)
    def toggleOcc(self,message):
        lines[0].blocks[message].occupied = not lines[0].blocks[message].occupied

    @pyqtSlot(list)
    def getHardwareAuthority(self,message):
        for i in range(len(lines[0].blocks)):
            if(i<41 or i>68):
                lines[0].blocks[i].authority = message[i]

    @pyqtSlot(list)
    def getSoftwareAuthority(self,message):
        for i in range(len(lines[0].blocks)):
            if(i>40 and i<69):
                lines[0].blocks[i].authority = message[i]

    @pyqtSlot(bool)
    def getSwitch13(self,message):
        lines[0].switches[0].setToLeft(message) 

    @pyqtSlot(bool)
    def getSwitch28(self,message):
        lines[0].switches[1].setToLeft(not message) 

    @pyqtSlot(bool)
    def getSwitch58(self,message):
        lines[0].switches[2].setToLeft(message)

    @pyqtSlot(bool)
    def getSwitch62(self,message):
        lines[0].switches[3].setToLeft(message)

    @pyqtSlot(bool)
    def getSwitch77(self,message):
        lines[0].switches[4].setToLeft(not message)

    @pyqtSlot(bool)
    def getSwitch85(self,message):    
        lines[0].switches[5].setToLeft(message)

    @pyqtSlot(bool)
    def getCrossing19(self,message):
        lines[0].crossings[0].on=message #crossing 19

    @pyqtSlot(bool)
    def getCrossing108(self,message):
        lines[0].crossings[1].on=message #crossing 108    

# FRONT END BRANCH

passive = [] #no update method, do not react to backend changes
active = [] #update method, react to backend changes
#the below label styles are only used for widgets assigned transparent backgrounds in PyQT
labelstyle = """QLabel {
                background-color: transparent
                }"""
tooltipstyle = """QToolTip { 
                background-color: lightgray; 
                color: white; 
                border: white solid 1px
                }"""

def offset(angle):
    x=angle
    if(x<0): #min angle check
        x=x+360
    if(x>360): #max angle check
        x=x-360
    if(x>315):
        return 1 - ((x - 315)/45)
    if(x>225):
        return 1
    if(x>180):
        return (x-180)/45
    return 0
    
clock=0
class SpeedMeter(QWidget):
    def __init__(self,window):
        global speed
        super().__init__()  
        self.slider = QSlider(Qt.Orientation.Horizontal, window)
        self.slider.setGeometry(750,0,180,45)
        self.slider.setMinimum(-100)
        self.slider.setMaximum(200)
        self.slider.valueChanged.connect(self.update)
        
        self.number = QLabel(window)
        self.number.move(930,0)
        self.slider.setValue(0)
        self.number.setText(str(speed) + "x")


    def update(self):
        global speed
        temp=self.slider.value()
        speed=float(int(10*pow(10,temp/100))/10)
        self.number.setText(str(speed) + "x")
        self.number.adjustSize()

class HeaterSystem(QWidget):
    def __init__(self,window):
        super().__init__()
        self.temp=70
        self.label = QLabel(window)
        self.label.move(405,0)
        self.label.setToolTip("Track heaters off")
        pixmap = QPixmap('TrackModel/Icons/OffHeater.png')
        self.label.setPixmap(pixmap)
        
        self.slider = QSlider(Qt.Orientation.Horizontal, window)
        self.slider.setGeometry(450,0,180,45)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.valueChanged.connect(self.update)
        
        self.number = QLabel(window)
        self.number.move(630,0)
        self.number.setText(str(self.temp) + " °F")

        self.slider.setValue(self.temp)

    def update(self):
        global heaters
        self.temp=self.slider.value()
        self.number.setText(str(self.temp) + " °F")
        self.number.adjustSize()

        if((not heaters) and self.temp<=32):
            self.label.setToolTip("Track heaters on")
            heaters=True
            pixmap = QPixmap('TrackModel/Icons/OnHeater.png')
            self.label.setPixmap(pixmap)

        if(heaters and self.temp>32):
            self.label.setToolTip("Track heaters off")
            heaters=False
            pixmap = QPixmap('TrackModel/Icons/OffHeater.png')
            self.label.setPixmap(pixmap)

class TrainOccupy(QWidget):
    def __init__(self,linenum,blocknum,window):
        global failmode
        super().__init__()
        self.linenum = linenum
        self.blocknum = blocknum
        self.label = QLabel(window)
        self.center = lines[linenum].blocks[blocknum].center
        self.check=False
        pixmap = QPixmap('TrackModel/Icons/TrainOccupy.png')
        pixmap = pixmap.transformed(QTransform().scale(SCL/100,SCL/100))
        self.label.setPixmap(pixmap)
        self.label.move(-100,-100)
        self.label.setToolTip("Occupied at \n" + linenames[linenum] + " Line, Block " + str(blocknum))
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.update()

    def update(self):
        occ = lines[self.linenum].blocks[self.blocknum].occupied
        if(self.check!=occ):
            if(occ):
                self.label.move((int((self.center[0]-0.125)*SCL)),int((self.center[1]+0.175)*SCL))
            else:
                self.label.move(-100,-100)
            self.label.show()
            self.check=occ


class Failure(QWidget):
    def __init__(self,linenum,blocknum,window):
        global failmode
        super().__init__()
        self.linenum = linenum
        self.blocknum = blocknum
        self.label = QLabel(window)
        self.center = lines[linenum].blocks[blocknum].center
        self.check=0
        pixmap = QPixmap('TrackModel/Icons/RailFailure.png')
        self.label.setPixmap(pixmap)
        self.label.move(-100,-100)
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.update()
        
    def update(self):
        objfail = lines[self.linenum].blocks[self.blocknum].failure
        if(self.check!=objfail):
            if(objfail==0):
                self.label.move(-100,-100)
            else:
                pixmap = QPixmap('TrackModel/Icons/' + failnames[objfail] + 'Failure.png')
                pixmap = pixmap.transformed(QTransform().scale(SCL/100,SCL/100))
                self.label.setPixmap(pixmap)
                self.label.move((int((self.center[0]-0.125)*SCL)),int((self.center[1]-0.45)*SCL))
                self.label.setToolTip(failnames[objfail] + " Failure\n" + linenames[self.linenum] + " Line, Block " + str(self.blocknum))
            self.label.show()
            self.check=objfail

        

class FailureSelect(QWidget):
    def __init__(self,window):
        super().__init__()
        self.label = QLabel(window)
        self.label.setPixmap(QPixmap('TrackModel/Icons/FailureSelect.png'))
        self.label.move(-100,-100)
        self.check=0
        self.update()
    
    def update(self):
        if(self.check!=failmode):
            self.label.move(180+failmode*45,50)
            self.check=failmode

class FileButton(QWidget):
    def __init__(self,window):
        super().__init__()
        pixmap = QPixmap('TrackModel/Icons/SelectFile.png')
        self.label = QLabel(window)
        self.label.setPixmap(pixmap)
        self.label.move(90,0)
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.label.setToolTip("Select File")

        self.label.mousePressEvent = self.selectFile

    def selectFile(self, message):
        global fileselected
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx)")
        if filename:
            read(filename)
        fileselected = True

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
        global active
        self.window=window
        self.obj=obj
        pixmap = QPixmap('TrackModel/Icons/' + linenames[obj.linenum] + 'Arrow' + ('Bi' if (obj.twoway) else '') + '.png')
        self.label=QLabel(window)
        pixmap = pixmap.transformed(QTransform().scale(obj.mag*SCL/100,SCL/50))
        pixmap = pixmap.transformed(QTransform().rotate(self.obj.angle))
        self.label.setPixmap(pixmap)
        self.label.setToolTip(obj.toString())
        xoff = obj.mag*cos(obj.angle*pi/180)*offset(obj.angle+90)
        yoff = obj.mag*sin(obj.angle*pi/180)*offset(obj.angle)
        self.label.move(int((obj.x+xoff)*SCL),int((obj.y+yoff)*SCL))
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.label.mousePressEvent = self.setFailure
        active.append(Failure(self.obj.linenum,self.obj.number,self.window))
        active.append(TrainOccupy(self.obj.linenum,self.obj.number,self.window))

    def update(self):
        self.label.setToolTip(self.obj.toString())
        self.label.show()

    def setFailure(self,event):
        global failmode
        objfail = lines[self.obj.linenum].blocks[self.obj.number].failure
        lines[self.obj.linenum].blocks[self.obj.number].failure = failmode
        lines[self.obj.linenum].blocks[self.obj.number].occupied = (failmode in [1,3])      

class SwitchIcon(QWidget):
    def __init__(self,obj,window):
        super().__init__()
        self.linenum=obj.linenum
        self.switchid=obj.switchid
        pixmap = QPixmap('TrackModel/Icons/OpenSwitch.png')
        pixmap = pixmap.transformed(QTransform().scale(SCL/100,SCL/100))
        self.openlabel=QLabel(window)
        self.openlabel.setPixmap(pixmap)
        self.openlabel.setToolTip("Switched open")
        self.openlabel.setStyleSheet(labelstyle)
        pixmap = QPixmap('TrackModel/Icons/ClosedSwitch.png')
        pixmap = pixmap.transformed(QTransform().scale(SCL/100,SCL/100))
        self.closedlabel=QLabel(window)
        self.closedlabel.setPixmap(pixmap)
        self.closedlabel.setToolTip("Switched closed")
        self.closedlabel.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.check=[0,0]
        
    def update(self):
        global lines
        tempobj=lines[self.linenum].switches[self.switchid]
        opencenter=lines[tempobj.linenum].blocks[tempobj.getopen()].center
        if(self.check!=opencenter):
            closedcenter=lines[tempobj.linenum].blocks[tempobj.getclosed()].center
            self.openlabel.move(int((opencenter[0]-0.125)*SCL),int((opencenter[1]+0.225)*SCL))
            self.closedlabel.move(int((closedcenter[0]-0.125)*SCL),int((closedcenter[1]+0.225)*SCL))
            self.openlabel.show()
            self.closedlabel.show()
            self.check=opencenter
    
class CrossingIcon(QWidget):
    def __init__(self,obj,window):
        super().__init__()
        self.linenum=obj.linenum
        self.crossingid=obj.crossingid
        self.label=QLabel(window)
        self.check=True
        center = lines[obj.linenum].blocks[obj.block].center
        self.label.move(int((center[0]-0.25)*SCL),int((center[1]-0.225)*SCL))
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.update()

    def update(self):
        obj = lines[self.linenum].crossings[self.crossingid]
        if(self.check!=obj.on):
            if (obj.on):
                self.pixmap = QPixmap('TrackModel/Icons/OnCrossing.png')
            else:
                self.pixmap = QPixmap('TrackModel/Icons/OffCrossing.png')
            self.check=obj.on
            self.pixmap = self.pixmap.transformed(QTransform().scale(SCL/100,SCL/100))
            self.label.setPixmap(self.pixmap)
            self.label.setToolTip(obj.toString())
            self.label.show()

class TransponderIcon(QWidget):
    def __init__(self,obj,window):
        super().__init__()
        self.obj=obj
        pixmap = QPixmap('TrackModel/Icons/Transponder.png')
        pixmap = pixmap.transformed(QTransform().scale(SCL/100,SCL/100))
        self.label=QLabel(window)
        self.label.setPixmap(pixmap)
        self.label.setToolTip(obj.msg) #no toString, transponder message is static
        center = lines[obj.linenum].blocks[obj.block].center
        self.label.move(int((center[0]-0.05)*SCL),int((center[1]-0.125)*SCL))
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)

class StationIcon(QWidget):
    def __init__(self,obj,window):
        super().__init__()
        self.obj=obj
        if(self.obj.name=="Yard"):
            pixmap = QPixmap('TrackModel/Icons/Yard.png')
        else:
            pixmap = QPixmap('TrackModel/Icons/Station.png')
        self.label=QLabel(window)
        pixmap = pixmap.transformed(QTransform().scale(SCL/100,SCL/100))
        self.label.setPixmap(pixmap)
        self.label.setToolTip(obj.msg) #no toString, station message is static
        center = lines[obj.linenum].blocks[obj.block].center
        self.label.move(int((center[0]-0.05)*SCL),int((center[1]-0.125)*SCL))
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)

class Map(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1280,720)
        self.move(0,0)
        self.setWindowTitle("Track Model Map")
        self.setStyleSheet("background-color: lightyellow;")
        passive.append(FileButton(self))
        passive.append(HeaterSystem(self))
        for i in range(4):
            passive.append(FailureButton((i),self)) #add failure buttons
        active.append(FailureSelect(self)) #this goes after the dynamic icons, we hide them behind this widget system
        read("TrackModel/Red Line.xlsx")
        read("TrackModel/Green Line.xlsx")
        print(str(len(lines[0].blocks)))
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
        active.append(SpeedMeter(self))
        self.timer=QTimer() #timer for active components
        self.timer.timeout.connect(self.update) #connect timer to update method
        self.timer.start(int(1000/60)) #set clock speed of timer

        self.tenBaud=QTimer() #timer for active components
        self.tenBaud.timeout.connect(self.tenBaudClock) #connect timer to update method
        self.tenBaud.start(1) #set clock speed of timer

        self.signals=SignalHandler()
        self.show()
    
    def tenBaudClock(self):
        global lines
        global clock
        global speed
        clock += speed
        if clock>=1000:
            clock -= 1000
            #print("10 baud passed")
            for l in lines:
                for t in l.trains:
                    t.tenBaudMessage()
    
    def update(self): 
        global occflag
        for a in active:
            a.update() #update every active component
        if(occflag):
            print("occ update")
            occupancies=[]
            for b in lines[0].blocks:
                occupancies.append(b.occupied)
            self.signals.callOccSend(occupancies)
            occflag = False

class Testbench(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400,400)
        self.move(1500,0)
        self.setWindowTitle("Track Model Testbench")

        occupybutton = QPushButton("Switch occupancy", self)
        occupybutton.move(100,50)
        occupybutton.clicked.connect(self.switchOccupancy)

        switchbutton = QPushButton("Flip switch", self)
        switchbutton.move(100,75)
        switchbutton.clicked.connect(self.flipSwitch)

        crossingbutton = QPushButton("Change crossing", self)
        crossingbutton.move(100,100)
        crossingbutton.clicked.connect(self.flipCrossing)
        
        param1=QLabel("Line number",self)
        param1.move(100,175)
        self.input1 = QLineEdit(self)
        self.input1.move(100,200)

        param2=QLabel("Component number",self)
        param2.move(100,250)
        self.input2 = QLineEdit(self)
        self.input2.move(100,275)

    def switchOccupancy(self):
        line = int(self.input1.text())
        comp = int(self.input2.text())
        if(comp<len(lines[line].blocks)):
            lines[line].blocks[comp].switchOccupancy()

    def flipSwitch(self):
        line = int(self.input1.text())
        comp = int(self.input2.text())
        if(comp<len(lines[line].switches)):
            lines[line].switches[comp].switch()

    def flipCrossing(self):
        line = int(self.input1.text())
        comp = int(self.input2.text())
        if(comp<len(lines[line].crossings)):
            lines[line].crossings[comp].f()

# MAIN BRANCH

def main():
    app=QApplication(sys.argv)
    trackmap=Map()
    testbench=Testbench()
    trackmap.show()
    testbench.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()