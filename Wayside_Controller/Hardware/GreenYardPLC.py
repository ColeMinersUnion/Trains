
#Hardware zones
# ----
# 41-46
# ----
# 47-57
# 58-62 (Switch 57-Yard/57-58)
# 63-68 (Switch yard-63/62-63)
# ----
# 69-76
# ----
class PLC:
    def __init__(self):
        self.occupancy = [False for i in range(151)]
        self.authority = [False for i in range(151)]
        self.maintenance = [False for i in range(151)]
        self.sw58 = False
        self.sw62 = False
        self.sig58 = False
        self.sig62 = False


    def ctc_suggested_switch(self, sw):
        if sw == False:
            if(any(self.occupancy[58:63])):
                self.sw58 = True
                self.sw62 = True
                result = False
            else:
                self.sw58 = False
                self.sw62 = False
                result = True
        elif sw == True:
            self.sw58 = True
            self.sw62 = True
            result = True
        self.update_signals()
        self.update_authority(self.occupancy)
        return result
    
    def update_signals(self):
        if any(self.occupancy[58:63]):
            self.sig58 = False
        else:
            self.sig58 = True

        if any(self.occupancy[63:69]) or self.sw62 == False:
            self.sig62 = False
        else:
            self.sig62 = True


    
    def ctc_update_maintenance(self, maint_prop):
        for i in range(47, 58):
            if maint_prop[i] == False and self.maintenance[i] == True:
                self.maintenance[i] = False
                self.occupancy[i] = False
            elif maint_prop[i] == True and self.maintenance[i] == False:

                maint_safety = True
                for j in range(41, 58):
                    if self.occupancy[j] == True and self.maintenance[j] == False:
                        maint_safety = False
                        break
                if maint_safety == True:
                    self.maintenance[i] = True
                    self.occupancy[i] = True
        
        for i in range(58, 62):
            if maint_prop[i] == False and self.maintenance[i] == True:
                self.maintenance[i] = False
                self.occupancy[i] = False
            elif maint_prop[i] == True and self.maintenance[i] == False:

                maint_safety = True
                for j in range(47, 63):
                    if self.occupancy[j] == True and self.maintenance[j] == False:
                        maint_safety = False
                        break
                if maint_safety == True:
                    self.maintenance[i] = True
                    self.occupancy[i] = True

        for i in range(63, 69):
            if maint_prop[i] == False and self.maintenance[i] == True:
                self.maintenance[i] = False
                self.occupancy[i] = False
            elif maint_prop[i] == True and self.maintenance[i] == False:

                maint_safety = True
                for j in range(58, 69):
                    if self.occupancy[j] == True and self.maintenance[j] == False:
                        maint_safety = False
                        break
                if maint_safety == True:
                    self.maintenance[i] = True
                    self.occupancy[i] = True

        for i in range(69, 77):
            if maint_prop[i] == False and self.maintenance[i] == True:
                self.maintenance[i] = False
                self.occupancy[i] = False
            elif maint_prop[i] == True and self.maintenance[i] == False:

                maint_safety = True
                for j in range(63, 77):
                    if self.occupancy[j] == True and self.maintenance[j] == False:
                        maint_safety = False
                        break
                if maint_safety == True:
                    self.maintenance[i] = True
                    self.occupancy[i] = True
        
        self.update_authority(self.occupancy)
        return self.occupancy, self.authority, self.maintenance


    def update_authority(self, occ):
        self.occupancy = occ
        auth = [True for i in range(151)]

        for i in range(41, 47):
            if any(occ[47:58]):
                auth[i] = False
           
        for i in range(47, 58):
            if any(occ[58:63]) and self.sw58 == True:
                auth[i] = False

        for i in range(58, 63):
            if any(occ[63:69]) or self.sw62 == False:
                auth[i] = False

        for i in range(63, 69):
            if any(occ[69:77]):
                auth[i] = False
        self.authority = auth
        self.update_signals()
        return self.authority