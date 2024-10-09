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
        self.block_error = [False for i in range(17)]
        self.maint_occ = [False for i in range(17)]
        self.train_occ = [False for i in range(17)]

        #stores the switch commands for switch 5
        self.switch_5_queue = SwitchQueue()

        #track state variables
        self.switch_5 = False
        self.signal_6 = False
        self.signal_12 = False
        self.crossing_3 = False

    def dispatch(self, new_route):
        self.switch_5_queue.enqueue(new_route)

    def say_hi(self):
        print("PLC Uploaded Successfully")

    def block_error_check(self):
        #checks every new occupancy to see if a previous block was occupied, if not, track error is detected
        for i in range(1, 6):
            if self.occupancy[i] == True and self.previous_occupancy[i-1] == False and self.previous_occupancy[i] == False:
                self.block_error[i] = True
           
        for i in range(7, 12):
            if self.occupancy[i] == True and self.previous_occupancy[i-1] == False and self.previous_occupancy[i] == False:
                self.block_error[i] = True

        for i in range(13, 17):
            if self.occupancy[i] == True and self.previous_occupancy[i-1] == False and self.previous_occupancy[i] == False:
                self.block_error[i] = True

        if self.occupancy[6] == True and self.previous_occupancy[5] == False and self.previous_occupancy[6] == False:
            self.block_error[6] = True
        
        if self.occupancy[12] == True and self.previous_occupancy[5] == False and self.previous_occupancy[5] == False:
            self.block_error[12] = True

        #resets error state if track error is fixed
        for i in range(17):
            if self.block_error[i] == True and self.occupancy[i] == False:
                self.block_error[i] = False
        
    def update_train_occ(self):
        for i in range(17):
            if self.occupancy[i] == True and self.block_error[i] == False and self.maint_occ[i] == False:
                self.train_occ[i] = True
            else:
                self.train_occ[i] = False

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
        if self.occupancy[5] == False and self.previous_occupancy[5] == True:
            self.switch_5_queue.dequeue()
            if self.switch_5_queue.peek() != None:
                self.switch_5 = self.switch_5_queue.peek()
            else:
                self.switch_5 = False

        #checks for track errors on blocks 6-8, and 12-14, if so, sets the switch to the other direction
        if self.block_error[6] == True or self.block_error[7] == True or self.block_error[8] == True:
            self.switch_5 = False

        if self.block_error[12] == True or self.block_error[13] == True or self.block_error[14] == True:
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
            if i < 6:
                if all(j == False for j in self.occupancy[1:5]):
                    self.next_authority[i] = True
            elif i < 12:
                if all(j == False for j in self.occupancy[6:12]):
                    self.next_authority[i] = True
            else:
                if all(j == False for j in self.occupancy[12:17]):
                    self.next_authority[i] = True
        
        if all(j == False for j in self.occupancy[6:12]) and self.switch_5 == True:
            self.next_authority[5] = True

        if all(j == False for j in self.occupancy[12:17]) and self.switch_5 == False:
            self.next_authority[5] = True

        self.next_authority[11] = False
        self.next_authority[16] = False

    def get_block_info(self):
        return self.occupancy, self.next_authority

                
    def update_track(self, new_blocks):
        self.previous_occupancy = self.occupancy
        self.occupancy = copy.deepcopy(new_blocks)
        self.block_error_check()
        self.update_crossing()
        self.update_switch()
        self.update_signal()
        self.update_authority()
    

        

        




        
        


        
        
        
    
                 
    