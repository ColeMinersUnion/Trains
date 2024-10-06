import pandas as pd #reading the excel file
from enum import Enum
Failure = Enum('Failure',['Rail','Circuit','Power'])

linenames=[]
lines=[]
CLOCK_TIME = 1/60

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
        self.circuit = False
        self.heater = False
        self.prev = number-1 #will change with crossing instantiation
        self.next = number+1 #will change with crossing instantiation

    def center(self):
        return [(self.x1+self.x2)/2,(self.y1+self.y2)/2]

class Switch:
#note, structuring switch depends on section, include that?)
    #instantiation
    #note, no three way switches; think V, not Δ
    def __init__(self,linenum,blocks):
        self.linenum = linenum
        self.blocks = blocks
        self.lights = [True, False] #the first block is the central
        self.updateEnds()

    def updateEnds(self):
        if(self.lights[1]==True): #connect 0 to 1
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
        self.lights[0] = not self.lights[0]
        self.lights[1] = not self.lights[1]
        self.updateEnds()

    #stop a specific direction
    def stop(self,stopblock):
        for i in [1,2]:
            if (self.blocks[i]==stopblock and self.lights[i]==True):
                self.switch()
                break
        self.updateEnds()

    #make a specific direction have green
    def go(self,goblock):
        for i in [1,2]:
            if (self.blocks[i]==goblock and self.lights[i]==False):
                self.switch()
                break
        self.updateEnds()
class Crossing:
    #instantiation
    def __init__(self,linenum,block):
        self.linenum = linenum
        self.block = block
        self.on = True

    #change state of crossing
    def switch(self):
        on = not on
class Transponder:
    #instantiation
    def __init__(self,linenum,block):
        self.linenum = linenum
        self.block = block 
        self.data = ""
class Station:
    #instantiation
    def __init__(self,linenum,block,name,side):
        self.linenum = linenum
        self.block = block
        self.name = name
        self.side = side
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
    
class Line:
    def __init__(self,linenum):
        self.linenum = linenum
        self.blocks = []
        self.switches = []
        self.crossings = []
        self.transponders = []
        self.stations = []


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
    i=2 #for loop doesnt work idk why
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
        if(readX(data.iat[i,11])):
            lines[linenum].transponders.append(Transponder(linenum,data.iat[i,2]))
        if(data.iat[i,12]!=""):
            lines[linenum].stations.append(Station(linenum,data.iat[i,2],data.iat[i,12],data.iat[i,13]))
        if(readX(data.iat[i,14])):
            lines[linenum].crossings.append(Crossing(linenum,data.iat[i,2]))
        i=i+1 #increment
    for s in tempswitch: #add switches now, blocks should update
        lines[s[0]].switches.append(Switch(s[0],[s[1],s[2],s[3]])) #add switch to appropriate line number
    return
