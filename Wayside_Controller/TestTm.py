
class TrackModel:
    def __init__ (self):
        self.occupancy = [False for i in range(17)]
        self.switch_5 = False
        self.signal_6 = False
        self.signal_12 = False
        self.crossing_3 = False
        self.shell = None
        self.trains = []

    def dispatch(self, Speed, Authority):
        self.trains.append(0)
        self.occupancy[0] = True
        print(Speed, Authority)

    def move_trains(self):
        for i in range(len(self.trains)):
            if self.shell.next_authority[self.trains[i]] == True:
                if self.trains[i] == 5 and self.shell.switch_5 == False:
                    print("Train at block", self.trains[i], " has moved to block ", 12)
                    self.trains[i] = 12
                    self.occupancy[5] = False
                    self.occupancy[12] = True
                else:
                    print("Train at block", self.trains[i], " has moved to block ", self.trains[i] + 1)
                    self.occupancy[self.trains[i]] = False
                    self.occupancy[self.trains[i] + 1] = True
                    self.trains[i] += 1
        
        self.shell.set_occupancy(self.occupancy)