from Graph import Graph #!to export the tracks
from Node import Node
import pandas as pd #!to read in the track data
import os #!To check the file stuff
import math

def readTrackConfig(fn: str = "Track.xlsx") -> Graph:
    #* Three graphs, one for each line
    fn = os.getcwd() + "/CTC_Office/Backend/" + fn
    blueLine = pd.read_excel(fn, sheet_name="Blue Line")
    greenLine = pd.read_excel(fn, sheet_name="Green Line")
    redLine = pd.read_excel(fn, sheet_name="Red Line")
    #print(blue)
    blue = DF_to_Graph(blueLine)
    green = DF_to_Graph(greenLine)
    red = DF_to_Graph(redLine)
    
    
       
    return blue, green, red

def DF_to_Graph(df : pd.DataFrame) -> Graph:
    graff = Graph()
    #!Uncomment print statements for debugging
    for index, dfRow in df.iterrows():
        row = dfRow.to_dict()
        #print(f"dict\n{row}\ndict\n")
        #print(f'{ row["Line"] }: {type(row["ELEVATION (M)"])}, {math.isnan(row["ELEVATION (M)"])}')
        if(not math.isnan(row["ELEVATION (M)"])):
            #print(type(row["Block Number"]))
            newNode = Node(row)
            #print(str(newNode))
            graff.addNode(newNode)
    
    return graff

if(__name__ == '__main__'):
    readTrackConfig()