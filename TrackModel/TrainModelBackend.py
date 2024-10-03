import pandas as pd #reading the excel file
import re #
from enum import Enum
Failure = Enum('Failure',['Rail','Circuit','Power'])

CLOCK_TIME = 1/60
class Block:
    #instantiation
    def __init__(self, section, number, length, grade, speed, elevation, underground, prev, next):
        self.section = section
        self.number = number
        self.length = length
        self.grade = grade
        self.speed = speed
        self.elevation = elevation
        self.underground = underground
        self.circuit = False
        self.heater = False
        self.prev = 0
        self.next = 0


class Switch:
#note, structuring switch depends on section, include that?)
    #instantiation
    #note, no three way switches; think V, not Δ
    def __init__(self,blocks,sections):
        self.blocks = blocks
        self.sections = sections
        self.lights = [True, True, False] #the first block is the central
    
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

    #check if it has a section
    def hasSection(self,section):
        ret = False
        for sectionToCheck in self.sections:
            ret = ret or (sectionToCheck==section)
        return ret
    
    #switch the switch
    def switch(self):
        self.lights[1] = not self.lights[1]
        self.lights[2] = not self.lights[2]

    #stop a specific direction
    def stop(self,stopsection):
        for i in [1,2]:
            if (self.blocks[i]==stopsection and self.lights[i]==True):
                self.switch()
                break

    #make a specific direction have green
    def go(self,gosection):
        for i in [1,2]:
            if (self.blocks[i]==gosection and self.lights[i]==False):
                self.switch()
                break
class Crossing:
    #instantiation
    def __init__(self,block,time):
        self.block = block
        self.on = True
        self.time = time

    #change state of crossing
    def switch(self):
        on = not on
class Transponder:
    #instantiation
    def __init__(self,name,section):
        self.name = name
        self.section = section 
class Station:
    #instantiation
    def __init__(self,number,section):
        self.number = number
        self.section = section

class Train:
    def __init__(self,block1,length):
        self.block1 = block1
        self.block2 = block1 #train can occupy multiple blocks
        self.length=length
        self.velocity = 0
        self.pos = 0
        self.goingUp = True #direction depending if it crosses segment in ascending or descending block order

    def newPos(self):
        pos += self.velocity * CLOCK_TIME
        if pos>(self.block.length):
            pos -= self.block.length
        if pos>(self.block.length-self.length): 
            self.block2 = self.block1 #move train off old track if up far enough
            
class Line:
    def __init__(self):
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

