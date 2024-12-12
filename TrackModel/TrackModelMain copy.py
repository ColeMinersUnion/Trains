import sys
import time
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QSlider, QApplication, QFileDialog
from PyQt6.QtGui import QTransform, QPixmap
from PyQt6.QtCore import Qt,QTimer,QObject, pyqtSignal, pyqtSlot
import pandas as pd #reading the excel file
from math import atan2,pi,sqrt,pow,sin,cos

#offsets are multiplied by scl
XOFFSET = 0 #x-offset for track graphics
YOFFSET = 3 #y-offset for track graphics
SCL=25 #scale, length of blockthat is 1 wide in the file coordinate system
occflag = True #whether occupancy must be updated from another change
linenames=["Green","Red"] #default line names
lines=[] #default lines, will be instantiated and built later
switchid=[0,0] #track switch numbers for pinging
crossingid=[0,0] #track crossing numbers for pinging
signalid=[0,0] #signal numbers for pinging
stationid=[0,0] #station numbers for pinging
failmode = 0 #starting fail mode for setting failures; no failure
failnames = ["No","Rail","Circuit","Power"] # failure names
heaters = False #program starts with heaters off
speed = 1 #speed of simulation
fileselected = False #determine if an appropriate file has been selected
class Block: #block class
    #instantiation
    def __init__(self, linenum, section, number, length, grade, speed, twoway, elevation, underground,x1,y1,x2,y2):
        self.linenum = linenum #index in lines of the Line object that block belongs to
        self.section = section
        self.number = number #block number
        self.length = length
        self.grade = grade
        self.speed = speed
        self.twoway = twoway
        self.elevation = elevation #cumulative elevation
        self.underground = underground #whether it it udnerground
        self.x=x1 #start x coordinate
        self.y=y1 #start y coordinate
        self._occupied = False
        self.center = [(x1+x2)/2,(y1+y2)/2] #center for front end
        self.mag = sqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1))) #magnitude for front end
        self.angle = atan2((y2-y1),(x2-x1))*180/pi #angle for front end
        self.failure=0 #failure type
        self.authority = True #whether the block has authority
        if(self.angle<0):
            self.angle = self.angle+360 #normalize angle for front end
        r = linenames[linenum] + " Line"
        r = r + "\nSection " + section
        r = r + "\nBlock " + str(number)
        r = r + "\n" + str(round(length*3.28084)) + " feet long\n"
        r = r + str(grade) + "% grade\n"
        r = r + str(round(speed*0.621371)) + " mph speed limit"
        r = r + "\nBidirectional: " + str(twoway)
        r = r + "\nUnderground: " + str(underground) 
        r = r + "\nOccupied: "
        self.msg = r # r gathers object data and attaches it to self.msg   

    @property
    def occupied(self):
        return self._occupied
    
    @occupied.setter #triggers onOccChange to make occflag true when occupancy is changed
    def occupied(self,newocc):
        self._occupied = newocc
        self.onOccChange()

    def onOccChange(self): #makes occupancy true
        global occflag
        print("Occupancy change detected! " + str(self.number) + " is " + str(self.occupied))
        occflag = True    

    def toString(self): #displays string with current information
        return self.msg + str(self.occupied) + "\nAuthority: " + str(self.authority) + "\nFailure: " + failnames[self.failure] 
    
    def switchOccupancy(self): #switches occupancy
        self.occupied = not self.occupied

    def setAuth(self,auth): #sets authority
        self.authority = auth
class Switch:
#note, structuring switch depends on section, include that?)
    #instantiation
    #note, no three way switches; think V, not Δ
    def __init__(self,linenum,blocks):
        global lines
        self.linenum = linenum #index in lines of Line object it belongs to
        self.blocks = blocks
        self.switchid = switchid[linenum] #identifies switch in line
        switchid[linenum] = switchid[linenum]+1 #gets id for next switch
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
        self.linenum = linenum #index in lines of Line object it belongs to
        self.block = block
        self.on = False
        self.crossingid = crossingid[linenum] #gives id in line
        crossingid[linenum] = crossingid[linenum]+1 #gets next id
        self.msg = "Crossing (" + linenames[linenum] + " Line, Block " + str(block) + ")\nClosed: "
    def toString(self):
        return self.msg + str(self.on) #message to display on hover

    #change state of crossing
    def switch(self):
        self.on = not self.on

class Signal:
    #instantiation
    def __init__(self,linenum,block):
        self.linenum = linenum #index in lines of Line object it belongs to
        self.block = block
        self.on = False
        self.signalid = signalid[linenum] #gives id in line
        signalid[linenum] = signalid[linenum]+1 #gets next id
        self.msg = "Signal (" + linenames[linenum] + " Line, Block " + str(block) + ")\nGo: "
    def toString(self):
        return self.msg + str(self.on) #message to display on hover

    #change state of crossing
    def switch(self):
        self.on = not self.on
