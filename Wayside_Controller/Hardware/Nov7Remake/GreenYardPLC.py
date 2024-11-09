
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
        pass

    def update(self, occ, sw, maint_prop, maint_curr):
        
        sw_success, sw58, sw62 = self.update_switches(occ, sw)
        occ, maint_curr = self.update_maintenance(occ, maint_prop, maint_curr)
        auth = self.update_authority(occ)

        return occ, auth, sw_success, sw58, sw62, maint_curr

    def update_switches(occ, sw):
        if sw == False:
            if(any(occ[58:63])):
                return False, True, True
            else:
                return True, False, False
        
        elif sw == True:
            return True, True, True
    
    def update_maintenance(occ, maint_prop, maint_curr):
        for i in range(47, 58):
            if maint_prop[i] == False and maint_curr[i] == True:
                maint_curr[i] = False
                occ[i] = False
            elif maint_prop[i] == True and maint_curr[i] == False:

                maint_safety = True
                for j in range(41, 58):
                    if occ[j] == True and maint_curr[j] == False:
                        maint_safety = False
                        break
                if maint_safety == True:
                    maint_curr[i] = True
                    occ[i] = True
        
        for i in range(58, 62):
            if maint_prop[i] == False and maint_curr[i] == True:
                maint_curr[i] = False
                occ[i] = False
            elif maint_prop[i] == True and maint_curr[i] == False:

                maint_safety = True
                for j in range(47, 63):
                    if occ[j] == True and maint_curr[j] == False:
                        maint_safety = False
                        break
                if maint_safety == True:
                    maint_curr[i] = True
                    occ[i] = True

        for i in range(63, 69):
            if maint_prop[i] == False and maint_curr[i] == True:
                maint_curr[i] = False
                occ[i] = False
            elif maint_prop[i] == True and maint_curr[i] == False:

                maint_safety = True
                for j in range(58, 69):
                    if occ[j] == True and maint_curr[j] == False:
                        maint_safety = False
                        break
                if maint_safety == True:
                    maint_curr[i] = True
                    occ[i] = True

        for i in range(69, 77):
            if maint_prop[i] == False and maint_curr[i] == True:
                maint_curr[i] = False
                occ[i] = False
            elif maint_prop[i] == True and maint_curr[i] == False:

                maint_safety = True
                for j in range(63, 77):
                    if occ[j] == True and maint_curr[j] == False:
                        maint_safety = False
                        break
                if maint_safety == True:
                    maint_curr[i] = True
                    occ[i] = True
        
        return occ, maint_curr

    def update_authority(occ, sw58, sw62):
        auth = [True for i in range(151)]

        for i in range(41, 47):
            if any(occ[i:58]):
                auth[i] = False
           
        for i in range(47, 58):
            if any(occ[i:58]) and sw58 == True:
                auth[i] = False

        for i in range(58, 63):
            if any(occ[i:63]) or sw62 == False:
                auth[i] = False

        for i in range(63, 69):
            if any(occ[i:69]):
                auth[i] = False
        return auth