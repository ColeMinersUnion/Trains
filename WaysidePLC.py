#A class that contains a queue of booleans values that represent the switch commands

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
        self.switch_5 = SwitchQueue()
        self.signal_6 = False
        self.signal_12 = False
        self.crossing_3 = False

    def dispatch(self, new_route):
        self.switch_5.enqueue(new_route)
    
    def update_track(self, new_blocks):
        self.previous_occupancy = self.occupancy
        self.occupancy = new_blocks
        self.next_authority = [False for i in range(17)]
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
            
    def main_check(self, new_blocks):
        self.update_track(new_blocks)


        

        
        
        
    
                 
    