from Graph import Graph #!to export the tracks
from Node import Node
import pandas as pd #!to read in the track data
import os #!To check the file stuff
import math

def readTrackConfig(fn: str = "Track.xlsx") -> Graph:
    #* Three graphs, one for each line
    fn = os.getcwd() + "/CTC_Office/Backend/" + fn
    blueLine = pd.read_excel(fn, sheet_name="Blue Line")
    #print(blue)
    blue = Graph()
    
    for index, blueRow in blueLine.iterrows():
        row = blueRow.to_dict()
        #print(f"dict\n{row}\ndict\n")
        print(f'{ row["Line"] }: {type(row["ELEVATION (M)"])}, {math.isnan(row["ELEVATION (M)"])}')
        if(not math.isnan(row["ELEVATION (M)"])):
            print(type(row["Block Number"]))
            newNode = Node(row)
            print(str(newNode))
            blue.addNode(newNode)
        


        

        


        
        
    return blue


if(__name__ == '__main__'):
    readTrackConfig()