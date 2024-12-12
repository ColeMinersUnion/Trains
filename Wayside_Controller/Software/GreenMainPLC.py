
#boolean values for the switch state: left=true, right=false

#class to hardcode green line        
class GreenPLC:

    def __init__(self):
        #to hold maintenance occupancies
        self.maintenance_occ=[False for i in range(151)]
        self.authority=[False for i in range(151)]
        #track switches
        self.switch_13 = True
        self.switch_28 = False
        self.switch_77 = False
        self.switch_85 = True
        #signals
        self.signal_13 = True
        self.signal_28 = True
        self.signal_77 = True
        self.signal_85 = True
        #crossings
        self.crossing_19=False
        self.crossing_108=False

        self.maint_safety=True
        self.sw_safety=True
        '''
        #stores block occupancies
        self.occupancies=[False for i in range(1,150)]
        #maintenance occupancies
        self.maint_occ=[False for i in range(1,150)]
        #stores authority
        self.next_authority=[False for i in range(1,150)]
        #zones
        self.zones=[self.occupancies[1:28], #FEDCBA
                        self.occupancies[29:35], #GH
                        self.occupancies[36:46], #I
                        self.occupancies[69:76], #LM
                        self.occupancies[77:100], #NOPQ
                        self.occupancies[101:109], #RST
                        self.occupancies[110:121], #UV
                        self.occupancies[122:143], #W
                        self.occupancies[144:150]] #XYZ ''' 
    
    #intakes new occupancies from track model and switch defaults from the shell
    def update_values(self, occupancy):
        #update switches then signals then crossings then authority
        switch77, switch85, switch28, switch13 = self.update_switch(occupancy)
        signal77, signal85, signal28, signal13 = self.update_signal(occupancy)
        crossing19, crossing108 = self.update_crossing(occupancy)
        self.authority=self.update_authority(occupancy)
        return self.authority, switch77, switch85, switch28, switch13, signal77, signal85, signal28, signal13, crossing19, crossing108
    
    def ctc_update_switch(self, sw:int, occupancy:list):
        if sw==13:
            if any(occupancy[1:29])==True:
                self.sw_safety=False
            else:
                self.sw_safety=True
                self.switch_13=not self.switch_13
                #self.shell_sw13.emit(self.switch_13)
        if sw==28:
            if any(occupancy[1:29]) or any(occupancy[144:150])==True:
                self.sw_safety=False
            else:
                self.sw_safety=True
                self.switch_28=not self.switch_28
                #self.shell_sw28.emit(self.switch_28)
        if sw==77:
            if any(occupancy[74:100])==True:
                self.sw_safety=False
            else:
                self.sw_safety=True
                self.switch_77=not self.switch_77
                #self.shell_sw77.emit(self.shell_sw77)
        if sw==85:
            if any(occupancy[82:100])==True:
                self.sw_safety=False
            else:
                self.sw_safety=True
                self.switch_85=not self.switch_85
                #self.shell_sw85.emit(self.shell_sw85)
        return self.sw_safety,self.switch_77,self.switch_85,self.switch_28,self.switch_13
            
    #takes in list of occupancies from ctc, updates with current occupancy list from the shell
    def maintenance_mode(self, suggested_maintenance, occupancy):
        #if theres an occupancy in the region, no maintenance or manual mode, it's disabled
        for i in range(77, 100):
            if suggested_maintenance[i] == False and self.maintenance_occ[i] == True:
                self.maintenance_occ[i] = False
            elif suggested_maintenance[i] == True and self.maintenance_occ[i] == False:
                self.maint_safety = True
                for j in range(69, 100):
                    if occupancy[j] == True and self.maintenance_occ[j] == False:
                        self.maint_safety = False
                        break
                if self.maint_safety == True:
                    self.maintenance_occ[i] = True
        for i in range(1, 29):
            if suggested_maintenance[i] == False and self.maintenance_occ[i] == True:
                self.maintenance_occ[i] = False
            elif suggested_maintenance[i] == True and self.maintenance_occ[i] == False:
                self.maint_safety = True
                for j in range(1, 13):
                    if occupancy[j] == True and self.maintenance_occ[j] == False:
                        self.maint_safety = False
                        break
                if self.maint_safety == True:
                    self.maintenance_occ[i] = True
        return suggested_maintenance, self.maint_safety
    
    #confirm PLC is uploaded
    def say_hi(self):
        print("PLC Uploaded Successfully")
    
    def update_signal(self, occupancy):
        #update signals according to default path (they turn red when there's a train on the section of track)
        if any(occupancy[77:100]):
            self.signal_77=False
        else: 
            self.signal_77=True
        if any(occupancy[86:100]):
            self.signal_85=False
        else: 
            self.signal_85=True
        if any(occupancy[1:27]):
            self.signal_28=False
        else: 
            self.signal_28=True
        if any(occupancy[1:12]):
            self.signal_13=False
        else: 
            self.signal_13=True
        return self.signal_77, self.signal_85, self.signal_28, self.signal_13

    
    def update_crossing(self, occupancy):
        #checks if the train is within 3 blocks of the crossings, if so sets crossings to true
        #crossings on greenline: 19 and 108 
        if any(occupancy[17:21])==True:
            self.crossing_19 = True
        else:
            self.crossing_19 = False
        if any(occupancy[106:110])==True:
            self.crossing_108=True
        else:
            self.crossing_108=False

        return self.crossing_19, self.crossing_108

    def update_switch(self, occupancy):
        #enforce default path (ie switch 77 can only switch to zone R when a train is present in NOPQ zone, and switch back when the train has left R)
        #switches on greenline: 13, 28, 77, 85
        self.switch_77=False
        self.switch_85=True
        self.switch_28=False
        self.switch_13=True
        #switch 77 (right then left, false then true)
        if any(occupancy[78:100])==True and self.switch_77==False:
            self.switch_77=True
        else: 
            self.switch_77=False
        #switch 85 (left then right, true then false)
        if any(occupancy[86:100])==True and self.switch_85==True:
            self.switch_85=False
        else: 
            self.switch_85=True
        #switch 28 (right then left, false then true)
        if any(occupancy[1:27])==True and self.switch_28==False:
            self.switch_28=True
        else: 
            self.switch_28=False
        #switch 13 (left then right, true then false)
        if any(occupancy[1:12])==True and self.switch_13==True:
            self.switch_13=False
        else: 
            self.switch_13=True
        
        return self.switch_77, self.switch_85, self.switch_28, self.switch_13

    
    #coding the default path along the green line
    #determines if each occupied block has the authority to move to the next block, this is layout dependent so it is hardcoded
    def update_authority(self, occupancy) -> list[bool]:
        #reset authority to true so train is moving unless told otherwise
        self.authority=[True for i in range(151)]
        #go through a zone using hardcoded index (cannot modify index) to make sure there is no other train on track to move ahead
        #or set authority to true by default and always look ahead to next zone (hardcode) to make sure no train is in the next zone
        #ONLY ONE TRAIN IN A ZONE AT A TIME (simplifies things for us and is technically a 'safety feature')
        #start at section overlap with waysideHW (block 69-76) (aka sections L and M):
        if (any(occupancy[69:76])==True):
            self.authority[69]=False
        else:
            self.authority[69]=True
        if (any(occupancy[70:76])==True):
            self.authority[70]==False
        else:
            self.authority[70]=True
        if (any(occupancy[71:76])==True):
            self.authority[71]==False
        else:
            self.authority[71]=True
        if (any(occupancy[72:76])==True):
            self.authority[72]==False
        else:
            self.authority[72]=True
        if (any(occupancy[73:76])==True):
            self.authority[73]==False
        else:
            self.authority[73]=True
        #now looking ahead to next zone
        if (any(occupancy[74:76])==True or any(occupancy[77:100])==True):
            self.authority[74]==False
        else:
            self.authority[74]=True
        if (any(occupancy[75:76])==True or any(occupancy[77:100])==True):
            self.authority[75]==False
        else:
            self.authority[75]=True
        if (occupancy[76]==True or any(occupancy[77:100])==True):
            self.authority[76]==False
        else:
            self.authority[76]=True
        #SWITCH 77 MUST BE FALSE (right) FOR TRAIN TO MOVE FORWARD
        if (self.switch_77==True or any(occupancy[77:100])==True):
            self.authority[77]=False
        else:
            self.authority[77]=True
        #end of zone LM


        #beginning of zone NOPQ (loop) (blocks 77-100)
        if (any(occupancy[78:100])==True):
            self.authority[78]=False
        else:
            self.authority[78]=True
        if (any(occupancy[79:100])==True):
            self.authority[79]=False
        else:
            self.authority[79]=True
        if (any(occupancy[80:100])==True):
            self.authority[80]=False
        else:
            self.authority[80]=True
        if (any(occupancy[81:100])==True):
            self.authority[81]=False
        else:
            self.authority[81]=True
        if (any(occupancy[82:100])==True):
            self.authority[82]=False
        else:
            self.authority[82]=True
        if (any(occupancy[83:100])==True):
            self.authority[83]=False
        else:
            self.authority[83]=True
        if (any(occupancy[84:100])==True):
            self.authority[84]=False
        else:
            self.authority[84]=True
        if (any(occupancy[85:100])==True):
            self.authority[85]=False
        else:
            self.authority[85]=True
        #SWITCH 85 MUST BE TRUE (left) BEFORE TRAIN CAN MOVE FORWARD
        if (self.switch_85==False or any(occupancy[86:100])==True):
            self.authority[86]=False
        else:
            self.authority[86]=True
        if (any(occupancy[87:100])==True):
            self.authority[87]=False
        else:
            self.authority[87]=True
        if (any(occupancy[88:100])==True):
            self.authority[88]=False
        else:
            self.authority[88]=True
        if (any(occupancy[89:100])==True):
            self.authority[89]=False
        else:
            self.authority[89]=True
        if (any(occupancy[90:100])==True):
            self.authority[90]=False
        else:
            self.authority[90]=True
        if (any(occupancy[91:100])==True):
            self.authority[91]=False
        else:
            self.authority[91]=True
        if (any(occupancy[92:100])==True):
            self.authority[92]=False
        else:
            self.authority[92]=True
        if (any(occupancy[93:100])==True):
            self.authority[93]=False
        else:
            self.authority[93]=True
        if (any(occupancy[94:100])==True):
            self.authority[94]=False
        else:
            self.authority[94]=True
        if (any(occupancy[95:100])==True):
            self.authority[95]=False
        else:
            self.authority[95]=True
        if (any(occupancy[96:100])==True):
            self.authority[96]=False
        else:
            self.authority[96]=True
        if (any(occupancy[97:100])==True):
            self.authority[97]=False
        else:
            self.authority[97]=True
        if (any(occupancy[98:100])==True):
            self.authority[98]=False
        else:
            self.authority[98]=True
        if (any(occupancy[99:100])==True):
            self.authority[99]=False
        else:
            self.authority[99]=True
        if self.switch_85==True or any(occupancy[85:77])==True:
            self.authority[100]=False
        else:
            self.authority[100]=True
        #Q ends at 100 and goes back into N (85)
        #start looking ahead into N at the end of the loop (blocks 85 down to 77)
        #SWITCH 85 AGAIN after going round the loop must be switched so train can move forward
        if (self.switch_85==True or any(occupancy[85:77])==True):
            self.authority[85]=False
        else:
            self.authority[85]=True
        if (any(occupancy[84:77])==True):
            self.authority[84]=False
        else:
            self.authority[84]=True
        if (any(occupancy[83:77])==True):
            self.authority[83]=False
        else:
            self.authority[83]=True
        if (any(occupancy[82:77])==True):
            self.authority[82]=False
        else:
            self.authority[82]=True
        if (any(occupancy[81:77])==True):
            self.authority[81]=False
        else:
            self.authority[81]=True
        if (any(occupancy[80:77])==True):
            self.authority[80]=False
        else:
            self.authority[80]=True
        if (any(occupancy[79:77])==True):
            self.authority[79]=False
        else:
            self.authority[79]=True
        #look ahead into next zone RST (blocks 101-109)
        if (any(occupancy[78:77])==True or any(occupancy[101:109])==True):
            self.authority[78]=False
        else:
            self.authority[78]=True
        if (any(occupancy[101:109])==True):
            self.authority[77]=False
        else:
            self.authority[77]=True
        #SWITCH 77 MUST BE SWITCHED TO LEFT FOR TRAIN TO MOVE TO ZONE RST
        if (self.switch_77==False or any(occupancy[101:109])==True):
            self.authority[101]=False
        else:
            self.authority[101]=True
        #end of zone NOPQ


        #beginning of zone RST (blocks 101-109)
        if (any(occupancy[102:109])==True):
            self.authority[102]=False
        else:
            self.authority[102]=True
        if (any(occupancy[103:109])==True):
            self.authority[103]=False
        else:
            self.authority[103]=True
        if (any(occupancy[104:109])==True):
            self.authority[104]=False
        else:
            self.authority[104]=True
        if (any(occupancy[105:109])==True):
            self.authority[105]=False
        else:
            self.authority[105]=True
        if (any(occupancy[106:109])==True):
            self.authority[106]=False
        else:
            self.authority[106]=True
        #look ahead to next zone (blocks 110-121)
        if (any(occupancy[107:109])==True or any(occupancy[110:121])==True):
            self.authority[107]=False
        else:
            self.authority[107]=True
        if (any(occupancy[108:109])==True or any(occupancy[110:121])==True):
            self.authority[108]=False
        else:
            self.authority[108]=True
        if (occupancy[109]==True or any(occupancy[110:121])==True):
            self.authority[109]=False
        else:
            self.authority[109]=True
        if (any(occupancy[110:121])==True):
            self.authority[110]=False
        else:
            self.authority[110]=True
        #end of zone RST


        #beginning of zone UV (blocks 110-121)
        if (any(occupancy[111:121])==True):
            self.authority[111]=False
        else:
            self.authority[111]=True
        if (any(occupancy[112:121])==True):
            self.authority[112]=False
        else:
            self.authority[112]=True 
        if (any(occupancy[113:121])==True):
            self.authority[113]=False
        else:
            self.authority[113]=True
        if (any(occupancy[114:121])==True):
            self.authority[114]=False
        else:
            self.authority[114]=True
        if (any(occupancy[115:121])==True):
            self.authority[115]=False
        else:
            self.authority[115]=True
        if (any(occupancy[116:121])==True):
            self.authority[116]=False
        else:
            self.authority[116]=True
        if (any(occupancy[117:121])==True):
            self.authority[117]=False
        else:
            self.authority[117]=True
        if (any(occupancy[118:121])==True):
            self.authority[118]=False
        else:
            self.authority[118]=True
        if (any(occupancy[119:121])==True):
            self.authority[119]=False
        else:
            self.authority[119]=True
        #look ahead to next zone (aka blocks 122-143)
        if (any(occupancy[120:121])==True or any(occupancy[122:143])==True):
            self.authority[120]=False
        else:
            self.authority[120]=True
        if (any(occupancy[121:143])==True):
            self.authority[121]=False
        else:
            self.authority[121]=True
        if (any(occupancy[122:143])==True):
            self.authority[122]=False
        else:
            self.authority[122]=True
        #end of zone UV


        #beginning of zone W (blocks 122-143)
        if (any(occupancy[123:143])==True):
            self.authority[123]=False
        else:
            self.authority[123]=True
        if (any(occupancy[124:143])==True):
            self.authority[124]=False
        else:
            self.authority[124]=True
        if (any(occupancy[125:143])==True):
            self.authority[125]=False
        else:
            self.authority[125]=True
        if (any(occupancy[126:143])==True):
            self.authority[126]=False
        else:
            self.authority[126]=True
        if (any(occupancy[127:143])==True):
            self.authority[127]=False
        else:
            self.authority[127]=True
        if (any(occupancy[128:143])==True):
            self.authority[128]=False
        else:
            self.authority[128]=True
        if (any(occupancy[129:143])==True):
            self.authority[129]=False
        else:
            self.authority[129]=True
        if (any(occupancy[130:143])==True):
            self.authority[130]=False
        else:
            self.authority[130]=True
        if (any(occupancy[131:143])==True):
            self.authority[131]=False
        else:
            self.authority[131]=True
        if (any(occupancy[132:143])==True):
            self.authority[132]=False
        else:
            self.authority[132]=True
        if (any(occupancy[133:143])==True):
            self.authority[133]=False
        else:
            self.authority[133]=True
        if (any(occupancy[134:143])==True):
            self.authority[134]=False
        else:
            self.authority[134]=True
        if (any(occupancy[135:143])==True):
            self.authority[135]=False
        else:
            self.authority[135]=True
        if (any(occupancy[136:143])==True):
            self.authority[136]=False
        else:
            self.authority[136]=True
        if (any(occupancy[137:143])==True):
            self.authority[137]=False
        else:
            self.authority[137]=True
        if (any(occupancy[138:143])==True):
            self.authority[138]=False
        else:
            self.authority[138]=True
        if (any(occupancy[139:143])==True):
            self.authority[139]=False
        else:
            self.authority[139]=True
        if (any(occupancy[140:143])==True):
            self.authority[140]=False
        else:
            self.authority[140]=True
        #look ahead to next zone (blocks 144-150)
        if (any(occupancy[141:143])==True or any(occupancy[144:150])==True):
            self.authority[141]=False
        else:
            self.authority[141]=True
        if (any(occupancy[142:143])==True or any(occupancy[144:150])==True):
            self.authority[142]=False
        else:
            self.authority[142]=True
        if (occupancy[143]==True or any(occupancy[144:150])==True):
            self.authority[143]=False
        else:
            self.authority[143]=True
        if (any(occupancy[144:150])==True):
            self.authority[144]=False
        else:
            self.authority[144]=True
        #end of zone W
        

        #beginning of zone XYZ (blocks 144-150)
        if (any(occupancy[145:150])==True):
            self.authority[145]==False
        else:
            self.authority[145]==True
        if (any(occupancy[146:150])==True):
            self.authority[146]=False
        else:
            self.authority[146]=True
        if (any(occupancy[147:150])==True):
            self.authority[147]=False
        else:
            self.authority[147]=True
        #look ahead to zone FEDCBA (blocks 28 down to 1)
        if (any(occupancy[148:150])==True):
            self.authority[148]=False
        else:
            self.authority[148]=True
        if (any(occupancy[149:150])==True):
            self.authority[149]=False
        else:
            self.authority[149]=True
        if (occupancy[150]==True):
            self.authority[150]=False
        else:
            self.authority[150]=True
        #SWITCH 28 must be right (false) before train can go through
        if (self.switch_28==True or any(occupancy[1:28])==True):
            self.authority[28]=False
        else:
            self.authority[28]=True
        #end of zone XYZ


        #beginning of zone FEDCBA
        if (any(occupancy[1:27])==True):
            self.authority[27]=False
        else:
            self.authority[27]=True
        if (any(occupancy[1:26])==True):
            self.authority[26]=False
        else:
            self.authority[26]=True
        if (any(occupancy[1:25])==True):
            self.authority[25]=False
        else:
            self.authority[25]=True
        if (any(occupancy[1:24])==True):
            self.authority[24]=False
        else:
            self.authority[24]=True
        if (any(occupancy[1:23])==True):
            self.authority[23]=False
        else:
            self.authority[23]=True
        if (any(occupancy[1:22])==True):
            self.authority[22]=False
        else:
            self.authority[22]=True
        if (any(occupancy[1:21])==True):
            self.authority[21]=False
        else:
            self.authority[21]=True
        if (any(occupancy[1:20])==True):
            self.authority[20]=False
        else:
            self.authority[20]=True
        if (any(occupancy[1:19])==True):
            self.authority[19]=False
        else:
            self.authority[19]=True
        if (any(occupancy[1:18])==True):
            self.authority[18]=False
        else:
            self.authority[18]=True
        if (any(occupancy[1:17])==True):
            self.authority[17]=False
        else:
            self.authority[17]=True
        if (any(occupancy[1:16])==True):
            self.authority[16]=False
        else:
            self.authority[16]=True
        if (any(occupancy[1:15])==True):
            self.authority[15]=False
        else:
            self.authority[15]=True
        if (any(occupancy[1:14])==True):
            self.authority[14]=False
        else:
            self.authority[14]=True
        if (any(occupancy[1:13])==True):
            self.authority[13]=False
        else:
            self.authority[13]=True
        #SWITCH 13 MUST BE LEFT (TRUE) FOR TRAIN TO MOVE FORWARD
        if (self.switch_13==False or any(occupancy[1:12])==True):
            self.authority[12]=False
        else:
            self.authority[12]=True
        if (any(occupancy[1:11])==True):
            self.authority[11]=False
        else:
            self.authority[11]=True
        if (any(occupancy[1:10])==True):
            self.authority[10]=False
        else:
            self.authority[10]=True
        if (any(occupancy[1:9])==True):
            self.authority[9]=False
        else:
            self.authority[9]=True
        if (any(occupancy[1:8])==True):
            self.authority[8]=False
        else:
            self.authority[8]=True
        if (any(occupancy[1:7])==True):
            self.authority[7]=False
        else:
            self.authority[7]=True
        if (any(occupancy[1:6])==True):
            self.authority[6]=False
        else:
            self.authority[6]=True
        if (any(occupancy[1:5])==True):
            self.authority[5]=False
        else:
            self.authority[5]=True
        if (any(occupancy[1:4])==True):
            self.authority[4]=False
        else:
            self.authority[4]=True
        #LOOK BACK AHEAD TO DEF
        if (any(occupancy[1:3])==True or any(occupancy[13:28])):
            self.authority[3]=False
        else:
            self.authority[3]=True
        if (any(occupancy[1:2])==True or any(occupancy[13:28])):
            self.authority[2]=False
        else:
            self.authority[2]=True
        if (occupancy[12]==True or any(occupancy[13:28])):
            self.authority[1]=False
        else:
            self.authority[1]=True
        if (any(occupancy[13:28])==True):
            self.authority[12]==False
        else:
            self.authority[12]=True
        #BACK TO SWITCH 13 (ON BLOCK 12 OF C) MUST BE FALSE (RIGHT) FOR THE TRAIN TO GO
        #END OF CBA LOOP
        #BACK IN DEF
        if (self.switch_13==True or any(occupancy[13:28])==True):
            self.authority[13]==False
        else:
            self.authority[13]==True
        if (any(occupancy[14:28])==True):
            self.authority[14]==False
        else:
            self.authority[14]==True
        if (any(occupancy[15:28])==True):
            self.authority[15]==False
        else:
            self.authority[15]==True
        if (any(occupancy[16:28])==True):
            self.authority[16]==False
        else:
            self.authority[16]==True
        if (any(occupancy[17:28])==True):
            self.authority[17]==False
        else:
            self.authority[17]==True
        if (any(occupancy[18:28])==True):
            self.authority[18]==False
        else:
            self.authority[18]==True
        if (any(occupancy[19:28])==True):
            self.authority[19]==False
        else:
            self.authority[19]==True
        if (any(occupancy[20:28])==True):
            self.authority[20]==False
        else:
            self.authority[20]==True
        if (any(occupancy[21:28])==True):
            self.authority[21]==False
        else:
            self.authority[21]==True
        if (any(occupancy[22:28])==True):
            self.authority[22]==False
        else:
            self.authority[22]==True
        if (any(occupancy[23:28])==True):
            self.authority[23]==False
        else:
            self.authority[23]==True
        if (any(occupancy[24:28])==True):
            self.authority[24]==False
        else:
            self.authority[24]==True
        if (any(occupancy[24:28])==True):
            self.authority[24]==False
        else:
            self.authority[24]==True
        if (any(occupancy[25:28])==True):
            self.authority[25]==False
        else:
            self.authority[25]==True
        #LOOK AHEAD TO GH
        if (any(occupancy[26:28])==True or any(occupancy[29:35])==True):
            self.authority[26]==False
        else:
            self.authority[26]==True
        if (any(occupancy[27:28])==True or any(occupancy[29:35])==True):
            self.authority[27]==False
        else:
            self.authority[27]==True
        if (any(occupancy[29:35])==True):
            self.authority[28]==False
        else:
            self.authority[28]==True
        #BACK TO SWITCH 28 must be LEFT (True)
        if (self.switch_28==False or any(occupancy[29:35])==True):
            self.authority[29]==False
        else:
            self.authority[29]==True
        #END OF FEDCBA


        #beginning of zone GH (blocks 29-35)
        if (any(occupancy[30:35])==True):
            self.authority[30]=False
        else:
            self.authority[30]=True
        if (any(occupancy[31:35])==True):
            self.authority[31]=False
        else:
            self.authority[31]=True
        if (any(occupancy[32:35])==True):
            self.authority[32]=False
        else:
            self.authority[32]=True
        #look ahead into next zone (blocks 36-46)
        if (any(occupancy[33:35])==True or any(occupancy[36:46])==True):
            self.authority[33]=False
        else:
            self.authority[33]=True
        if (any(occupancy[34:35])==True or any(occupancy[36:46])==True):
            self.authority[34]=False
        else:
            self.authority[34]=True
        if (occupancy[35]==True or any(occupancy[36:46])==True):
            self.authority[35]=False
        else:
            self.authority[35]=True
        if (any(occupancy[36:46])==True):
            self.authority[36]=False
        else:
            self.authority[36]=True
        #end of zone GH


        #beginning of zone I (blocks 36-46)
        if (any(occupancy[37:46])==True):
            self.authority[37]=False
        else:
            self.authority[37]=True
        if (any(occupancy[38:46])==True):
            self.authority[38]=False
        else:
            self.authority[38]=True
        if (any(occupancy[39:46])==True):
            self.authority[39]=False
        else:
            self.authority[39]=True
        if(any(occupancy[40:46])==True):
            self.authority[40]=False
        else:
            self.authority[40]=True
        

        return self.authority