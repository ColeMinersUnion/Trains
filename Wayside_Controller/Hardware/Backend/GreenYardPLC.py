class PLC:
    def __init__(self):
        self.occupancy = [False for i in range(36)]
        self.authority = [True for i in range(28)]
        self.switch_57 = False
        self.switch_63 = False
        self.maintenance = [False for i in range(36)]
        self.signal_57 = False
    def update_occupancy(self, new_occ):
        self.occupancy = new_occ
    
    def update_authority(self):
        for i in range(6):
            if any(self.occupancy[6:17]):
                self.authority[i] = False
            else:
                self.authority[i] = True

        for i in range(6, 17):
            if any(self.occupancy[17:22]) and self.switch_57 == True:
                self.authority[i] = False
                self.signal_57 = False
            else:
                self.authority[i] = True
                self.signal_57 = True   

        for i in range(17, 22):
            if any(self.occupancy[22:28]) or self.switch_63 == False:
                self.authority[i] = False
            else:
                self.authority[i] = True    

        for i in range(22, 28):
            if any(self.occupancy[28:]):
                self.authority[i] = False
            else:
                self.authority[i] = True    

    def update_switches(self, suggested_switch):
        if suggested_switch == True:
            self.switch_57 = True
            self.switch_63 = True
            return True
        elif suggested_switch == False:
            if any(self.occupancy[17:22]):
                self.switch_57 = True
                self.switch_63 = True
                return False
            else:
                self.switch_57 = False
                self.switch_63 = False
                return True
    
    def update_maintenance(self, new_maint):
        for i in range(6):
            if new_maint[i] == True and self.maintenance[i] == False:
                maint_safety = True
                for j in range(17):
                    if self.occupancy[j] == True and self.maintenance[j] == False:
                        maint_safety = False
                        break
                if maint_safety == True:
                    self.maintenance[i] = True
                    self.occupancy[i] = True
            elif new_maint[i] == False and self.maintenance[i] == True:
                self.maintenance[i] = False
                self.occupancy[i] = False
            
        for i in range(6, 17):
            if new_maint[i] == True and self.maintenance[i] == False:
                maint_safety = True
                for j in range(6, 22):
                    if self.occupancy[j] == True and self.maintenance[j] == False:
                        maint_safety = False
                        break
                if maint_safety == True:
                    self.maintenance[i] = True
                    self.occupancy[i] = True
            elif new_maint[i] == False and self.maintenance[i] == True:
                self.maintenance[i] = False
                self.occupancy[i] = False
        
        for i in range(17, 22):
            if new_maint[i] == True and self.maintenance[i] == False:
                maint_safety = True
                for j in range(17, 28):
                    if self.occupancy[j] == True and self.maintenance[j] == False:
                        maint_safety = False
                        break
                if maint_safety == True:
                    self.maintenance[i] = True
                    self.occupancy[i] = True
            elif new_maint[i] == False and self.maintenance[i] == True:
                self.maintenance[i] = False
                self.occupancy[i] = False
        
        for i in range(22, 28):
            if new_maint[i] == True and self.maintenance[i] == False:
                maint_safety = True
                for j in range(22, 36):
                    if self.occupancy[j] == True and self.maintenance[j] == False:
                        maint_safety = False
                        break
                if maint_safety == True:
                    self.maintenance[i] = True
                    self.occupancy[i] = True

    def maintenance_switch(self, sw57, sw63):
        if self.maintenance[57] == True and self.maintenance[58] == True:
            self.switch_57 = sw57

        if self.maintenance[63] == True and self.maintenance[64] == True:
            self.switch_63 = sw63

    def say_hello(self):
        print("Hello")