class Transponder:
    #instantiation
    def __init__(self,linenum,block,data):
        self.linenum = linenum #index in lines of Line object it belongs to
        self.block = block 
        self.data = data #data in beacon
        self.msg = "Beacon (" + linenames[linenum] + " Line, Block " + str(block) + ")\n" + data #message to display on hover
class Station: #yard also
    #instantiation
    def __init__(self,linenum,block,name,side):
        self.linenum = linenum #index in lines of Line object it belongs to
        self.block = block #block the station is on
        self.name = name
        self.side = side #which doors the train needs to open
        self.msg = "" 
        self.stationid=stationid[linenum] #id for station in line
        stationid[linenum]=stationid[linenum]+1 #get next id

        if(name=="YARD"): #message for yard 
            self.passengers = 0  
            self.msg = "YARD"
        else: #message for normal stations
            self.passengers = 10
            self.msg = "Station " + str(name) + "\nSide " + str(side) + "\n" + linenames[linenum] + " Line, Block " + str(block)

    def toString(self):
        return self.msg + "\n" + str(self.passengers) + " people waiting" 

class Line:
    def __init__(self,linenum):
        self.linenum = linenum #index in lines
        self.blocks = []
        self.switches = []
        self.crossings = []
        self.signals = [] #signal lights, not to be confused with pyqtSignals
        self.transponders = [] #AKA beacons
        self.stations = []
        self.trains = []

    def beaconByBlock(self,block): #called beacon so other people understand, returns beacon data at block
        for x in self.transponders:
            if (x.block==block):
                return x.data
        return None

    def getSwitch(self,block): #gets id of switch at block
        for x in self.switches:
            if x.hasBlock(block):
                return x.switchid
        return None
            
    def getCrossing(self,block): #gets id of crossing at block
        for x in self.crossings:
            if (x.block==block):
                return x.crossingid
        return None
    
    def getSignal(self,block): #gets id of crossing at block
        for x in self.Signal:
            if (x.block==block):
                return x.signalid
        return None
    
    def stationByBlock(self,block): #gets id of station at block
        for x in self.stations:
            if (x.block==block):
                return x.stationid
        return None
    
    def stationByName(self,name): #gets name of station at block
        for x in self.stations:
            if (x.name==name):
                return x.stationid
        return None

def readX(string): #return true if X, used for reading booleans in Excel files
    return (string=="X")

def readFiles(filenames): #read multiple files
    global linenames, lines, switchid, crossingid, signalid, stationid, passive, active

    #reset model
    linenames=["Green","Red"] #default line names
    lines=[Line(0),Line(1)] #default lines, will be instantiated and built later
    switchid=[0,0] #track switch numbers for pinging
    crossingid=[0,0] #track crossing numbers for pinging
    signalid=[0,0] #signal numbers for pinging
    stationid=[0,0] #station numbers for pinging
    active = [] #taken from Excel file

    for f in filenames:
        read(f)
    return


def read(file):
    data=pd.read_excel(file,engine='openpyxl')       
    tempswitch=[] #instantiate switches last to make sure everything is there
    i=1 #for loop doesnt work idk why
    while(i<len(data.index)): #go through all blocks/rows
        linename=data.iat[i,0] #get first line
        linenum=len(linenames)
        if linename in linenames: #if linename already added
            linenum= linenames.index(linename) #get line if already in
        else: #if linename not added, then add it
            linenames.append(linename)
            lines.append(Line(linenum))
            crossingid.append(0)
            switchid.append(0)
            stationid.append(0)
            signalid.append(0)
        while len(lines[linenum].blocks) <= data.iat[i,2]: #add values to list to fit block until right number found
            lines[linenum].blocks.append(None) 
        lines[linenum].blocks[data.iat[i,2]]=Block(linenum,
                                                data.iat[i,1], #section
                                                data.iat[i,2], #block
                                                data.iat[i,3], #length
                                                data.iat[i,4], #grade
                                                data.iat[i,5], #speed
                                                readX(data.iat[i,6]), #2-way
                                                data.iat[i,7], #elevation
                                                readX(data.iat[i,8]), #undeground
                                                XOFFSET+data.iat[i,16], #x1-coord
                                                YOFFSET+data.iat[i,17], #y1-coord
                                                XOFFSET+data.iat[i,18], #x2-coord
                                                YOFFSET+data.iat[i,19]) #y2-coord
        if(not (pd.isnull(data.iat[i,9]) or pd.isnull(data.iat[i,10]))): #start building switch if switch vertex at block
            tempswitch.append([linenum,data.iat[i,2],data.iat[i,9],data.iat[i,10]])
        if(not pd.isnull(data.iat[i,11])): #add beacon if at block
            lines[linenum].transponders.append(Transponder(linenum,data.iat[i,2],data.iat[i,11]))
        if(not pd.isnull(data.iat[i,12])): #add station if at block
            lines[linenum].stations.append(Station(linenum,data.iat[i,2],data.iat[i,12],data.iat[i,13]))
        if(readX(data.iat[i,14])): #add crosing if at block
            lines[linenum].crossings.append(Crossing(linenum,data.iat[i,2]))
        if(readX(data.iat[i,15])): #add signal if at block
            lines[linenum].signals.append(Signal(linenum,data.iat[i,2]))
        i=i+1 #increment
    for s in tempswitch: #add switches now, blocks should update
        lines[s[0]].switches.append(Switch(s[0],[s[1],s[2],s[3]])) #add switch to appropriate line number
    return
