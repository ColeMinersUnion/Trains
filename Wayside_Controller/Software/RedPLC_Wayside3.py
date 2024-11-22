#class for a wayside of the red line
#covers sections IJKLMN
#left=true, right=false
class RedWayside2:
    def __init__(self):
        #track switches
        #set to default track settings
        self.switch_52 = False
        #signals
        self.signal_52 = False
        #crossings
        self.crossing_47 = False
    def update_values():
        pass
    def update_crossing(self,occupancy):
        if any(occupancy[44:49])==True:
            self.crossing_47=True
        else:
            self.crossing_47=False
    def update_switch(self,occupancy):
        if any(occupancy[53:66])==True:
            self.switch_52=False
        else:
            self.switch_52=True
    def update_signal(self,sw52):
        #switch 52 settings: first left(true), then right(false)
        self.signal_52 = sw52
        if self.switch_52==False:
            self.signal_52=True
        else:
            self.signal_52=False
        return self.signal_52
    def update_authority(self,occupancy) -> list[bool]:
        #set train to move forward unless told otherwise
        authority=[True for i in range(77)]
        #begins on block 46
        if occupancy[45]==True and any(occupancy[46:66])==True:
            authority[46]=False
        else:
            authority[46]=True
        if occupancy[46]==True and any(occupancy[47:66])==True:
            authority[47]=False
        else:
            authority[47]=True
        #....rest of blocks leading to 52
        #switch 52 must be left(true) for train to move forward
        if occupancy[52]==True and (self.switch_52==False or any(occupancy[53:66])==True):
            authority[53]=False
        else:
            authority[53]=True
        if occupancy[53]==True and any(occupancy[54:66])==True:
            authority[54]=False
        else:
            authority[54]=True
        if occupancy[54]==True and any(occupancy[55:66])==True:
            authority[55]=False
        else:
            authority[55]=True
        if occupancy[55]==True and any(occupancy[56:66])==True:
            authority[56]=False
        else:
            authority[56]=True
        if occupancy[56]==True and any(occupancy[57:66])==True:
            authority[57]=False
        else:
            authority[57]=True
        if occupancy[57]==True and any(occupancy[58:66])==True:
            authority[58]=False
        else:
            authority[58]=True
        if occupancy[58]==True and any(occupancy[59:66])==True:
            authority[59]=False
        else:
            authority[59]=True
        if occupancy[59]==True and any(occupancy[60:66])==True:
            authority[60]=False
        else:
            authority[60]=True
        if occupancy[60]==True and any(occupancy[61:66])==True:
            authority[61]=False
        else:
            authority[61]=True
        #look ahead to J and I 
        #if there's an occupancy there train must stop in N

        #back in section I
        #look ahead to H 