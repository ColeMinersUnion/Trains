
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

            elif maint_prop[i] == True and self.maintenance[i] == False and not any(self.occupancy[41:77]):
                self.maintenance[i] = True

        for i in range(58, 63):
            if maint_prop[i] == False and self.maintenance[i] == True:
                self.maintenance[i] = False

            elif maint_prop[i] == True and self.maintenance[i] == False and not any(self.occupancy[47, 58]):
                self.maintenance[i] = True

        for i in range(63, 69):
            if maint_prop[i] == False and self.maintenance[i] == True:
                self.maintenance[i] = False

            elif maint_prop[i] == True and self.maintenance[i] == False and not any(self.occupancy[58, 63]):
                self.maintenance[i] = True

        for i in range(69, 77):
            if maint_prop[i] == False and self.maintenance[i] == True:
                self.maintenance[i] = False

            elif maint_prop[i] == True and self.maintenance[i] == False and not any(self.occupancy[63, 69]):
                self.maintenance[i] = True
        
        


    def update_authority(self, occ):
        self.occupancy = occ

        self.authority[41] = not any(occ[47:58]) and not any(occ[42:47])
        self.authority[42] = not any(occ[47:58]) and not any(occ[43:47])
        self.authority[43] = not any(occ[47:58]) and not any(occ[44:47])
        self.authority[44] = not any(occ[47:58]) and not any(occ[45:47])
        self.authority[45] = not any(occ[47:58]) and not any(occ[46:47])
        self.authority[46] = not any(occ[47:58])
        

        self.authority[47] = (not any(occ[58:63]) or self.sw58 == False) and not any(occ[48:58])
        self.authority[48] = (not any(occ[58:63]) or self.sw58 == False) and not any(occ[49:58])
        self.authority[49] = (not any(occ[58:63]) or self.sw58 == False) and not any(occ[50:58])
        self.authority[50] = (not any(occ[58:63]) or self.sw58 == False) and not any(occ[51:58])
        self.authority[51] = (not any(occ[58:63]) or self.sw58 == False) and not any(occ[52:58])
        self.authority[52] = (not any(occ[58:63]) or self.sw58 == False) and not any(occ[53:58])
        self.authority[53] = (not any(occ[58:63]) or self.sw58 == False) and not any(occ[54:58])
        self.authority[54] = (not any(occ[58:63]) or self.sw58 == False) and not any(occ[55:58])
        self.authority[55] = (not any(occ[58:63]) or self.sw58 == False) and not any(occ[56:58])
        self.authority[56] = (not any(occ[58:63]) or self.sw58 == False) and not any(occ[57:58])
        self.authority[57] = (not any(occ[58:63]) or self.sw58 == False) and not any(occ[58:59])
        
        self.authority[58] = (not any(occ[63:69]) and self.sw62 == True) and not any(occ[59:63])
        self.authority[59] = (not any(occ[63:69]) and self.sw62 == True) and not any(occ[60:63])
        self.authority[60] = (not any(occ[63:69]) and self.sw62 == True) and not any(occ[61:63])
        self.authority[61] = (not any(occ[63:69]) and self.sw62 == True) and not any(occ[62:63])
        self.authority[62] = (not any(occ[63:69]) and self.sw62 == True) and not any(occ[63:64])
        

        self.authority[63] = not any(occ[69:77]) and not any(occ[64:69])
        self.authority[64] = not any(occ[69:77]) and not any(occ[65:69])
        self.authority[65] = not any(occ[69:77]) and not any(occ[66:69])
        self.authority[66] = not any(occ[69:77]) and not any(occ[67:69])
        self.authority[67] = not any(occ[69:77]) and not any(occ[68:69])
        self.authority[68] = not any(occ[69:77]) and not any(occ[69:70])
        
        


        # auth = [True for i in range(151)]

        # for i in range(41, 47):
        #     if any(occ[47:58]):
        #         auth[i] = False
           
        # for i in range(47, 58):
        #     if any(occ[58:63]) and self.sw58 == True:
        #         auth[i] = False

        # for i in range(58, 63):
        #     if any(occ[63:69]) or self.sw62 == False:
        #         auth[i] = False

        # for i in range(63, 69):
        #     if any(occ[69:77]):
        #         auth[i] = False
        # self.authority = auth

        self.update_signals()
        return self.authority
    
    def toggle_sw58(self):
        if not any(self.occupancy[41:77]):
            self.sw58 = not self.sw58
            self.update_authority(self.occupancy)

    
    def toggle_sw62(self):
        if not any(self.occupancy[41:77]):
            self.sw62 = not self.sw62
            self.update_authority(self.occupancy)
        

    def toggle_sig58(self):
        if not any(self.occupancy[41:77]):
            self.sig58 = not self.sig58

    def toggle_sig62(self):
        if not any(self.occupancy[41:77]):
            self.sig62 = not self.sig62

    def maint_sw58(self):
        if self.maintenance[57] and self.maintenance[58]:
            self.sw58 = not self.sw58

    def maint_sw62(self):      
        if self.maintenance[62] and self.maintenance[63]:
            self.sw62 = not self.sw62
    
if __name__ == "__main__":
    plc = PLC()
    test_maint = [False for i in range(151)]
    test_maint[47] = True
    plc.ctc_update_maintenance(test_maint)