class SignalHandler(QObject): #handles signals from other modules

    sendOccupancies = pyqtSignal(list) #to send occupancies to track controller
    sendAuthorities = pyqtSignal(list) #to send authorities to train model
    sendPassengers = pyqtSignal(list) #to send station block and passengers to train model
    sendBeacon = pyqtSignal(list) #to send beacon block and data to train model

    def __init__(self):
        super().__init__()

    def callOccSend(self, occupancies: list): #lets other classes properly send occupancies
        self.sendOccupancies.emit(occupancies)

    def callAuthSend(self): # call to send authorities to train
        authorities=[]
        for b in lines[0].blocks: #gather authorities
            authorities.append(b.authority) 
        self.sendAuthorities.emit(authorities)
        print("Sending authority")
        print(authorities)

    @pyqtSlot(list) #expecting block and number of passengers
    def getPassengers(self,message):
        stationid=lines[0].stationByBlock(message[0]) #get id of station at block and passengers disembarking
        waiting = lines[0].stations[stationid].passengers #get # of passengers waiting
        boarding = waiting - 2 if (waiting>2) else 0 # assume 2 people get off
        self.sendPassengers.emit([message[0],boarding]) #send block and # of boarding passenegrs to train model
        lines[0].stations[stationid].passengers = waiting - boarding + message[1] #find new number of passengers

    @pyqtSlot(int) #expecting block number
    def getBeacon(self,message):
        data = lines[0].beaconByBlock(message) #get data of beacon at block
        if(data!=None): #if data exists, send
            self.sendBeacon.emit([data,message])

    @pyqtSlot(int)
    def toggleOcc(self,message): #toggle occupancy of block
        lines[0].blocks[message].switchOccupancy()
        if(lines[0].blocks[message].occupied): #check if new block occupied
            self.sendBeacon.emit([message,lines[0].beaconByBlock(message)])

    @pyqtSlot(list)
    def getHardwareAuthority(self,message): #get authorities from hardware track controller
        global lines
        print("hardware authority received")
        print(message)
        for i in range(len(lines[0].blocks)): #make list with authorities from HW's ranges, [41,76] for green
            if(i>40 and i<69):
                lines[0].blocks[i].setAuth(message[i])
                print(str(i) + " " + str(message[i]) + " " + str(lines[0].blocks[i].authority))
        self.callAuthSend()

    @pyqtSlot(list)
    def getSoftwareAuthority(self,message): #get authorities from software track controller
        global lines
        print("software authority received")
        print(message)
        for i in range(len(lines[0].blocks)): #make list with authorities from SW's ranges, [1,40] and [77,151] for green
            if(i<41 or i>68):
                lines[0].blocks[i].setAuth(message[i])
                print(str(i) + " " + str(message[i]) + " " + str(lines[0].blocks[i].authority))
        self.callAuthSend()

    # Switch signals

    @pyqtSlot(bool)
    def getSwitch13(self,message): #get green line switch 13 state from track controller and implement on track model
        lines[0].switches[0].setToLeft(message) 

    @pyqtSlot(bool)
    def getSwitch28(self,message): #get green line switch 28 state from track controller and implement on track model
        lines[0].switches[1].setToLeft(not message) 

    @pyqtSlot(bool)
    def getSwitch58(self,message): #get green line switch 58 state from track controller and implement on track model
        lines[0].switches[2].setToLeft(message)

    @pyqtSlot(bool)
    def getSwitch62(self,message): #get green line switch 62 state from track controller and implement on track model
        lines[0].switches[3].setToLeft(message)

    @pyqtSlot(bool)
    def getSwitch77(self,message): #get green line switch 77 state from track controller and implement on track model
        lines[0].switches[4].setToLeft(not message)

    @pyqtSlot(bool)
    def getSwitch85(self,message): #get green line switch 85 state from track controller and implement on track model    
        lines[0].switches[5].setToLeft(message)

    # Signal light signals

    @pyqtSlot(bool)
    def getSignal13(self,message): #get green line signals 13 state from track controller and implement on track model
        lines[0].signals[0].on=message 

    @pyqtSlot(bool)
    def getSignal28(self,message): #get green line signals 28 state from track controller and implement on track model
        lines[0].signals[1].on=message

    @pyqtSlot(bool)
    def getSignal58(self,message): #get green line signals 58 state from track controller and implement on track model
        lines[0].signals[2].on=message

    @pyqtSlot(bool)
    def getSignal62(self,message): #get green line signals 62 state from track controller and implement on track model
        lines[0].signals[3].on=message

    @pyqtSlot(bool)
    def getSignal77(self,message): #get green line signals 77 state from track controller and implement on track model
        lines[0].signals[4].on=message

    @pyqtSlot(bool)
    def getSignal85(self,message): #get green line signals 85 state from track controller and implement on track model    
        lines[0].signals[5].on=message
    
    # Crossing signals

    @pyqtSlot(bool)
    def getCrossing19(self,message): #get green line crossing 19 state from track controller and implement on track model
        lines[0].crossings[0].on=message #crossing 19

    @pyqtSlot(bool)
    def getCrossing108(self,message): #get green line crossing 108 state from track controller and implement on track model
        lines[0].crossings[1].on=message #crossing 108    

