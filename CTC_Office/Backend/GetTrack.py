import Graph #!to export the tracks
import pandas as pd #!to read in the track data
import os #!To check the file stuff

def readTrackConfig(fn: str = "Track.xlsx") -> Graph:
    #* Three graphs, one for each line
    blue = pd.read_excel(fn, sheet_name="Blue Line")
    print(blue)
    
    return 


if(__name__ == '__main__'):
    readTrackConfig()