import WaysidePLC
from WaysidePLC import BluePLC

class WaysideShell:
    def __init__(self):
        self.plc = WaysidePLC.BluePLC()

    def dispatch(self, speed, auth,  new_route):
        self.plc.dispatch(new_route)
        
        

    

    

