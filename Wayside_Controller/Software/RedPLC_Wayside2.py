#class for a wayside of the red line
#covers sections GH and OPQRST
class RedWayside1:
    def __init__(self):
        #track switches on GH (no switches on OPQRST)
        #set to default track settings
        self.switch_27 = False
        self.switch_33 = False
        self.switch_38 = False
        self.switch_44 = False
        #signals
        self.signal_27 = False
        self.signal_33 = False
        self.signal_38 = False
        self.signal_44= False
        #no crossings on this wayside

    def update_values():
        pass
    def update_switch(self, occupancy):
        pass
    def update_signal(self,sw27,sw33,sw38,sw44):
        pass
    def update_authority(self, occupancy) -> list[bool]:
        pass