# FRONT END BRANCH

passive = [] #no update method, do not react to backend changes
active = [] #update method, react to backend changes
#the below label styles are only used for widgets assigned transparent backgrounds in PyQT
labelstyle = """QLabel {
                background-color: transparent
                }""" #CSS style for labels
tooltipstyle = """QToolTip { 
                background-color: lightgray; 
                color: white; 
                border: white solid 1px
                }""" #CSS style for tool tips

def offset(angle): #correct offset for blocks depending on angle; PyQT distorts the location of objects when rotating
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
class SpeedMeter(QWidget): #defunct, used for setting speed of ten baud model before integration
    def __init__(self,window):
        global speed
        super().__init__()  
        self.slider = QSlider(Qt.Orientation.Horizontal, window) #slider itself
        self.slider.setGeometry(750,0,180,45) 
        #these are not the maximum and minimum values for speed, these are determined in the update method
        self.slider.setMinimum(-100)
        self.slider.setMaximum(200)
        self.slider.valueChanged.connect(self.update)
        
        self.number = QLabel(window) #slider setting display
        self.number.move(930,0) #put adjacent to slider
        self.slider.setValue(0)
        self.number.setText(str(speed) + "x")


    def update(self): #update slider
        global speed
        temp=self.slider.value() #get value in slider object
        speed=float(int(10*pow(10,temp/100))/10) #get speed from sldier value
        self.number.setText(str(speed) + "x") #adjust display text
        self.number.adjustSize() #change display position so number fits next to slider

class HeaterSystem(QWidget):
    def __init__(self,window):
        super().__init__()
        self.temp=70 #temperature to be set by slider
        self.label = QLabel(window)
        self.label.move(405,0)
        self.label.setToolTip("Track heaters off")
        pixmap = QPixmap('TrackModel/Icons/OffHeater.png')
        self.label.setPixmap(pixmap)
        
        self.slider = QSlider(Qt.Orientation.Horizontal, window) #temperature slider
        self.slider.setGeometry(450,0,180,45)
        #temperature from 0 to 100 degrees Fahrenheit
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.valueChanged.connect(self.update) #update when value changes
        
        self.number = QLabel(window) #temperature number display
        self.number.move(630,0)
        self.number.setText(str(self.temp) + " °F")

        self.slider.setValue(self.temp)

    def update(self): #update display
        global heaters
        self.temp=self.slider.value()
        self.number.setText(str(self.temp) + " °F")
        self.number.adjustSize()

        if((not heaters) and self.temp<=32): #turn heaters on if they need to be turned on
            self.label.setToolTip("Track heaters on") #off label
            heaters=True
            pixmap = QPixmap('TrackModel/Icons/OnHeater.png') #on icon
            self.label.setPixmap(pixmap)

        if(heaters and self.temp>32): #turn heaters off if they need to turn off
            self.label.setToolTip("Track heaters off")#off label
            heaters=False
            pixmap = QPixmap('TrackModel/Icons/OffHeater.png') #off icon
            self.label.setPixmap(pixmap)

