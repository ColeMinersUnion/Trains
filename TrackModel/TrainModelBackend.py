#do components get assigned with the block object or separately with a different block number
#how do we know when the circuits get turned on
#track model needs to keep track of train

from enum import Enum
#failure class
Failure = Enum('Failure',['Rail','Circuit','Power']) 

#line class, will hold all components
class Line:
    def __init__(self,blocks,switches,crossings,transponders,stations):
        self.blocks = []
        self.switches = []
        self.crossings = []
        self.transponders = []
        self.stations = []

    #methods for adding components


#block class
class Block:
    #instantiation
    def __init__(self, section, number, length, grade, speed, elevation, underground, left, right):
        self.section = section
        self.number = number
        self.length = length
        self.grade = grade
        self.speed = speed
        self.elevation = elevation
        self.underground = underground
        self.circuit = False
        self.heater = False
        self.left = 0
        self.right = 0
    
#switch class (note, structuring switch depends on section, include that?)
class Switch:
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
    def hasblock(self,block):
        ret = False
        for blockToCheck in self.blocks:
            ret = ret or (blockToCheck==block)
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

#crossing class
class Crossing:
    #instantiation
    def __init__(self,block,time):
        self.block = block
        self.on = True
        self.time = time

    #change state of crossing
    def switch(self):
        on = not on

#transponder class

#station class 
class Station:
    def __init__(self,number,name):
        self.number = number
        self.name = name