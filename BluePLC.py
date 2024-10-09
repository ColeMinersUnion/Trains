#A class that contains a queue of booleans values that represent the switch commands
import copy
class SwitchQueue:
    def __init__(self):
        self.queue = []
            
    def enqueue(self, route):
        self.queue.append(route)
            
    def dequeue(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        else:
            return None
        
    def peek(self):
        if len(self.queue) > 0:
            return self.queue[0]
        else:
            return None
            
    
class BluePLC:
    def __init__(self):
        #stores the occupancy of each block
        self.occupancy = [False  for i in range(17)]

        #stores the boolean authority of each block, false values are based on the "zones" that only one train can occupy at a time
        self.next_authority = [False for i in range(17)]

        #stores the previous occupancy of each block, used in track error detection
        self.previous_occupancy = [False for i in range(17)]
        #stores any block errors
        self.block_error = [False for i in range(17)]
        #stores maintenance occupancy of each block
        self.maint_occ = [False for i in range(17)]
        #stores train occupancy for each block
        self.train_occ = [False for i in range(17)]

        #stores the switch commands for switch 5
        self.switch_5_queue = SwitchQueue()

        #track state variables
        self.switch_5 = False
        self.signal_6 = False
        self.signal_12 = False
        self.crossing_3 = False
    #pushes the route of the train to the queue for the switch on block 5 when it reaches the switch
    def dispatch(self, new_route):
        self.switch_5_queue.enqueue(new_route)

    #confirms that the PLC is successfully uploaded
    def say_hi(self):
        print("PLC Uploaded Successfully")

    def block_error_check(self):
        #checks if the occupancy of a block has changed, if so, sets the block error to true
        for i in range(17):
            if self.occupancy[i] == True and self.train_occ[i] == False and self.maint_occ[i] == False:
                self.block_error[i] = True
            else:
                self.block_error[i] = False
    #updates train occupancy as the train moves through the blue line    
    def update_train_occ(self):
        if self.occupancy[0] == True:
            self.train_occ[0] = True
        #updates train occupancy at blocks 12 and 5 based upon block occupancies of 12 and 5 and the switch state at block 5
        #boolean values for the switch state: left=true, right=false
        for i in range(1, 17):
            if  i == 12:
                if self.train_occ[5] == True and self.occupancy[5] == False and self.occupancy[12] == True and self.switch_5 == False:
                    self.train_occ[12] = True
                    self.train_occ[5] = False
            elif  i == 6:
                if self.train_occ[5] == True and self.occupancy[5] == False and self.occupancy[6] == True and self.switch_5 == True:
                    self.train_occ[6] = True
                    self.train_occ[5] = False
            #for the rest of the blocks, updates the train occupancy as it moves along the track
            #we are assuming for right now that the train is only the length of one block to simplify things
            elif self.train_occ[i - 1] == True and self.occupancy[i] == True:
                self.train_occ[i] = True
                self.train_occ[i - 1] = False
    #updates the maintenance occupancy of the blocks
    def update_maint_occ(self, proposed_maint):
        for i in range(17):
            #updates the maintenance occupancy to false if suggested
            if proposed_maint[i] == False:
                self.maint_occ[i] = False
            #if both proposed maintenance and current maintenance occupancies are true, do nothing
            elif proposed_maint[i] == True and self.maint_occ[i] == True:
                pass
            #if proposed maintenance is true and does not match the current maintenance occupancy 
            #then check the blocks before the signals (blocks 6 and 12)
            elif proposed_maint[i] == True and self.maint_occ[i] == False:
                #if the current block is before block 6 and all blocks have a false train occupancy
                #assign the block's maintenance occupancy to true
                #do the same if the block is before block 12 and all blocks from 6 to 12 have false train occupancies
                #otherwise assign a true maintenance occupancy if all blocks from 12-17 have false train occupancies
                if i < 6:
                    if all(j == False for j in self.train_occ[1:6]):
                        self.maint_occ[i] = True
                elif i < 12:
                    if all(j == False for j in self.train_occ[6:12]):
                        self.maint_occ[i] = True
                else:
                    if all(j == False for j in self.train_occ[12:17]):
                        self.maint_occ[i] = True

        
    def update_crossing(self):
         #checks if the train is within 3 blocks of the crossing, if so sets crossing to true
        if self.train_occ[1] == True or self.train_occ[2] == True or self.train_occ[3] == True or self.train_occ[4] == True or self.train_occ[5] == True:
            self.crossing_3 = True
        else:
            self.crossing_3 = False
    
    def update_switch(self):
        #checks if the switch queue is not empty, if not, sets switch 5 to the command at the top of the queue
        if self.switch_5_queue.peek() != None:
            self.switch_5 = self.switch_5_queue.peek()
        else:
            self.switch_5 = False
        
        #checks if a train has passed block 5, then takes in the next switch commmand in the queue
        if self.train_occ[6] == True or self.train_occ[12] == True:
            self.switch_5_queue.dequeue()
            if self.switch_5_queue.peek() != None:
                self.switch_5 = self.switch_5_queue.peek()
            else:
                self.switch_5 = False

        #checks for track errors on blocks 6-8, and 12-14, if so, sets the switch to the other direction
        if any(self.block_error[6:12]) == True or any(self.maint_occ[6:12]) == True:
            self.switch_5 = False

        if any(self.block_error[12:17]) == True or any(self.maint_occ[12:17]) == True:
            self.switch_5 = True

    def update_signal(self):
        #sets signal 6 to true and signal 12 to false if switch is true, and vice versa
        if self.switch_5 == True:
            self.signal_6 = True
            self.signal_12 = False
        else:
            self.signal_6 = False
            self.signal_12 = True

        #sets signal 6 to false if there is a block occupancy from 6-11
        for i in range(6, 12):
            if self.occupancy[i] == True:
                self.signal_6 = False
        
        #sets signal 12 to false if there is a block occupancy from 12-16
        for i in range(12, 17):
            if self.occupancy[i] == True:
                self.signal_12 = False
    
    def update_authority(self):
        #determines if each occupied block has the authority to move to the next block, this is layout dependent so it is hardcoded

        #resets the authority to false initally
        self.next_authority = [False for i in range(17)]  
  
        for i in range(17):
            if self.occupancy[i] == True:    
                if i < 6 and i != 5:
                    if all(j == False for j in self.occupancy[i+1:5]):
                        self.next_authority[i] = True
                elif i < 12 and i != 5:
                    if all(j == False for j in self.occupancy[i+1:12]):
                        self.next_authority[i] = True
                elif i < 16 and i != 5:
                    if all(j == False for j in self.occupancy[i+1:17]):
                        self.next_authority[i] = True
            
                if i == 5 and all(j == False for j in self.occupancy[6:12]) and self.switch_5 == True:
                    self.next_authority[5] = True


                if i == 5 and all(j == False for j in self.occupancy[12:17]) and self.switch_5 == False:
                    self.next_authority[5] = True

        self.next_authority[11] = False
        self.next_authority[16] = False

    def get_next_authority(self):
        return self.next_authority

                
    def update_track(self, new_blocks):
        self.previous_occupancy = self.occupancy
        self.occupancy = copy.deepcopy(new_blocks)
        self.update_train_occ()
        #self.update_maint_occ()
        self.block_error_check()
        self.update_crossing()
        self.update_switch()
        self.update_signal()
        self.update_authority()
        # print("occ", self.occupancy)
        # print("auth", self.next_authority)


        

        




        
        


        
        
        
    
                 
    