class TrainOccupy(QWidget):
    def __init__(self,linenum,blocknum,window):
        global failmode
        super().__init__()
        self.linenum = linenum #index in lines of block object
        self.blocknum = blocknum #number of block it represents
        self.label = QLabel(window)
        self.center = lines[linenum].blocks[blocknum].center
        self.check=False #to check for changes to occupancy
        pixmap = QPixmap('TrackModel/Icons/TrainOccupy.png') #upload icon
        pixmap = pixmap.transformed(QTransform().scale(SCL/100,SCL/100)) #scale icon
        self.label.setPixmap(pixmap) #set image
        self.label.move(-100,-100) #move offscreen for no occupancy
        self.label.setToolTip("Occupied at \n" + linenames[linenum] + " Line, Block " + str(blocknum)) #display message
        self.label.setStyleSheet(labelstyle) #set style sheets
        self.setStyleSheet(tooltipstyle)
        self.update() #update for initial values

    def update(self):
        occ = lines[self.linenum].blocks[self.blocknum].occupied 
        if(self.check!=occ): #if occupancy doesnt match check
            if(occ): #move on screen if occupied
                self.label.move((int((self.center[0]-0.125)*SCL)),int((self.center[1]+0.175)*SCL))
            else: #move off screen otherwise
                self.label.move(-100,-100)
            self.label.show()  #show update
            self.check=occ #update check value


class Failure(QWidget):
    def __init__(self,linenum,blocknum,window):
        global failmode
        super().__init__()
        self.linenum = linenum #index in lines of block object
        self.blocknum = blocknum #number of block it represents
        self.label = QLabel(window)
        self.center = lines[linenum].blocks[blocknum].center #where to put failure whe on
        self.check=0 #assumed failmode to check by
        pixmap = QPixmap('TrackModel/Icons/RailFailure.png') #make initial pixmap
        self.label.setPixmap(pixmap) #set pixmap
        self.label.move(-100,-100) #move off screen for no failure
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.update() #update 
        
    def update(self): #check for update
        objfail = lines[self.linenum].blocks[self.blocknum].failure
        if(self.check!=objfail): #if object failure does not match 
            if(objfail==0): #if no failure, move off screen
                self.label.move(-100,-100)
            else: #update for a failure by changing icon and setting on screen
                pixmap = QPixmap('TrackModel/Icons/' + failnames[objfail] + 'Failure.png')
                pixmap = pixmap.transformed(QTransform().scale(SCL/100,SCL/100))
                self.label.setPixmap(pixmap)
                self.label.move((int((self.center[0]-0.125)*SCL)),int((self.center[1]-0.45)*SCL)) #move on screen
                self.label.setToolTip(failnames[objfail] + " Failure\n" + linenames[self.linenum] + " Line, Block " + str(self.blocknum)) #set new value on hover
            self.label.show()
            self.check=objfail #update check to not check again until another change

        

class FailureSelect(QWidget): #underline to show selected failure
    def __init__(self,window):
        super().__init__()
        self.label = QLabel(window)
        self.label.setPixmap(QPixmap('TrackModel/Icons/FailureSelect.png')) #underline icon
        self.label.move(-100,-100) #start offscreen
        self.check=0 #assume no failure
        self.update() #update for back end
    
    def update(self): #check for back end update
        if(self.check!=failmode): #if failmode changes
            self.label.move(180+failmode*45,50) #move to selected failure button
            self.check=failmode #set check to backend value

class FileSignal(QObject): #file button needs QObject to send signal
    signal = pyqtSignal(list)

class FileButton(QWidget): #button to select file
    def __init__(self,window):
        super().__init__()
        pixmap = QPixmap('TrackModel/Icons/SelectFile.png') #get icon from file
        self.label = QLabel(window) 
        self.label.setPixmap(pixmap)#set icon
        self.label.move(90,0) #move onto screen
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.label.setToolTip("Select File") #tells you what it does when you hover over it

        self.label.mousePressEvent = self.selectFile #select file when clicked
        self.fileSignal = FileSignal()

    def selectFile(self, message):
        global fileselected
        global lines
        filenames,_ = QFileDialog.getOpenFileNames(self, "Open File", "", "Excel Files (*.xlsx)") #open file select dialog
        if(filenames):
            print(filenames)
            print("emitting signal")
            self.fileSignal.signal.emit(filenames)

class FailureButton(QWidget): #button to select a failure, we make 3 of these
    def __init__(self,failnum,window): #button changes depending on what failure it represents
        super().__init__()
        self.failnum=failnum #representative fail number
        self.pixmap = QPixmap('TrackModel/Icons/' + failnames[failnum] + 'Failure.png')
        self.label = QLabel(window)
        self.label.setPixmap(self.pixmap) #set icon from file
        self.label.setToolTip(failnames[failnum] + " Failure")
        self.label.move(180+failnum*45,0) #move on screen
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.label.mousePressEvent = self.changeFailMode #change failure setting mode when clicked

    def changeFailMode(self,event): #change failure setting mode
        global failmode
        if (failmode==self.failnum): #deselect when already clicked
            failmode=0
        else:   
            failmode=self.failnum #select failnum when clicked


