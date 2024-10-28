
class GreenYardPLC:
    def __init__(self):
        self.switch_58 = False
        self.switch_62 = False
        self.authority = [False for i in range(27)]
        self.occupancy = [False for i in range(33)]

        # 2 dimensional lists to represent occupancy and authorities split into zones
        self.zone_occ = [self.occupancy[:6], self.occupancy[6:16], self.occupancy[16:22], self.occupancy[22:27], self.occupancy[27:]]
        self.zone_auth = [self.authority[:6], self.authority[6:16], self.authority[16:22], self.authority[22:]]
        self.maint_zones = [self.occupancy[:6], self.occupancy[6:16], self.occupancy[16:22], self.occupancy[22:27], self.occupancy[27:]]
   
    # takes inputted occupancy list and splits it into zones
    def update_occupancy(self, new_occ):
        self.occupancy = new_occ
        self.zone_occ = [self.occupancy[:6], self.occupancy[6:16], self.occupancy[16:22], self.occupancy[22:27], self.occupancy[27:]]
        self.update_authority()
        return self.authority

    # takes suggested maintenance list and checks for safety, then updates maintenance 2d list
    def maintenance(self, maint_sugg):
        maint_sugg_zones = [maint_sugg[:6], maint_sugg[6:16], maint_sugg[16:22], maint_sugg[22:27], maint_sugg[27:]]
        for i in range(5):
            for j in range(len(self.maint_zones[i])):
                if maint_sugg_zones[i][j] == True and self.maint_zones[i][j] == False:
                    if any(self.zone_occ[i][k] == True and self.maint_zones[i][k] == False for k in range(len(self.maint_zones[i]))):
                        self.maint_zones[i][j] = False
                        return False
                    else:
                        self.maint_zones[i][j] = True
                        self.zone_occ[i][j] = True
                        return True
                if maint_sugg_zones[i][j] == False and self.maint_zones[i][j] == True:
                    self.maint_zones[i][j] = False
                    self.zone_occ[i][j] = False
                    return True
        # reconstructs occupancy list based on zone occupancy 2d list
        self.occupancy = []
        for zone in self.zone_occ:
            for block in zone:
                self.occupancy.append(block)

        # updates authorities based on new maintenance blocks
        self.update_authority()
        return self.authority
    
    def switch_suggestion(self, switch):
        if switch == True:
            if self.switch_58 and self.switch_62:
                self.update_authority()
                return True
            self.switch_58 = True
            self.switch_62 = True
            self.update_authority()
            return True
        
        if switch == False:
            if any(self.zone_occ[3]):
                self.switch_58 = True
                self.switch_62 = True
                self.update_authority()
                return False
            else:
                self.switch_58 = False
                self.switch_62 = False
                self.update_authority()
                return True
        
            
    def update_authority(self):
        next_zone = iter(self.zone_occ)
        next(next_zone)

        #initially sets the authority all occupancies to true
        self.authority = self.occupancy[:27]
        self.zone_auth = [self.authority[:6], self.authority[6:16], self.authority[16:22], self.authority[22:]]

        # sets the all the auth of the current zone to false if the next zone has any occupancy
        for i in range(4):
            if any(next(next_zone)):
                self.zone_auth[i] = [False for j in range(len(self.zone_auth[i]))]
        
        # sets the authority of zone 3 to false if the switch is not connected to the line
        # This is a redunant check as the switch should always be set to true if there is an occupancy in zone 3
        if self.switch_62 == False:
            self.zone_auth[3] = [False for i in range(5)]

        # problem for later: set auth of zone to false if occupancy is detected in the same zone

        # updates authority based on zone_auth
        self.authority = []
        for zone in self.zone_auth:
            for block in zone:
                self.authority.append(block)
    


            
    def say_hi(self):
        print("PLC Uploaded Successfully")


if __name__ == "__main__":
    plc = GreenYardPLC()