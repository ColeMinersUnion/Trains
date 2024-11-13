
#boolean values for the switch state: left=true, right=false

#class to hardcode green line        
class GreenPLC:
    def __init__(self):
       
        #track switches
        self.switch_13 = True
        self.switch_28 = False
        self.switch_77 = False
        self.switch_85 = True
        #signals
        self.signal_13 = False
        self.signal_28 = False
        self.signal_77 = False
        self.signal_85 = False
        #crossings
        self.crossing_19=False
        self.crossing_108=False
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
    def update_values(self, occupancy, sw77, sw85, sw28, sw13):
        #update signals, switches, crossings then authority
        switch77, switch85, switch28, switch13 = self.update_switch(occupancy, sw77, sw85, sw28, sw13)
        signal77, signal85, signal28, signal13 = self.update_signal(switch77, switch85, switch28, switch13)
        crossing19, crossing108 = self.update_crossing(occupancy)
        authority=self.update_authority(occupancy)
        return authority, switch77, switch85, switch28, switch13, signal77, signal85, signal28, signal13, crossing19, crossing108

    def maintenance(self):
        #if theres an occupancy in the region, no maintenance or manual mode, it's disabled
        pass
    
    #confirm PLC is uploaded
    def say_hi(self):
        print("PLC Uploaded Successfully")
    
    def update_signal(self, sw77, sw85, sw28, sw13):
        self.switch_77=sw77
        self.switch_85=sw85
        self.switch_28=sw28
        self.switch_13=sw13
        #update signals according to default path (they turn on when the switch changes from 'default' setting)
        if self.switch_77==True:
            self.signal_77=True
        else: 
            self.signal_77=False
        if self.switch_85==False:
            self.signal_85=True
        else: 
            self.signal_85=False
        if self.switch_28==True:
            self.signal_28=True
        else: 
            self.signal_28=False
        if self.switch_13==False:
            self.signal_13=True
        else: 
            self.signal_13=False
        return self.signal_77, self.signal_85, self.signal_28, self.signal_13

    
    def update_crossing(self, occupancy):
        #checks if the train is within 3 blocks of the crossings, if so sets crossings to true
        #crossings on greenline: 19 and 108 
        if occupancy[17] == True or occupancy[18] == True or occupancy[19] == True or occupancy[20] == True or occupancy[21] == True:
            self.crossing_19 = True
        else:
            self.crossing_19 = False
        if occupancy[106]==True or occupancy[107]==True or occupancy[108]==True or occupancy[109]==True or occupancy[110]==True:
            self.crossing_108=True
        else:
            self.crossing_108=False

        return self.crossing_19, self.crossing_108

    def update_switch(self, occupancy, switch_77, switch_85, switch_28, switch_13):
        #enforce default path (ie switch 77 can only switch to zone R when a train is present in NOPQ zone, and switch back when the train has left R)
        #switches on greenline: 13, 28, 77, 85
        #switch 77 (right then left, false then true)
        if any(occupancy[78:100]==True) and switch_77==False:
            switch_77=True
        else: 
            switch_77=False
        #switch 85 (left then right, true then false)
        if any(occupancy[86:100]==True) and switch_85==True:
            switch_85=False
        else: 
            switch_85=True
        #switch 28 (right then left, false then true)
        if any(occupancy[1:27]==True) and switch_28==False:
            switch_28=True
        else: 
            switch_28=False
        #switch 13 (left then right, true then false)
        if any(occupancy[1:12]==True) and switch_13==True:
            switch_13=False
        else: 
            switch_13=True
        
        return switch_77, switch_85, switch_28, switch_13

    
    #coding the default path along the green line
    #determines if each occupied block has the authority to move to the next block, this is layout dependent so it is hardcoded
    def update_authority(self, occupancy):
        #reset authority to true so train is moving unless told otherwise
        authority=[True for i in range(1,150)]
        #go through a zone using hardcoded index (cannot modify index) to make sure there is no other train on track to move ahead
        #or set authority to true by default and always look ahead to next zone (hardcode) to make sure no train is in the next zone
        #ONLY ONE TRAIN IN A ZONE AT A TIME (simplifies things for us and is technically a 'safety feature')
        #start at section overlap with waysideHW (block 69-76) (aka sections L and M):
        if occupancy[69]==True and (any(occupancy[70:76])==True):
            authority[70]==False
        else:
            authority[70]=True
        if occupancy[70]==True and (any(occupancy[71:76])==True):
            authority[71]==False
        else:
            authority[71]=True
        if occupancy[71]==True and (any(occupancy[72:76])==True):
            authority[72]==False
        else:
            authority[72]=True
        if occupancy[72]==True and (any(occupancy[73:76])==True):
            authority[73]==False
        else:
            authority[73]=True
        #now looking ahead to next zone
        if occupancy[73]==True and (any(occupancy[74:76])==True or any(occupancy[77:100])==True):
            authority[74]==False
        else:
            authority[74]=True
        if occupancy[74]==True and (any(occupancy[75:76])==True or any(occupancy[77:100])==True):
            authority[75]==False
        else:
            authority[75]=True
        if occupancy[75]==True and (occupancy[76]==True or any(occupancy[77:100])==True):
            authority[76]==False
        else:
            authority[76]=True
        if occupancy[76]==True and (any(occupancy[77:100])==True):
            authority[77]==False
        #SWITCH 77 MUST BE FALSE (right) FOR TRAIN TO MOVE FORWARD
        elif occupancy[76]==True and (self.switch_77==True or any(occupancy[77:100])==True):
            authority[77]=False
        else:
            authority[77]=True
        #end of zone LM


        #beginning of zone NOPQ (loop) (blocks 77-100)
        if occupancy[77]==True and (any(occupancy[78:100])==True):
            authority[78]=False
        else:
            authority[78]=True
        if occupancy[78]==True and (any(occupancy[79:100])==True):
            authority[79]=False
        else:
            authority[79]=True
        if occupancy[79]==True and (any(occupancy[80:100])==True):
            authority[80]=False
        else:
            authority[80]=True
        if occupancy[80]==True and (any(occupancy[81:100])==True):
            authority[81]=False
        else:
            authority[81]=True
        if occupancy[81]==True and (any(occupancy[82:100])==True):
            authority[82]=False
        else:
            authority[82]=True
        if occupancy[82]==True and (any(occupancy[83:100])==True):
            authority[83]=False
        else:
            authority[83]=True
        if occupancy[83]==True and (any(occupancy[84:100])==True):
            authority[84]=False
        else:
            authority[84]=True
        if occupancy[84]==True and (any(occupancy[85:100])==True):
            authority[85]=False
        else:
            authority[85]=True
        #SWITCH 85 MUST BE TRUE (left) BEFORE TRAIN CAN MOVE FORWARD
        if occupancy[85]==True and (self.switch_85==False or any(occupancy[86:100])==True):
            authority[86]=False
        else:
            authority[86]=True
        if occupancy[86]==True and (any(occupancy[87:100])==True):
            authority[87]=False
        else:
            authority[87]=True
        if occupancy[87]==True and (any(occupancy[88:100])==True):
            authority[88]=False
        else:
            authority[88]=True
        if occupancy[88]==True and (any(occupancy[89:100])==True):
            authority[89]=False
        else:
            authority[89]=True
        if occupancy[89]==True and (any(occupancy[90:100])==True):
            authority[90]=False
        else:
            authority[90]=True
        if occupancy[90]==True and (any(occupancy[91:100])==True):
            authority[91]=False
        else:
            authority[91]=True
        if occupancy[91]==True and (any(occupancy[92:100])==True):
            authority[92]=False
        else:
            authority[92]=True
        if occupancy[92]==True and (any(occupancy[93:100])==True):
            authority[93]=False
        else:
            authority[93]=True
        if occupancy[93]==True and (any(occupancy[94:100])==True):
            authority[94]=False
        else:
            authority[94]=True
        if occupancy[94]==True and (any(occupancy[95:100])==True):
            authority[95]=False
        else:
            authority[95]=True
        if occupancy[95]==True and (any(occupancy[96:100])==True):
            authority[96]=False
        else:
            authority[96]=True
        if occupancy[96]==True and (any(occupancy[97:100])==True):
            authority[97]=False
        else:
            authority[97]=True
        if occupancy[97]==True and (any(occupancy[98:100])==True):
            authority[98]=False
        else:
            authority[98]=True
        if occupancy[98]==True and (any(occupancy[99:100])==True):
            authority[99]=False
        else:
            authority[99]=True
        if occupancy[99]==True and (occupancy[100]==True):
            authority[100]=False
        else:
            authority[100]=True
        #Q ends at 100 and goes back into N (85)
        #start looking ahead into N at the end of the loop (blocks 85 down to 77)
        #SWITCH 85 AGAIN after going round the loop must be switched so train can move forward
        if occupancy[100]==True and (self.switch_85==True or any(occupancy[85:77])==True):
            authority[85]=False
        else:
            authority[85]=True
        if occupancy[85]==True and (any(occupancy[84:77])==True):
            authority[84]=False
        else:
            authority[84]=True
        if occupancy[84]==True and (any(occupancy[83:77])==True):
            authority[83]=False
        else:
            authority[83]=True
        if occupancy[83]==True and (any(occupancy[82:77])==True):
            authority[82]=False
        else:
            authority[82]=True
        if occupancy[82]==True and (any(occupancy[81:77])==True):
            authority[81]=False
        else:
            authority[81]=True
        if occupancy[81]==True and (any(occupancy[80:77])==True):
            authority[80]=False
        else:
            authority[80]=True
        if occupancy[80]==True and (any(occupancy[79:77])==True):
            authority[79]=False
        else:
            authority[79]=True
        #look ahead into next zone RST (blocks 101-109)
        if occupancy[79]==True and (any(occupancy[78:77])==True or any(occupancy[101:109])==True):
            authority[78]=False
        else:
            authority[78]=True
        if occupancy[78]==True and (occupancy[77]==True or any(occupancy[101:109])==True):
            authority[77]=False
        else:
            authority[77]=True
        #SWITCH 77 MUST BE SWITCHED TO LEFT FOR TRAIN TO MOVE TO ZONE RST
        if occupancy[77]==True and (self.switch_77==False or any(occupancy[101:109])==True):
            authority[101]=False
        else:
            authority[101]=True
        #end of zone NOPQ


        #beginning of zone RST (blocks 101-109)
        if occupancy[101]==True and (any(occupancy[102:109])==True):
            authority[102]=False
        else:
            authority[102]=True
        if occupancy[102]==True and (any(occupancy[103:109])==True):
            authority[103]=False
        else:
            authority[103]=True
        if occupancy[103]==True and (any(occupancy[104:109])==True):
            authority[104]=False
        else:
            authority[104]=True
        if occupancy[104]==True and (any(occupancy[105:109])==True):
            authority[105]=False
        else:
            authority[105]=True
        if occupancy[105]==True and (any(occupancy[106:109])==True):
            authority[106]=False
        else:
            authority[106]=True
        #look ahead to next zone (blocks 110-121)
        if occupancy[106]==True and (any(occupancy[107:109])==True or any(occupancy[110:121])==True):
            authority[107]=False
        else:
            authority[107]=True
        if occupancy[107]==True and (any(occupancy[108:109])==True or any(occupancy[110:121])==True):
            authority[108]=False
        else:
            authority[108]=True
        if occupancy[108]==True and (occupancy[109]==True or any(occupancy[110:121])==True):
            authority[109]=False
        else:
            authority[109]=True
        if occupancy[109]==True and (any(occupancy[110:121])==True):
            authority[110]=False
        else:
            authority[110]=True
        #end of zone RST


        #beginning of zone UV (blocks 110-121)
        if occupancy[110]==True and (any(occupancy[111:121])==True):
            authority[111]=False
        else:
            authority[111]=True
        if occupancy[111]==True and (any(occupancy[112:121])==True):
            authority[112]=False
        else:
            authority[112]=True 
        if occupancy[112]==True and (any(occupancy[113:121])==True):
            authority[113]=False
        else:
            authority[113]=True
        if occupancy[113]==True and (any(occupancy[114:121])==True):
            authority[114]=False
        else:
            authority[114]=True
        if occupancy[114]==True and (any(occupancy[115:121])==True):
            authority[115]=False
        else:
            authority[115]=True
        if occupancy[115]==True and (any(occupancy[116:121])==True):
            authority[116]=False
        else:
            authority[116]=True
        if occupancy[116]==True and (any(occupancy[117:121])==True):
            authority[117]=False
        else:
            authority[117]=True
        if occupancy[117]==True and (any(occupancy[118:121])==True):
            authority[118]=False
        else:
            authority[118]=True
        if occupancy[118]==True and (any(occupancy[119:121])==True):
            authority[119]=False
        else:
            authority[119]=True
        #look ahead to next zone (aka blocks 122-143)
        if occupancy[119]==True and (any(occupancy[120:121])==True or any(occupancy[122:143])==True):
            authority[120]=False
        else:
            authority[120]=True
        if occupancy[120]==True and (occupancy[121]==True or any(occupancy[122:143]==True)):
            authority[121]=False
        else:
            authority[121]=True
        if occupancy[121]==True and (any(occupancy[122:143])==True):
            authority[122]=False
        else:
            authority[122]=True
        #end of zone UV


        #beginning of zone W (blocks 122-143)
        if occupancy[122]==True and (any(occupancy[123:143])==True):
            authority[123]=False
        else:
            authority[123]=True
        if occupancy[123]==True and (any(occupancy[124:143])==True):
            authority[124]=False
        else:
            authority[124]=True
        if occupancy[124]==True and (any(occupancy[125:143])==True):
            authority[125]=False
        else:
            authority[125]=True
        if occupancy[125]==True and (any(occupancy[126:143])==True):
            authority[126]=False
        else:
            authority[126]=True
        if occupancy[126]==True and (any(occupancy[127:143])==True):
            authority[127]=False
        else:
            authority[127]=True
        if occupancy[127]==True and (any(occupancy[128:143])==True):
            authority[128]=False
        else:
            authority[128]=True
        if occupancy[128]==True and (any(occupancy[129:143])==True):
            authority[129]=False
        else:
            authority[129]=True
        if occupancy[129]==True and (any(occupancy[130:143])==True):
            authority[130]=False
        else:
            authority[130]=True
        if occupancy[130]==True and (any(occupancy[131:143])==True):
            authority[131]=False
        else:
            authority[131]=True
        if occupancy[131]==True and (any(occupancy[132:143])==True):
            authority[132]=False
        else:
            authority[132]=True
        if occupancy[132]==True and (any(occupancy[133:143])==True):
            authority[133]=False
        else:
            authority[133]=True
        if occupancy[133]==True and (any(occupancy[134:143])==True):
            authority[134]=False
        else:
            authority[134]=True
        if occupancy[134]==True and (any(occupancy[135:143])==True):
            authority[135]=False
        else:
            authority[135]=True
        if occupancy[135]==True and (any(occupancy[136:143])==True):
            authority[136]=False
        else:
            authority[136]=True
        if occupancy[136]==True and (any(occupancy[137:143])==True):
            authority[137]=False
        else:
            authority[137]=True
        if occupancy[137]==True and (any(occupancy[138:143])==True):
            authority[138]=False
        else:
            authority[138]=True
        if occupancy[138]==True and (any(occupancy[139:143])==True):
            authority[139]=False
        else:
            authority[139]=True
        if occupancy[139]==True and (any(occupancy[140:143])==True):
            authority[140]=False
        else:
            authority[140]=True
        #look ahead to next zone (blocks 144-150)
        if occupancy[140]==True and (any(occupancy[141:143])==True or any(occupancy[144:150])==True):
            authority[141]=False
        else:
            authority[141]=True
        if occupancy[141]==True and (any(occupancy[142:143])==True or any(occupancy[144:150])==True):
            authority[142]=False
        else:
            authority[142]=True
        if occupancy[142]==True and (occupancy[143]==True or any(occupancy[144:150])==True):
            authority[143]=False
        else:
            authority[143]=True
        if occupancy[143]==True and (any(occupancy[144:150])==True):
            authority[144]=False
        else:
            authority[144]=True
        #end of zone W
        

        #beginning of zone XYZ (blocks 144-150)
        if occupancy[144]==True and (any(occupancy[145:150])==True):
            authority[145]==False
        else:
            authority[145]==True
        if occupancy[145]==True and (any(occupancy[146:150])==True):
            authority[146]=False
        else:
            authority[146]=True
        if occupancy[146]==True and (any(occupancy[147:150])==True):
            authority[147]=False
        else:
            authority[147]=True
        #look ahead to zone FEDCBA (blocks 28 down to 1)
        if occupancy[147]==True and (any(occupancy[148:150])==True):
            authority[148]=False
        else:
            authority[148]=True
        if occupancy[148]==True and (any(occupancy[149:150])==True):
            authority[149]=False
        else:
            authority[149]=True
        if occupancy[149]==True and (occupancy[150]==True):
            authority[150]=False
        else:
            authority[150]=True
        #SWITCH 28 must be right (false) before train can go through
        if occupancy[150]==True and (self.switch_28==True or any(occupancy[1:28])==True):
            authority[28]=False
        else:
            authority[28]=True
        #end of zone XYZ


        #beginning of zone FEDCBA
        if occupancy[28]==True and (any(occupancy[1:27])==True):
            authority[27]=False
        else:
            authority[27]=True
        if occupancy[27]==True and (any(occupancy[1:26])==True):
            authority[26]=False
        else:
            authority[26]=True
        if occupancy[26]==True and (any(occupancy[1:25])==True):
            authority[25]=False
        else:
            authority[25]=True
        if occupancy[25]==True and (any(occupancy[1:24])==True):
            authority[24]=False
        else:
            authority[24]=True
        if occupancy[24]==True and (any(occupancy[1:23])==True):
            authority[23]=False
        else:
            authority[23]=True
        if occupancy[23]==True and (any(occupancy[1:22])==True):
            authority[22]=False
        else:
            authority[22]=True
        if occupancy[22]==True and (any(occupancy[1:21])==True):
            authority[21]=False
        else:
            authority[21]=True
        if occupancy[21]==True and (any(occupancy[1:20])==True):
            authority[20]=False
        else:
            authority[20]=True
        if occupancy[20]==True and (any(occupancy[1:19])==True):
            authority[19]=False
        else:
            authority[19]=True
        if occupancy[19]==True and (any(occupancy[1:18])==True):
            authority[18]=False
        else:
            authority[18]=True
        if occupancy[18]==True and (any(occupancy[1:17])==True):
            authority[17]=False
        else:
            authority[17]=True
        if occupancy[17]==True and (any(occupancy[1:16])==True):
            authority[16]=False
        else:
            authority[16]=True
        if occupancy[16]==True and (any(occupancy[1:15])==True):
            authority[15]=False
        else:
            authority[15]=True
        if occupancy[15]==True and (any(occupancy[1:14])==True):
            authority[14]=False
        else:
            authority[14]=True
        if occupancy[14]==True and (any(occupancy[1:13])==True):
            authority[13]=False
        else:
            authority[13]=True
        #SWITCH 13 MUST BE LEFT (TRUE) FOR TRAIN TO MOVE FORWARD
        if occupancy[13]==True and (self.switch_13==False or any(occupancy[1:12])==True):
            authority[12]=False
        else:
            authority[12]=True
        if occupancy[12]==True and (any(occupancy[1:11])==True):
            authority[11]=False
        else:
            authority[11]=True
        if occupancy[11]==True and (any(occupancy[1:10])==True):
            authority[10]=False
        else:
            authority[10]=True
        if occupancy[10]==True and (any(occupancy[1:9])==True):
            authority[9]=False
        else:
            authority[9]=True
        if occupancy[9]==True and (any(occupancy[1:8])==True):
            authority[8]=False
        else:
            authority[8]=True
        if occupancy[8]==True and (any(occupancy[1:7])==True):
            authority[7]=False
        else:
            authority[7]=True
        if occupancy[7]==True and (any(occupancy[1:6])==True):
            authority[6]=False
        else:
            authority[6]=True
        if occupancy[6]==True and (any(occupancy[1:5])==True):
            authority[5]=False
        else:
            authority[5]=True
        if occupancy[5]==True and (any(occupancy[1:4])==True):
            authority[4]=False
        else:
            authority[4]=True
        #LOOK BACK AHEAD TO DEF
        if occupancy[4]==True and (any(occupancy[1:3])==True or any(occupancy[13:28])):
            authority[3]=False
        else:
            authority[3]=True
        if occupancy[3]==True and (any(occupancy[1:2])==True or any(occupancy[13:28])):
            authority[2]=False
        else:
            authority[2]=True
        if occupancy[2]==True and (occupancy[1]==True or occupancy[12]==True or any(occupancy[13:28])):
            authority[1]=False
        else:
            authority[1]=True
        if occupancy[1]==True and (occupancy[12]==True or any(occupancy[13:28])==True):
            authority[12]==False
        else:
            authority[12]=True
        #BACK TO SWITCH 13 (ON BLOCK 12 OF C) MUST BE FALSE (RIGHT) FOR THE TRAIN TO GO
        #END OF CBA LOOP
        #BACK IN DEF
        if occupancy[12]==True and (self.switch_13==True or any(occupancy[13:28])==True):
            authority[13]==False
        else:
            authority[13]==True
        if occupancy[13]==True and (any(occupancy[14:28])==True):
            authority[14]==False
        else:
            authority[14]==True
        if occupancy[14]==True and (any(occupancy[15:28])==True):
            authority[15]==False
        else:
            authority[15]==True
        if occupancy[15]==True and (any(occupancy[16:28])==True):
            authority[16]==False
        else:
            authority[16]==True
        if occupancy[16]==True and (any(occupancy[17:28])==True):
            authority[17]==False
        else:
            authority[17]==True
        if occupancy[17]==True and (any(occupancy[18:28])==True):
            authority[18]==False
        else:
            authority[18]==True
        if occupancy[18]==True and (any(occupancy[19:28])==True):
            authority[19]==False
        else:
            authority[19]==True
        if occupancy[19]==True and (any(occupancy[20:28])==True):
            authority[20]==False
        else:
            authority[20]==True
        if occupancy[20]==True and (any(occupancy[21:28])==True):
            authority[21]==False
        else:
            authority[21]==True
        if occupancy[21]==True and (any(occupancy[22:28])==True):
            authority[22]==False
        else:
            authority[22]==True
        if occupancy[22]==True and (any(occupancy[23:28])==True):
            authority[23]==False
        else:
            authority[23]==True
        if occupancy[23]==True and (any(occupancy[24:28])==True):
            authority[24]==False
        else:
            authority[24]==True
        if occupancy[24]==True and (any(occupancy[24:28])==True):
            authority[24]==False
        else:
            authority[24]==True
        if occupancy[24]==True and (any(occupancy[25:28])==True):
            authority[25]==False
        else:
            authority[25]==True
        #LOOK AHEAD TO GH
        if occupancy[25]==True and (any(occupancy[26:28])==True or any(occupancy[29:35])==True):
            authority[26]==False
        else:
            authority[26]==True
        if occupancy[26]==True and (any(occupancy[27:28])==True or any(occupancy[29:35])==True):
            authority[27]==False
        else:
            authority[27]==True
        if occupancy[27]==True and (occupancy[28]==True or any(occupancy[29:35])==True):
            authority[28]==False
        else:
            authority[28]==True
        #BACK TO SWITCH 28 must be LEFT (True)
        if occupancy[28]==True and (self.switch_28==False or any(occupancy[29:35])==True):
            authority[29]==False
        else:
            authority[29]==True
        #END OF FEDCBA


        #beginning of zone GH (blocks 29-35)
        if occupancy[29]==True and (any(occupancy[30:35])==True):
            authority[30]=False
        else:
            authority[30]=True
        if occupancy[30]==True and (any(occupancy[31:35])==True):
            authority[31]=False
        else:
            authority[31]=True
        if occupancy[31]==True and (any(occupancy[32:35])==True):
            authority[32]=False
        else:
            authority[32]=True
        #look ahead into next zone (blocks 36-46)
        if occupancy[32]==True and (any(occupancy[33:35])==True or any(occupancy[36:46])==True):
            authority[33]=False
        else:
            authority[33]=True
        if occupancy[33]==True and (any(occupancy[34:35])==True or any(occupancy[36:46])==True):
            authority[34]=False
        else:
            authority[34]=True
        if occupancy[34]==True and (occupancy[35]==True or any(occupancy[36:46])==True):
            authority[35]=False
        else:
            authority[35]=True
        if occupancy[35]==True and (any(occupancy[36:46])==True):
            authority[36]=False
        else:
            authority[36]=True
        #end of zone GH


        #beginning of zone I (blocks 36-46)
        if occupancy[36]==True and (any(occupancy[37:46])==True):
            authority[37]=False
        else:
            authority[37]=True
        if occupancy[37]==True and (any(occupancy[38:46])==True):
            authority[38]=False
        else:
            authority[38]=True
        if occupancy[38]==True and (any(occupancy[39:46])==True):
            authority[39]=False
        else:
            authority[39]=True
        if occupancy[39]==True and (any(occupancy[40:46])==True):
            authority[40]=False
        else:
            authority[40]=True
        if occupancy[40]==True and (any(occupancy[41:46])==True):
            authority[41]=False
        else:
            authority[41]=True
        if occupancy[41]==True and (any(occupancy[42:46])==True):
            authority[42]=False
        else:
            authority[42]=True
        if occupancy[42]==True and (any(occupancy[43:46])==True):
            authority[43]=False
        else:
            authority[43]=True
        if occupancy[43]==True and (any(occupancy[44:46])==True):
            authority[44]=False
        else:
            authority[44]=True
        if occupancy[44]==True and (any(occupancy[45:46])==True):
            authority[45]=False
        else:
            authority[45]=True
        if occupancy[45]==True and (occupancy[46]==True):
            authority[46]=False
        else:
            authority[46]=True
        #end of zone I for main wayside

        return authority