class BlockIcon(QWidget):
    def __init__(self,obj,window): #line number and block number
        super().__init__()
        global active
        self.window=window
        self.obj=obj
        pixmap = QPixmap('TrackModel/Icons/' + linenames[obj.linenum] + 'Arrow' + ('Bi' if (obj.twoway) else '') + '.png') #get right color and direction for block icon
        self.label=QLabel(window)
        pixmap = pixmap.transformed(QTransform().scale(obj.mag*SCL/100,SCL/50)) #stretch or squash block to fit length
        pixmap = pixmap.transformed(QTransform().rotate(self.obj.angle)) #rotate block to fit length
        self.label.setPixmap(pixmap)
        self.label.setToolTip(obj.toString()) #get string
        xoff = obj.mag*cos(obj.angle*pi/180)*offset(obj.angle+90) #determine x offset
        yoff = obj.mag*sin(obj.angle*pi/180)*offset(obj.angle) #determine y offset
        self.label.move(int((obj.x+xoff)*SCL),int((obj.y+yoff)*SCL)) #move onto screen
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.label.mousePressEvent = self.setFailure #set failure from failure select when clicked
        active.append(Failure(self.obj.linenum,self.obj.number,self.window)) #make failure icon for it
        active.append(TrainOccupy(self.obj.linenum,self.obj.number,self.window)) #make occupied icon for it

    def update(self): #when block needs updated
        self.label.setToolTip(self.obj.toString()) #make new string
        self.label.show() #show new label

    def setFailure(self,event): #set failure
        global failmode 
        objfail = lines[self.obj.linenum].blocks[self.obj.number].failure

        authority = lines[self.obj.linenum].blocks[self.obj.number].authority
        print(authority)

        if(objfail != failmode): #only update backend if new value
            lines[self.obj.linenum].blocks[self.obj.number].failure = failmode #change back end object
            lines[self.obj.linenum].blocks[self.obj.number].occupied = (failmode in [1,3]) #occupied if rail or power failure so no train goes there     

class SwitchIcon(QWidget):
    def __init__(self,obj,window):
        super().__init__()
        self.linenum=obj.linenum #index of lines to which line belongs
        self.switchid=obj.switchid #id of switch on line
        pixmap = QPixmap('TrackModel/Icons/OpenSwitch.png') #icon for open switch
        pixmap = pixmap.transformed(QTransform().scale(SCL/100,SCL/100)) #scale icon
        self.openlabel=QLabel(window)
        self.openlabel.setPixmap(pixmap)
        self.openlabel.setToolTip("Switched open") #label for open switch
        self.openlabel.setStyleSheet(labelstyle)
        pixmap = QPixmap('TrackModel/Icons/ClosedSwitch.png') #icon for closed switch
        pixmap = pixmap.transformed(QTransform().scale(SCL/100,SCL/100))
        self.closedlabel=QLabel(window)
        self.closedlabel.setPixmap(pixmap)
        self.closedlabel.setToolTip("Switched closed") #label for closed switch
        self.closedlabel.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.check=[0,0] #check values
        
    def update(self): #update switch statets
        global lines
        tempobj=lines[self.linenum].switches[self.switchid]
        opencenter=lines[tempobj.linenum].blocks[tempobj.getopen()].center #get center for checking
        if(self.check!=opencenter): #check with center because we use that value anyway
            closedcenter=lines[tempobj.linenum].blocks[tempobj.getclosed()].center
            self.openlabel.move(int((opencenter[0]-0.125)*SCL),int((opencenter[1]+0.225)*SCL)) #move open label to right spot
            self.closedlabel.move(int((closedcenter[0]-0.125)*SCL),int((closedcenter[1]+0.225)*SCL)) #move closed label to right spot
            self.openlabel.show()
            self.closedlabel.show()
            self.check=opencenter
    
class CrossingIcon(QWidget):
    def __init__(self,obj,window):
        super().__init__()
        self.linenum=obj.linenum #index of line object it belongs to
        self.crossingid=obj.crossingid #id of crossing
        self.label=QLabel(window)
        self.check=True
        center = lines[obj.linenum].blocks[obj.block].center #get center for locating on screen
        self.label.move(int((center[0]-0.25)*SCL),int((center[1]-0.225)*SCL))
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.update()

    def update(self): #update crossing icon for new backend value
        obj = lines[self.linenum].crossings[self.crossingid]
        if(self.check!=obj.on): #only change if new backend value
            if (obj.on): #change icon if on now
                self.pixmap = QPixmap('TrackModel/Icons/OnCrossing.png')
            else: #chane icon if off now
                self.pixmap = QPixmap('TrackModel/Icons/OffCrossing.png')
            self.check=obj.on #update with backend
            self.pixmap = self.pixmap.transformed(QTransform().scale(SCL/100,SCL/100))
            self.label.setPixmap(self.pixmap)
            self.label.setToolTip(obj.toString())
            self.label.show()

