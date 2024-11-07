class Shell():
    def __init__(self):
        self.occupancy = [False for i in range(36)]
        self.authority = [False for i in range(28)]
        self.switch_57 = False
        self.signal_57 = False
        self.switch_63 = False
        self.signal_63 = False


    def rec_tm_occupancy(self, occ):
        self.occupancy = occ
