class CTC:
    def __init__(self):
        self.occupancy = [False for i in range(17)]
        self.block_error = [False for i in range(17)]
        self.switch_5 = False
        self.signal_6 = False
        self.signal_12 = False
        self.crossing_3 = False
        self.shell = None

    def dispatch(self, Speed, Authority, Switch):
        if all(i == False for i in self.occupancy[0:6]):
            self.shell.dispatch(Speed, Authority, Switch)
            return True
        else:
            print("Cannot dispatch train")
            return False
        
    def maintenance(self, maint_blocks):
        pass

    def set_occupancy(self, occupancy):
        self.occupancy = occupancy