class SignalIcon(QWidget):
    def __init__(self,obj,window):
        super().__init__()
        self.linenum=obj.linenum #index of line object it belongs to
        self.signalid=obj.signalid #id of signal
        self.label=QLabel(window)
        self.check=True
        center = lines[obj.linenum].blocks[obj.block].center #get center for locating on screen
        self.label.move(int((center[0]-0.25)*SCL),int((center[1]-0.225)*SCL))
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.update()

    def update(self): #update signal icon for new backend value
        obj = lines[self.linenum].signals[self.signalid]
        if(self.check!=obj.on): #only change if new backend value
            if (obj.on): #change icon if on now
                self.pixmap = QPixmap('TrackModel/Icons/OnSignal.png')
            else: #chane icon if off now
                self.pixmap = QPixmap('TrackModel/Icons/OffSignal.png')
            self.check=obj.on #update with backend
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

    def update(self): #I do this so I can classify transponder as active so i can reset it
        return

class StationIcon(QWidget):
    def __init__(self,obj,window):
        super().__init__()
        self.linenum=obj.linenum
        self.stationid=obj.stationid
        self.check=obj.passengers #front end check
        if(obj.name=="Yard" or obj.name=="YARD"): #set yard icon
            pixmap = QPixmap('TrackModel/Icons/Yard.png')
        else: #set station icon
            pixmap = QPixmap('TrackModel/Icons/Station.png')
        self.label=QLabel(window)
        pixmap = pixmap.transformed(QTransform().scale(SCL/100,SCL/100)) #scale icon
        self.label.setPixmap(pixmap)
        self.label.setToolTip(obj.toString()) #no toString, station message is static
        center = lines[obj.linenum].blocks[obj.block].center
        self.label.move(int((center[0]-0.05)*SCL),int((center[1]-0.125)*SCL)) #move icon
        self.label.setStyleSheet(labelstyle)
        self.setStyleSheet(tooltipstyle)
        self.update() #update form backend value

    def update(self): #update form backend value
        obj = lines[self.linenum].stations[self.stationid] #check current passengers
        if(self.check!=obj.passengers): #if passenger change
            self.check=obj.passengers #set new passengers
            self.label.setToolTip(obj.toString()) #show new string on hover
            self.label.show()

class Map(QWidget): #displays map
    def __init__(self):
        super().__init__()
        self.resize(1080,1080) #sets window size
        self.move(0,0)
        self.setWindowTitle("Track Model Map") #window title
        self.setStyleSheet("background-color: lightyellow;") #light yellow background
        self.signals = SignalHandler()
        fb = FileButton(self)
        fb.fileSignal.signal.connect(self.renderGraphics)
        passive.append(fb) #add file select button
        passive.append(HeaterSystem(self)) #add heater setup
        for i in range(4): #there are four failure buttons, the objects handle what they do
            passive.append(FailureButton((i),self)) #add failure buttons
        active.append(FailureSelect(self)) #this goes after the dynamic icons, we hide them behind this widget system
        
        #active.append(SpeedMeter(self)) #adds speed meter
        self.timer=QTimer() #timer for active components
        self.timer.timeout.connect(self.update) #connect timer to update method
        self.timer.start(int(1000/60)) #set clock speed of timer

        self.tenBaud=QTimer() #timer for active components
        self.tenBaud.timeout.connect(self.tenBaudClock) #connect timer to update method
        self.tenBaud.start(1) #set clock speed of timer

        self.renderGraphics(["TrackModel/Red Line.xlsx","TrackModel/Green Line.xlsx"]) #read red and green lines

    def renderGraphics(self,filenames):
        print("signal received")
        global lines, active
        active.clear() #remove active components
        oldstuff = self.children()[9:] #all these widgets are made with the file select
        for o in oldstuff:
            o.deleteLater()

        readFiles(filenames)
        for line in lines: #adds components tied to every line object
            for block in line.blocks: #adds all blocks
                active.append(BlockIcon(block,self)) #updates for view
            for switch in line.switches: #biggest components to smallest so all can be hovered
                active.append(SwitchIcon(switch,self)) 
            for crossing in line.crossings: #adds all crossings
                active.append(CrossingIcon(crossing,self))
            for signal in line.signals: #adds all signals
                active.append(SignalIcon(signal,self))
            print("these arent shown???")
            for transponder in line.transponders: #adds all beacons
                active.append(TransponderIcon(transponder,self))  
            for station in line.stations: #adds all stations
                active.append(StationIcon(station,self))
        print("graphics rendered")
        print(len(active))
        self.update()
        self.show()

    def tenBaudClock(self): #clock for 10 baud messages
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
    
    def update(self): #update components on screen
        global occflag
        for a in active:
            a.update() #update every active component
        if(occflag): #if occupancy change detected
            occupancies=[] #reset sent occupancies
            for b in lines[0].blocks: #make new occupancy list
                occupancies.append(b.occupied)
            self.signals.callOccSend(occupancies) #send occupancy list
            occflag = False #turn off occupancy change flag now that they are sent

