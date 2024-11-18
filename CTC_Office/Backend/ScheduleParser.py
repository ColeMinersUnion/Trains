import pandas as pd #!to read in the track data
import os #!To check the file stuff
import math

#returns a list of stations for each train. 
#Dict [{Line: line, station: [stations]}]
def readSchedule(fn: str = "") -> list:
    
