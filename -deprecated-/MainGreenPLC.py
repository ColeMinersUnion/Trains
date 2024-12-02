import copy

#boolean values for the switch state: left=true, right=false
#switch queue to hold switch changes
class SwitchQueue:
    def __init__(self):
        self.queue=[]

    def enqueue(self, change):
        self.queue.append(change)

    def dequeue(self):
        try:
            return None
        except len(self.queue) > 0:
            return self.queue.pop(0)
        
    def peek(self):
        try:
            return None
        except len(self.queue) > 0:
            return self.queue[0]
        
#class to hardcode green line        
class GreenPLC:
    def __init__(self):
        #track switches, signals, crossings
        self.switch_13 = False
        self.switch_28 = False
        self.switch_77 = False
        self.switch_85 = False

        self.switch_13_queue=SwitchQueue()
        self.switch_28_queue=SwitchQueue()
        self.switch_77_queue=SwitchQueue()
        self.switch_85_queue=SwitchQueue()

        self.crossing_19=False
        self.crossing_108=False
         
        #stores block occupancies
        self.occupancies=[False for i in range(1,150)]
        self.prev_occupancies=[False for i in range(1,150)]
        #other occupancies
        self.maint_occ=[False for i in range(1,150)]
        self.train_occ=[False for i in range(1,150)]
        self.errors=[False for i in range(1,150)]
        #stores authority (authority is set to true until train must stop)
        self.next_authority=[True for i in range(1,150)]
 
    def update_train_occ(self):
        if self.occupancies[0]==True:
            self.train_occ[0]=True
        
    def maintenance(self):
        pass
    
    #confirm PLC is uploaded
    def say_hi(self):
        print("PLC Uploaded Successfully")

    #block errors
    def block_error_check(self):
        for i in self.occupancies:
            try:
                self.errors[i]=False
            except (self.occupancies[i]==True and self.maint_occ==False and self.train_occ==False):
                self.errors[i]=True
    
    def update_crossing(self):
        #checks if the train is within 3 blocks of the crossings, if so sets crossings to true
        #crossings on greenline: 19 and 108 
        if self.train_occ[17] == True or self.train_occ[18] == True or self.train_occ[19] == True or self.train_occ[20] == True or self.train_occ[21] == True:
            self.crossing_19 = True
        else:
            self.crossing_19 = False
        
        if self.train_occ[106]==True or self.train_occ[107]==True or self.train_occ[108]==True or self.train_occ[109]==True or self.train_occ[110]==True:
            self.crossing_108=True
        else:
            self.crossing_108=False

    def update_switch(self):
        #switches on greenline: 13, 28, 77, 85
        #checks if the switch queue is empty, if not, sets switch 13 to the command at the top of the queue
        if self.switch_13_queue.peek() != None:
            self.switch_13 = self.switch_13_queue.peek()
        else:
            self.switch_13 = False
        #do this for each switch on the green line:
        #switch 28
        if self.switch_28_queue.peek() != None:
            self.switch_28 = self.switch_28_queue.peek()
        else:
            self.switch_28 = False
        #switch 77
        if self.switch_77_queue.peek() != None:
            self.switch_77 = self.switch_77_queue.peek()
        else:
            self.switch_77 = False
        #switch 85
        if self.switch_85_queue.peek() != None:
            self.switch_85 = self.switch_85_queue.peek()
        else:
            self.switch_85 = False
        #enforce default path (ie switch 77 can only switch to R when a train is present in NOPQ zone, and switch back when the train has left R)
        
    
    #coding the default path along the green line
    #determines if each occupied block has the authority to move to the next block, this is layout dependent so it is hardcoded
    def update_authority(self):
        #reset authority to true
        self.next_authority=[True for i in range(1,150)]
        #section out the zones according to excel layout by putting block zones into a list
        self.zone_list=[self.occupancies[1:28], #FEDCBA
                        self.occupancies[29:35], #GH
                        self.occupancies[36:40], #I
                        self.occupancies[41:46], #I
                        self.occupancies[69:76], #LM
                        self.occupancies[77:100], #NOPQ
                        self.occupancies[101:109], #RST
                        self.occupancies[110:121], #UV
                        self.occupancies[122:143], #W
                        self.occupancies[144:150]] #XYZ
        #go through a zone using hardcoded index (cannot modify index) to make sure there is no other train on track to move ahead
        #or set authority to true by default and always look ahead to next zone (hardcode) to make sure no train is in the next zone
        #ONLY ONE TRAIN IN A ZONE AT A TIME (simplifies things for us and is technically a 'safety feature')
        #start at section overlap with waysideHW (block 69-76) (aka sections L and M):
        if self.train_occ[69]==True and (any(self.occupancies[70:76])==True or any(self.train_occ[70:76])==True):
            self.next_authority[70]==False
        else:
            self.next_authority[70]=True
        if self.train_occ[70]==True and (any(self.occupancies[71:76])==True or any(self.train_occ[71:76])==True):
            self.next_authority[71]==False
        else:
            self.next_authority[71]=True
        if self.train_occ[71]==True and (any(self.occupancies[72:76])==True or any(self.train_occ[72:76])==True):
            self.next_authority[72]==False
        else:
            self.next_authority[72]=True
        if self.train_occ[72]==True and (any(self.occupancies[73:76])==True or any(self.train_occ[73:76])==True):
            self.next_authority[73]==False
        else:
            self.next_authority[73]=True
        #now looking ahead to next zone
        if self.train_occ[73]==True and (any(self.occupancies[74:76])==True or any(self.train_occ[74:76])==True or 
                                           any(self.occupancies[77:100])==True or any(self.train_occ[77:100])==True):
            self.next_authority[74]==False
        else:
            self.next_authority[74]=True
        if self.train_occ[74]==True and (any(self.occupancies[75:76])==True or any(self.train_occ[75:76])==True or 
                                           any(self.occupancies[77:100])==True or any(self.train_occ[77:100])==True):
            self.next_authority[75]==False
        else:
            self.next_authority[75]=True
        if self.train_occ[75]==True and (self.occupancies[76]==True or self.train_occ[76]==True or 
                                           any(self.occupancies[77:100])==True or any(self.train_occ[77:100])==True):
            self.next_authority[76]==False
        else:
            self.next_authority[76]=True
        if self.train_occ[76]==True and (any(self.occupancies[77:100])==True or any(self.train_occ[77:100])==True):
            self.next_authority[77]==False
        #SWITCH 77 MUST BE IN CORRECT POSITION (right) FOR TRAIN TO MOVE FORWARD
        elif self.train_occ[76]==True and self.switch_77==False and (all(self.occupancies[77:100])==False and all(self.train_occ[77:100])==False):
            self.next_authority[77]=True
        else:
            self.next_authority[77]=True
        #end of zone LM


        #beginning of zone NOPQ (loop) (blocks 77-100)
        if self.train_occ[77]==True and (any(self.occupancies[78:100])==True or any(self.train_occ[78:100])==True):
            self.next_authority[78]=False
        else:
            self.next_authority[78]=True
        if self.train_occ[78]==True and (any(self.occupancies[79:100])==True or any(self.train_occ[79:100])==True):
            self.next_authority[79]=False
        else:
            self.next_authority[79]=True
        if self.train_occ[79]==True and (any(self.occupancies[80:100])==True or any(self.train_occ[80:100])==True):
            self.next_authority[80]=False
        else:
            self.next_authority[80]=True
        if self.train_occ[80]==True and (any(self.occupancies[81:100])==True or any(self.train_occ[81:100])==True):
            self.next_authority[81]=False
        else:
            self.next_authority[81]=True
        if self.train_occ[81]==True and (any(self.occupancies[82:100])==True or any(self.train_occ[82:100])==True):
            self.next_authority[82]=False
        else:
            self.next_authority[82]=True
        if self.train_occ[82]==True and (any(self.occupancies[83:100])==True or any(self.train_occ[83:100])==True):
            self.next_authority[83]=False
        else:
            self.next_authority[83]=True
        if self.train_occ[83]==True and (any(self.occupancies[84:100])==True or any(self.train_occ[84:100])==True):
            self.next_authority[84]=False
        else:
            self.next_authority[84]=True
        if self.train_occ[84]==True and (any(self.occupancies[85:100])==True or any(self.train_occ[85:100])==True):
            self.next_authority[85]=False
        else:
            self.next_authority[85]=True
        #SWITCH 85 MUST BE CORRECT BEFORE TRAIN CAN MOVE FORWARD
        if self.train_occ[85]==True and self.switch_85==True and (any(self.occupancies[86:100])==True or any(self.train_occ[86:100])==True):
            self.next_authority[86]=False
        elif self.train_occ[85]==True and self.switch_85==True and (all(self.occupancies[86:100])==False and all(self.train_occ[86:100])==False):
            self.next_authority[86]=True
        else:
            self.next_authority[86]=True
        if self.train_occ[86]==True and (any(self.occupancies[87:100])==True or any(self.train_occ[87:100])==True):
            self.next_authority[87]=False
        else:
            self.next_authority[87]=True
        if self.train_occ[87]==True and (any(self.occupancies[88:100])==True or any(self.train_occ[88:100])==True):
            self.next_authority[88]=False
        else:
            self.next_authority[88]=True
        if self.train_occ[88]==True and (any(self.occupancies[89:100])==True or any(self.train_occ[89:100])==True):
            self.next_authority[89]=False
        else:
            self.next_authority[89]=True
        if self.train_occ[89]==True and (any(self.occupancies[90:100])==True or any(self.train_occ[90:100])==True):
            self.next_authority[90]=False
        else:
            self.next_authority[90]=True
        if self.train_occ[90]==True and (any(self.occupancies[91:100])==True or any(self.train_occ[91:100])==True):
            self.next_authority[91]=False
        else:
            self.next_authority[91]=True
        if self.train_occ[91]==True and (any(self.occupancies[92:100])==True or any(self.train_occ[92:100])==True):
            self.next_authority[92]=False
        else:
            self.next_authority[92]=True
        if self.train_occ[92]==True and (any(self.occupancies[93:100])==True or any(self.train_occ[93:100])==True):
            self.next_authority[93]=False
        else:
            self.next_authority[93]=True
        if self.train_occ[93]==True and (any(self.occupancies[94:100])==True or any(self.train_occ[94:100])==True):
            self.next_authority[94]=False
        else:
            self.next_authority[94]=True
        if self.train_occ[94]==True and (any(self.occupancies[95:100])==True or any(self.train_occ[95:100])==True):
            self.next_authority[95]=False
        else:
            self.next_authority[95]=True
        if self.train_occ[95]==True and (any(self.occupancies[96:100])==True or any(self.train_occ[96:100])==True):
            self.next_authority[96]=False
        else:
            self.next_authority[96]=True
        if self.train_occ[96]==True and (any(self.occupancies[97:100])==True or any(self.train_occ[97:100])==True):
            self.next_authority[97]=False
        else:
            self.next_authority[97]=True
        if self.train_occ[97]==True and (any(self.occupancies[98:100])==True or any(self.train_occ[98:100])==True):
            self.next_authority[98]=False
        else:
            self.next_authority[98]=True
        if self.train_occ[98]==True and (any(self.occupancies[99:100])==True or any(self.train_occ[99:100])==True):
            self.next_authority[99]=False
        else:
            self.next_authority[99]=True
        if self.train_occ[99]==True and (self.occupancies[100]==True or self.train_occ[100]==True):
            self.next_authority[100]=False
        else:
            self.next_authority[100]=True
        #Q ends at 100 and goes back into N (85)
        #start looking ahead into N at the end of the loop (blocks 85 down to 77)
        #SWITCH 85 AGAIN after going round the loop must be switched so train can move forward
        if self.train_occ[100]==True and (any(self.occupancies[85:77])==True or any(self.train_occ[85:77])==True):
            self.next_authority[85]=False
        elif self.train_occ[100]==True and self.switch_85==False and (all(self.occupancies[85:77])==False and all(self.train_occ[85:77])==False):
            self.next_authority[85]=True
        else:
            self.next_authority[85]=True
        if self.train_occ[85]==True and (any(self.occupancies[84:77])==True or any(self.train_occ[84:77])==True):
            self.next_authority[84]=False
        else:
            self.next_authority[84]=True
        if self.train_occ[84]==True and (any(self.occupancies[83:77])==True or any(self.train_occ[83:77])==True):
            self.next_authority[83]=False
        else:
            self.next_authority[83]=True
        if self.train_occ[83]==True and (any(self.occupancies[82:77])==True or any(self.train_occ[82:77])==True):
            self.next_authority[82]=False
        else:
            self.next_authority[82]=True
        if self.train_occ[82]==True and (any(self.occupancies[81:77])==True or any(self.train_occ[81:77])==True):
            self.next_authority[81]=False
        else:
            self.next_authority[81]=True
        if self.train_occ[81]==True and (any(self.occupancies[80:77])==True or any(self.train_occ[80:77])==True):
            self.next_authority[80]=False
        else:
            self.next_authority[80]=True
        if self.train_occ[80]==True and (any(self.occupancies[79:77])==True or any(self.train_occ[79:77])==True):
            self.next_authority[79]=False
        else:
            self.next_authority[79]=True
        #look ahead into next zone RST (blocks 101-109)\
        if self.train_occ[79]==True and (any(self.occupancies[78:77])==True or any(self.train_occ[78:77])==True
                                         or any(self.occupancies[101:109])==True or any(self.train_occ[101:109])==True):
            self.next_authority[78]=False
        else:
            self.next_authority[78]=True
        if self.train_occ[78]==True and (self.occupancies[77]==True or self.train_occ[77]==True
                                         or any(self.occupancies[101:109])==True or any(self.train_occ[101:109])==True):
            self.next_authority[77]=False
        else:
            self.next_authority[77]=True
        #SWITCH 77 MUST BE SWITCHED FOR TRAIN TO MOVE TO ZONE RST
        if self.train_occ[77]==True and self.switch_77==False and (any(self.occupancies[101:109])==True or any(self.train_occ[101:109])==True):
            self.next_authority[101]=False
        elif self.train_occ[77]==True and self.switch_77==False and (all(self.occupancies[101:109])==False and all(self.train_occ[101:109])==False):
            self.next_authority[101]=True
        else:
            self.next_authority[101]=True
        #end of zone NOPQ


        #beginning of zone RST (blocks 101-109)
        if self.train_occ[101]==True and (any(self.occupancies[102:109])==True or any(self.train_occ[102:109])==True):
            self.next_authority[102]=False
        else:
            self.next_authority[102]=True
        if self.train_occ[102]==True and (any(self.occupancies[103:109])==True or any(self.train_occ[103:109])==True):
            self.next_authority[103]=False
        else:
            self.next_authority[103]=True
        if self.train_occ[103]==True and (any(self.occupancies[104:109])==True or any(self.train_occ[104:109])==True):
            self.next_authority[104]=False
        else:
            self.next_authority[104]=True
        if self.train_occ[104]==True and (any(self.occupancies[105:109])==True or any(self.train_occ[105:109])==True):
            self.next_authority[105]=False
        else:
            self.next_authority[105]=True
        if self.train_occ[105]==True and (any(self.occupancies[106:109])==True or any(self.train_occ[106:109])==True):
            self.next_authority[106]=False
        else:
            self.next_authority[106]=True
        #look ahead to next zone (blocks 110-121)
        if self.train_occ[106]==True and (any(self.occupancies[107:109])==True or any(self.train_occ[107:109])==True
                                          or any(self.occupancies[110:121])==True or any(self.train_occ[110:121])==True):
            self.next_authority[107]=False
        else:
            self.next_authority[107]=True
        if self.train_occ[107]==True and (any(self.occupancies[108:109])==True or any(self.train_occ[108:109])==True
                                          or any(self.occupancies[110:121])==True or any(self.train_occ[110:121])==True):
            self.next_authority[108]=False
        else:
            self.next_authority[108]=True
        if self.train_occ[108]==True and (self.occupancies[109]==True or self.train_occ[104:109]==True
                                          or any(self.occupancies[110:121])==True or any(self.train_occ[110:121])==True):
            self.next_authority[109]=False
        else:
            self.next_authority[109]=True
        if self.train_occ[109]==True and (any(self.occupancies[110:121])==True or any(self.train_occ[110:121])==True):
            self.next_authority[110]=False
        else:
            self.next_authority[110]=True
        #end of zone RST


        #beginning of zone UV (blocks 110-121)
        if self.train_occ[110]==True and (any(self.occupancies[111:121])==True or any(self.train_occ[111:121])==True):
            self.next_authority[111]=False
        else:
            self.next_authority[111]=True
        if self.train_occ[111]==True and (any(self.occupancies[112:121])==True or any(self.train_occ[112:121])==True):
            self.next_authority[112]=False
        else:
            self.next_authority[112]=True 
        if self.train_occ[112]==True and (any(self.occupancies[113:121])==True or any(self.train_occ[113:121])==True):
            self.next_authority[113]=False
        else:
            self.next_authority[113]=True
        if self.train_occ[113]==True and (any(self.occupancies[114:121])==True or any(self.train_occ[114:121])==True):
            self.next_authority[114]=False
        else:
            self.next_authority[114]=True
        if self.train_occ[114]==True and (any(self.occupancies[115:121])==True or any(self.train_occ[115:121])==True):
            self.next_authority[115]=False
        else:
            self.next_authority[115]=True
        if self.train_occ[115]==True and (any(self.occupancies[116:121])==True or any(self.train_occ[116:121])==True):
            self.next_authority[116]=False
        else:
            self.next_authority[116]=True
        if self.train_occ[116]==True and (any(self.occupancies[117:121])==True or any(self.train_occ[117:121])==True):
            self.next_authority[117]=False
        else:
            self.next_authority[117]=True
        if self.train_occ[117]==True and (any(self.occupancies[118:121])==True or any(self.train_occ[118:121])==True):
            self.next_authority[118]=False
        else:
            self.next_authority[118]=True
        if self.train_occ[118]==True and (any(self.occupancies[119:121])==True or any(self.train_occ[119:121])==True):
            self.next_authority[119]=False
        else:
            self.next_authority[119]=True
        #look ahead to next zone (aka blocks 122-143)
        if self.train_occ[119]==True and (any(self.occupancies[120:121])==True or any(self.train_occ[120:121])==True
                                          or any(self.occupancies[122:143])==True or any(self.train_occ[122:143])==True):
            self.next_authority[120]=False
        else:
            self.next_authority[120]=True
        if self.train_occ[120]==True and (self.occupancies[121]==True or self.train_occ[121]==True
                                          or any(self.occupancies[122:143])==True or any(self.train_occ[122:143]==True)):
            self.next_authority[121]=False
        else:
            self.next_authority[121]=True
        if self.train_occ[121]==True and (any(self.occupancies[122:143])==True or any(self.train_occ[122:143])==True):
            self.next_authority[122]=False
        else:
            self.next_authority[122]=True
        #end of zone UV


        #beginning of zone W (blocks 122-143)
        if self.train_occ[122]==True and (any(self.occupancies[123:143])==True or any(self.train_occ[123:143])==True):
            self.next_authority[123]=False
        else:
            self.next_authority[123]=True
        if self.train_occ[123]==True and (any(self.occupancies[124:143])==True or any(self.train_occ[124:143])==True):
            self.next_authority[124]=False
        else:
            self.next_authority[124]=True
        if self.train_occ[124]==True and (any(self.occupancies[125:143])==True or any(self.train_occ[125:143])==True):
            self.next_authority[125]=False
        else:
            self.next_authority[125]=True
        if self.train_occ[125]==True and (any(self.occupancies[126:143])==True or any(self.train_occ[126:143])==True):
            self.next_authority[126]=False
        else:
            self.next_authority[126]=True
        if self.train_occ[126]==True and (any(self.occupancies[127:143])==True or any(self.train_occ[127:143])==True):
            self.next_authority[127]=False
        else:
            self.next_authority[127]=True
        if self.train_occ[127]==True and (any(self.occupancies[128:143])==True or any(self.train_occ[128:143])==True):
            self.next_authority[128]=False
        else:
            self.next_authority[128]=True
        if self.train_occ[128]==True and (any(self.occupancies[129:143])==True or any(self.train_occ[129:143])==True):
            self.next_authority[129]=False
        else:
            self.next_authority[129]=True
        if self.train_occ[129]==True and (any(self.occupancies[130:143])==True or any(self.train_occ[130:143])==True):
            self.next_authority[130]=False
        else:
            self.next_authority[130]=True
        if self.train_occ[130]==True and (any(self.occupancies[131:143])==True or any(self.train_occ[131:143])==True):
            self.next_authority[131]=False
        else:
            self.next_authority[131]=True
        if self.train_occ[131]==True and (any(self.occupancies[132:143])==True or any(self.train_occ[132:143])==True):
            self.next_authority[132]=False
        else:
            self.next_authority[132]=True
        if self.train_occ[132]==True and (any(self.occupancies[133:143])==True or any(self.train_occ[133:143])==True):
            self.next_authority[133]=False
        else:
            self.next_authority[133]=True
        if self.train_occ[133]==True and (any(self.occupancies[134:143])==True or any(self.train_occ[134:143])==True):
            self.next_authority[134]=False
        else:
            self.next_authority[134]=True
        if self.train_occ[134]==True and (any(self.occupancies[135:143])==True or any(self.train_occ[135:143])==True):
            self.next_authority[135]=False
        else:
            self.next_authority[135]=True
        if self.train_occ[135]==True and (any(self.occupancies[136:143])==True or any(self.train_occ[136:143])==True):
            self.next_authority[136]=False
        else:
            self.next_authority[136]=True
        if self.train_occ[136]==True and (any(self.occupancies[137:143])==True or any(self.train_occ[137:143])==True):
            self.next_authority[137]=False
        else:
            self.next_authority[137]=True
        if self.train_occ[137]==True and (any(self.occupancies[138:143])==True or any(self.train_occ[138:143])==True):
            self.next_authority[138]=False
        else:
            self.next_authority[138]=True
        if self.train_occ[138]==True and (any(self.occupancies[139:143])==True or any(self.train_occ[139:143])==True):
            self.next_authority[139]=False
        else:
            self.next_authority[139]=True
        if self.train_occ[139]==True and (any(self.occupancies[140:143])==True or any(self.train_occ[140:143])==True):
            self.next_authority[140]=False
        else:
            self.next_authority[140]=True
        #look ahead to next zone (blocks 144-150)
        if self.train_occ[140]==True and (any(self.occupancies[141:143])==True or any(self.train_occ[141:143])==True
                                          or any(self.occupancies[144:150])==True or any(self.train_occ[144-150])==True):
            self.next_authority[141]=False
        else:
            self.next_authority[141]=True
        if self.train_occ[141]==True and (any(self.occupancies[142:143])==True or any(self.train_occ[142:143])==True
                                          or any(self.occupancies[144:150])==True or any(self.train_occ[144-150])==True):
            self.next_authority[142]=False
        else:
            self.next_authority[142]=True
        if self.train_occ[142]==True and (self.occupancies[143]==True or self.train_occ[143]==True
                                          or any(self.occupancies[144:150])==True or any(self.train_occ[144-150])==True):
            self.next_authority[143]=False
        else:
            self.next_authority[143]=True
        if self.train_occ[143]==True and (any(self.occupancies[144:150])==True or any(self.train_occ[144-150])==True):
            self.next_authority[144]=False
        else:
            self.next_authority[144]=True
        #end of zone W
        

        #beginning of zone XYZ (blocks 144-150)
        if self.train_occ[144]==True and (any(self.occupancies[145:150])==True or any(self.train_occ[145:150])==True):
            self.next_authority[145]==False
        else:
            self.next_authority[145]==True
        if self.train_occ[145]==True and (any(self.occupancies[146:150])==True or any(self.train_occ[146:150])==True):
            self.next_authority[146]=False
        else:
            self.next_authority[146]=True
        if self.train_occ[146]==True and (any(self.occupancies[147:150])==True or any(self.train_occ[147:150])==True):
            self.next_authority[147]=False
        else:
            self.next_authority[147]=True
        #look ahead to zone FEDCBA (blocks 28 down to 1)
        if self.train_occ[147]==True and (any(self.occupancies[148:150])==True or any(self.train_occ[148:150])==True
                                          or any(self.occupancies[1:28])==True or any(self.train_occ[1:28])==True):
            self.next_authority[148]=False
        else:
            self.next_authority[148]=True
        if self.train_occ[148]==True and (any(self.occupancies[149:150])==True or any(self.train_occ[149:150])==True
                                          or any(self.occupancies[1:28])==True or any(self.train_occ[1:28])==True):
            self.next_authority[149]=False
        else:
            self.next_authority[149]=True
        if self.train_occ[149]==True and (self.occupancies[150]==True or self.train_occ[150]==True
                                          or any(self.occupancies[1:28])==True):
            self.next_authority[150]=False
        else:
            self.next_authority[150]=True
        #SWITCH 28 must be right (false) before train can go through
        if self.train_occ[150]==True and (any(self.occupancies[1:28])==True or any(self.train_occ[1:28])==True):
            self.next_authority[28]=False
        elif self.train_occ[150]==True and self.switch_28==False and (all(self.occupancies[1:28])==False and all(self.train_occ[1:28])==False):
            self.next_authority[28]=True
        elif self.train_occ[150]==True and self.switch_28==True and (all(self.occupancies[1:28])==False and all(self.train_occ[1:28])==False):
            self.next_authority[28]=False
        else:
            self.next_authority[28]=True
        #end of zone XYZ


        #beginning of zone FEDCBA
        if self.train_occ[28]==True and (any(self.occupancies[1:27])==True or any(self.train_occ[1:27])==True):
            self.next_authority[27]=False
        else:
            self.next_authority[27]=True
        if self.train_occ[27]==True and (any(self.occupancies[1:26])==True or any(self.train_occ[1:26])==True):
            self.next_authority[26]=False
        else:
            self.next_authority[26]=True
        if self.train_occ[26]==True and (any(self.occupancies[1:25])==True or any(self.train_occ[1:25])==True):
            self.next_authority[25]=False
        else:
            self.next_authority[25]=True
        if self.train_occ[25]==True and (any(self.occupancies[1:24])==True or any(self.train_occ[1:24])==True):
            self.next_authority[24]=False
        else:
            self.next_authority[24]=True
        if self.train_occ[24]==True and (any(self.occupancies[1:23])==True or any(self.train_occ[1:23])==True):
            self.next_authority[23]=False
        else:
            self.next_authority[23]=True
        if self.train_occ[23]==True and (any(self.occupancies[1:22])==True or any(self.train_occ[1:22])==True):
            self.next_authority[22]=False
        else:
            self.next_authority[22]=True
        if self.train_occ[22]==True and (any(self.occupancies[1:21])==True or any(self.train_occ[1:21])==True):
            self.next_authority[21]=False
        else:
            self.next_authority[21]=True
        if self.train_occ[21]==True and (any(self.occupancies[1:20])==True or any(self.train_occ[1:20])==True):
            self.next_authority[20]=False
        else:
            self.next_authority[20]=True
        if self.train_occ[20]==True and (any(self.occupancies[1:19])==True or any(self.train_occ[1:19])==True):
            self.next_authority[19]=False
        else:
            self.next_authority[19]=True
        if self.train_occ[19]==True and (any(self.occupancies[1:18])==True or any(self.train_occ[1:18])==True):
            self.next_authority[18]=False
        else:
            self.next_authority[18]=True
        if self.train_occ[18]==True and (any(self.occupancies[1:17])==True or any(self.train_occ[1:17])==True):
            self.next_authority[17]=False
        else:
            self.next_authority[17]=True
        if self.train_occ[17]==True and (any(self.occupancies[1:16])==True or any(self.train_occ[1:16])==True):
            self.next_authority[16]=False
        else:
            self.next_authority[16]=True
        if self.train_occ[16]==True and (any(self.occupancies[1:15])==True or any(self.train_occ[1:15])==True):
            self.next_authority[15]=False
        else:
            self.next_authority[15]=True
        if self.train_occ[15]==True and (any(self.occupancies[1:14])==True or any(self.train_occ[1:14])==True):
            self.next_authority[14]=False
        else:
            self.next_authority[14]=True
        if self.train_occ[14]==True and (any(self.occupancies[1:13])==True or any(self.train_occ[1:13])==True):
            self.next_authority[13]=False
        else:
            self.next_authority[13]=True
        #SWITCH 13 MUST BE LEFT FOR TRAIN TO MOVE FORWARD
        if self.train_occ[13]==True and (any(self.occupancies[1:12])==True or any(self.train_occ[1:12])==True):
            self.next_authority[12]=False
        elif self.train_occ[13]==True and self.switch_13==True and (all(self.occupancies[1:12])==False or all(self.train_occ[1:12])==False):
            self.next_authority[12]=True
        elif self.train_occ[12]==True and self.switch_13==False and (all(self.occupancies[1:12])==False or all(self.train_occ[1:12])==False):
            self.next_authority[12]=False
        else:
            self.next_authority[12]=True
        if self.train_occ[12]==True and (any(self.occupancies[1:11])==True or any(self.train_occ[1:11])==True):
            self.next_authority[11]=False
        else:
            self.next_authority[11]=True
        if self.train_occ[11]==True and (any(self.occupancies[1:10])==True or any(self.train_occ[1:10])==True):
            self.next_authority[10]=False
        else:
            self.next_authority[10]=True
        #....rest of FEDCBA


        #beginning of zone GH (blocks 29-35)
        if self.train_occ[29]==True and (any(self.occupancies[30:35])==True or any(self.train_occ[30:35])==True):
            self.next_authority[30]=False
        else:
            self.next_authority[30]=True
        if self.train_occ[30]==True and (any(self.occupancies[31:35])==True or any(self.train_occ[31:35])==True):
            self.next_authority[31]=False
        else:
            self.next_authority[31]=True
        if self.train_occ[31]==True and (any(self.occupancies[32:35])==True or any(self.train_occ[32:35])==True):
            self.next_authority[32]=False
        else:
            self.next_authority[32]=True
        #look ahead into next zone (blocks 36-46)
        if self.train_occ[32]==True and (any(self.occupancies[33:35])==True or any(self.train_occ[33:35])==True
                                         or any(self.occupancies[36:46])==True or any(self.train_occ[36:46])==True):
            self.next_authority[33]=False
        else:
            self.next_authority[33]=True
        if self.train_occ[33]==True and (any(self.occupancies[34:35])==True or any(self.train_occ[34:35])==True
                                         or any(self.occupancies[36:46])==True or any(self.train_occ[36:46])==True):
            self.next_authority[34]=False
        else:
            self.next_authority[34]=True
        if self.train_occ[34]==True and (self.occupancies[35]==True or self.train_occ[35]==True
                                         or any(self.occupancies[36:46])==True or any(self.train_occ[36:46])==True):
            self.next_authority[35]=False
        else:
            self.next_authority[35]=True
        if self.train_occ[35]==True and (any(self.occupancies[36:46])==True or any(self.train_occ[36:46])==True):
            self.next_authority[36]=False
        else:
            self.next_authority[36]=True
        #end of zone GH


        #beginning of zone I (blocks 36-46)
        if self.train_occ[36]==True and (any(self.occupancies[37:46])==True or any(self.train_occ[37:46])==True):
            self.next_authority[37]=False
        else:
            self.next_authority[37]=True
        if self.train_occ[37]==True and (any(self.occupancies[38:46])==True or any(self.train_occ[38:46])==True):
            self.next_authority[38]=False
        else:
            self.next_authority[38]=True
        if self.train_occ[38]==True and (any(self.occupancies[39:46])==True or any(self.train_occ[39:46])==True):
            self.next_authority[39]=False
        else:
            self.next_authority[39]=True
        if self.train_occ[39]==True and (any(self.occupancies[40:46])==True or any(self.train_occ[40:46])==True):
            self.next_authority[40]=False
        else:
            self.next_authority[40]=True
        if self.train_occ[40]==True and (any(self.occupancies[41:46])==True or any(self.train_occ[41:46])==True):
            self.next_authority[41]=False
        else:
            self.next_authority[41]=True
        if self.train_occ[41]==True and (any(self.occupancies[42:46])==True or any(self.train_occ[42:46])==True):
            self.next_authority[42]=False
        else:
            self.next_authority[42]=True
        if self.train_occ[42]==True and (any(self.occupancies[43:46])==True or any(self.train_occ[43:46])==True):
            self.next_authority[43]=False
        else:
            self.next_authority[43]=True
        if self.train_occ[43]==True and (any(self.occupancies[44:46])==True or any(self.train_occ[44:46])==True):
            self.next_authority[44]=False
        else:
            self.next_authority[44]=True
        if self.train_occ[44]==True and (any(self.occupancies[45:46])==True or any(self.train_occ[45:46])==True):
            self.next_authority[45]=False
        else:
            self.next_authority[45]=True
        if self.train_occ[45]==True and (self.occupancies[46]==True or self.train_occ[46]==True):
            self.next_authority[46]=False
        else:
            self.next_authority[46]=True
        #end of zone I for main wayside