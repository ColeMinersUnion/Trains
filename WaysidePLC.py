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
        self.occupancy = [False  for i in range(17)]
        self.next_authority = [False for i in range(17)]
        self.previous_occupancy = [False for i in range(17)]
        self.block_error = [False for i in range(17)]
        self.switch_5_queue = SwitchQueue()
        self.switch_5 = False
        self.signal_6 = False
        self.signal_12 = False
        self.crossing_3 = False

    def dispatch(self, new_route):
        self.switch_5_queue.enqueue(new_route)

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

        #resets error state if track error is fix
        for i in range(17):
            if self.block_error[i] == True and self.occupancy[i] == False:
                self.block_error[i] = False

    def update_crossing(self):
         #checks if the train is within 3 blocks of the crossing, if so sets crossing to true
        if self.occupancy[1] == True or self.occupancy[2] == True or self.occupancy[3] == True or self.occupancy[4] == True or self.occupancy[5] == True:
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
        if self.occupancy[0] == True:
            if any(self.occupancy[1:4]) == True:
                self.next_authority[0] = False
            else:
                self.next_authority[0] = True

        if self.occupancy[1] == True:
            if any(self.occupancy[2:5]) == True:
                self.next_authority[1] = False
            else:
                self.next_authority[1] = True

        if self.occupancy[2] == True:
            if any(self.occupancy[3:6]) == True:
                self.next_authority[2] = False
            else:
                self.next_authority[2] = True

        if self.occupancy[3] == True:
            if any(self.occupancy[4:6]) == True:
                self.next_authority[3] = False
            else:
                self.next_authority[3] = True
            
            if self.switch_5 == False and self.occupancy[12] == True:
                self.next_authority[3] = False
            
            if self.switch_5 == True and self.occupancy[6] == True:
                self.next_authority[3] = False
        
        if self.occupancy[4] == True:
            if self.occupancy[5] == True:
                self.next_authority[4] = False
            else:
                self.next_authority[4] = True
            
            if self.switch_5 == False and any(self.occupancy[12:14]) == True:
                self.next_authority[4] = False

            if self.switch_5 == True and any(self.occupancy[6:8]) == True:
                self.next_authority[4] = False
        
        if self.occupancy[5] == True:
            if self.switch_5 == False and any(self.occupancy[12:15]) == True:
                self.next_authority[5] = False

            if self.switch_5 == True and any(self.occupancy[6:9]) == True:
                self.next_authority[5] = False
            else:
                self.next_authority[5] = True
        
        if self.occupancy[6] == True:
            if any(self.occupancy[7:10]) == True:
                self.next_authority[6] = False
            else:
                self.next_authority[6] = True
        
        if self.occupancy[7] == True:
            if any(self.occupancy[8:11]) == True:
                self.next_authority[7] = False
            else:
                self.next_authority[7] = True

        if self.occupancy[8] == True:
            if any(self.occupancy[9:12]) == True:
                self.next_authority[8] = False
            else:
                self.next_authority[8] = True
        
        if self.occupancy[9] == True:
            if any(self.occupancy[10:12]) == True:
                self.next_authority[9] = False
            else:
                self.next_authority[9] = True
        
        if self.occupancy[10] == True:
            if self.occupancy[11] == True:
                self.next_authority[10] = False
            else:
                self.next_authority[10] = True
        
        if self.occupancy[11] == True:
            self.next_authority[11] = True


        if self.occupancy[12] == True:
            if any(self.occupancy[13:16]) == True:
                self.next_authority[12] = False
            else:
                self.next_authority[12] = True
        
        if self.occupancy[13] == True:
            if any(self.occupancy[14:17]) == True:
                self.next_authority[13] = False
            else:
                self.next_authority[13] = True
        
        if self.occupancy[14] == True:
            if any(self.occupancy[15:17]) == True:
                self.next_authority[14] = False
            else:
                self.next_authority[14] = True
        
        if self.occupancy[15] == True:
            if self.occupancy[16] == True:
                self.next_authority[15] = False
            else:
                self.next_authority[15] = True
        
        if self.occupancy[16] == True:
            self.next_authority[16] = True

                
    def update_track(self, new_blocks):
        self.previous_occupancy = self.occupancy
        self.occupancy = copy.deepcopy(new_blocks)
        self.next_authority = [False for i in range(17)]
        self.block_error_check()
        self.update_crossing()
        self.update_switch()
        self.update_signal()
        self.update_authority()

        

        




        
        


        
        
        
    
                 
    