import pandas as pd #reading the excel file
from enum import Enum
from math import atan2,pi,sqrt

linenames=[]
lines=[] 
switchid=[] #track switch numbers for pinging
crossingid=[] #track crossing numbers for pinging
crossingid=[]
CLOCK_TIME = 1/60
failmode = 0
failnames = ["None","Rail","Circuit","Power"]
modelspeed = 10

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
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
        self.occupied = False
        self.prev = number-1 #will change with crossing instantiation
        self.next = number+1 #will change with crossing instantiation
        self.center = [(x1+x2)/2,(y1+y2)/2] #center for front end
        self.mag = sqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1))) #magnitude for front end
        self.angle = atan2((y2-y1),(x2-x1))*180/pi #angle for front end
        self.failure=0 
        if(self.angle<0):
            self.angle = self.angle+360
        r = linenames[linenum] + " Line"
        r = r + "\nSection " + section
        r = r + "\nBlock " + str(number)
        r = r + "\n" + str(round(length*3.28084)) + " feet long\n"
        r = r + str(grade) + "% grade\n"
        r = r + str(round(speed*0.621371)) + " mph speed limit\n"
        r = r + "Elevation of " + str(round(elevation*3.28084)) + " feet"
        r = r + "\nBidirectional: " + str(twoway)
        r = r + "\nUnderground: " + str(underground) 
        r = r + "\nOccupied: "
        self.msg = r    

    def toString(self):
        return self.msg + str(self.occupied) + "\nFailure: " + failnames[self.failure]
    
    def switchOccupancy(self):
        self.occupied = not self.occupied
class Switch:
#note, structuring switch depends on section, include that?)
    #instantiation
    #note, no three way switches; think V, not Δ
    def __init__(self,linenum,blocks):
        self.linenum = linenum
        self.blocks = blocks
        self.switchid = switchid[linenum]
        switchid[linenum] = switchid[linenum]+1
        self.leftside=True #the first block is the central
        self.updateEnds()

    def updateEnds(self):
        if(self.leftside): #connect 0 to 1
            lines[self.linenum].blocks[self.blocks[0]].next = self.blocks[1]
            lines[self.linenum].blocks[self.blocks[1]].prev = self.blocks[0]
            lines[self.linenum].blocks[self.blocks[2]].prev = None
        else: #connect 0 to 2
            lines[self.linenum].blocks[self.blocks[0]].next = self.blocks[2]
            lines[self.linenum].blocks[self.blocks[2]].prev = self.blocks[0]
            lines[self.linenum].blocks[self.blocks[1]].prev = None 

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
        self.updateEnds()
        print("Updated switch\n")

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
        self.msg = "Crossing (" + linenames[linenum] + " Line, Block " + str(block) + ")\n Closed: "
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
        if(name=="YARD"):  
            self.msg = "YARD"
        else:
            self.msg = "Station " + str(name) + "\nSide " + str(side) + "\n" + linenames[linenum] + " Line, Block " + str(block)

class Train:
    def __init__(self,linenum,block1,length):
        self.linenum = linenum
        self.block1 = block1
        self.block2 = block1 #train can occupy multiple blocks
        self.length=length
        self.velocity = 0
        self.pos = 0
        self.authority = 0
        self.goingUp = True #direction depending if it crosses segment in ascending or descending block order
        self.msgqueue = []
        self.tenbaud = [False,False,False,False,False,False,False,False,False,False]

    def newPos(self):
        pos += self.velocity * CLOCK_TIME
        if pos>(lines[self.linenum].blocks(self.block1).length):
            pos -= self.block.length
            if(self.goingUp):
                self.block1=lines[self.linenum].blocks(self.block1).next
            else:
                self.block1=lines[self.linenum].blocks(self.block1).prev
        if pos>(lines[self.linenum].blocks(self.block1).length-self.length): 
            self.block2 = self.block1 #move train off old track if up far enough

    def getTransponder(self,block):
        for x in lines[self.linenum].transponders:
            if (x.block==block):
                return x.data
        return ""
    
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
        return False
            
    def getCrossing(self,block):
        for x in self.crossings:
            if (x.block==block):
                return x
        return False
    
    def stationByBlock(self,block):
        for x in self.stations:
            if (x.block==block):
                return x
        return False
    
    def stationByName(self,name):
        for x in self.stations:
            if (x.name==name):
                return name
        return False
    
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
                                                data.iat[i,15], #x1-coord
                                                data.iat[i,16], #y1-coord
                                                data.iat[i,17], #x2-coord
                                                data.iat[i,18]) #y2-coord
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