class Testbench(QWidget): #testbench window
    def __init__(self):
        super().__init__()
        self.resize(400,400) #window size
        self.move(1500,0)
        self.setWindowTitle("Track Model Testbench")
        self.cyclenum = 0 #cycle number for full test, it has 8 tests

        #make, move and connect full test button
        testbutton = QPushButton("Full test cycle (click to cycle)",self)
        testbutton.move(100,25)
        testbutton.clicked.connect(self.test)

        #make, move and connect occupancy test button
        occupybutton = QPushButton("Switch occupancy", self)
        occupybutton.move(100,50)
        occupybutton.clicked.connect(self.switchOccupancy)

        #make, move and connect switch flip button
        switchbutton = QPushButton("Flip switch", self)
        switchbutton.move(100,75)
        switchbutton.clicked.connect(self.flipSwitch)

        #make, move and connect change crossing button
        crossingbutton = QPushButton("Change crossing", self)
        crossingbutton.move(100,100)
        crossingbutton.clicked.connect(self.flipCrossing)

        #make, move and connect change signal button
        signalbutton = QPushButton("Change signal", self)
        signalbutton.move(100,125)
        signalbutton.clicked.connect(self.flipSignal)
        
        #line number input
        param1=QLabel("Line number",self)
        param1.move(100,175)
        self.input1 = QLineEdit(self)
        self.input1.move(100,200)

        #switch/crossing/signal id input
        param2=QLabel("Component ID",self)
        param2.move(100,250)
        self.input2 = QLineEdit(self)
        self.input2.move(100,275)

    def test(self): #full test
        #0: Power failure on all blocks
        #1: Circuit failure on all blocks
        #2: Rail failure on all blocks
        #3: No failure on all blocks
        #4: True occupancy for all blocks
        #5: False occupancy for all blocks
        #6: Toggle crossings, switches, and signals for all blocks
        #7: Toggle crossings, switches, and signals again for all blocks
        #resets to 0 after test 7
        global lines
        if(self.cyclenum<4): #tests 0-3 for failure
            for l in range(len(lines)):
                for b in range(len(lines[l].blocks)):
                    lines[l].blocks[b].failure = 3-self.cyclenum
            print(failnames[3-self.cyclenum] + " Failure complete! Please hover over the blocks to check their status")
        elif(self.cyclenum<6): #tests 4-5 for occupancy
            for l in range(len(lines)):
                for b in range(len(lines[l].blocks)):
                    lines[l].blocks[b].occupied = (self.cyclenum==4)
            print(str((self.cyclenum==4)) + " Occupancy complete! Please hover over the blocks to check their status")
        elif(self.cyclenum<8): #tests 6-7 for crossings, switches, and signals
            for l in range(len(lines)): #go through all lines
                for s in range(len(lines[l].switches)): #for all switches
                    lines[l].switches[s].switch()#flip switch
                for c in range(len(lines[l].crossings)):#for all crossings
                    lines[l].crossings[c].switch()#flip crossing
                for s in range(len(lines[l].signals)):#for all signals
                    lines[l].signals[c].switch()#flip signal
            print("Switches, crossings, and signals toggled! Please hover over the blocks to check their status")
        self.cyclenum=self.cyclenum+1 #reset cycle
        if(self.cyclenum==8):
            self.cyclenum=0
                    

    
    def switchOccupancy(self): #switch occupancy button result
        line = int(self.input1.text()) #get right line
        comp = int(self.input2.text()) #get right component
        if(comp<len(lines[line].blocks)): #find matching component
            lines[line].blocks[comp].switchOccupancy() #execute command

    def flipSwitch(self): #switch flip button result
        line = int(self.input1.text())
        comp = int(self.input2.text())
        if(comp<len(lines[line].switches)):
            lines[line].switches[comp].switch()

    def flipCrossing(self): #crossing flip button result
        line = int(self.input1.text())
        comp = int(self.input2.text())
        if(comp<len(lines[line].crossings)):
            lines[line].crossings[comp].switch()

    def flipSignal(self): #signal flip button result
        line = int(self.input1.text())
        comp = int(self.input2.text())
        if(comp<len(lines[line].signals)):
            lines[line].signals[comp].switch()

# MAIN BRANCH

def main():
    app=QApplication(sys.argv)
    trackmap=Map() #make map object
    testbench=Testbench() #make testbench object
    trackmap.show() #show map
    testbench.show() #show testbench
    sys.exit(app.exec()) #allows exiting
    print("Finished main") #confirm completion of main

if __name__ == "__main__":
    main() #execute main if run from this file
