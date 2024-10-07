
from WaysidePLC import BluePLC

# class Train:
#     train_id = 0
#     def __init__(self, speed, authority, plc):
#         Train.train_id += 1
#         self.id = Train.train_id
#         self.speed = speed
#         self.authority = authority
#         self.current_block = 0
#         self.plc = plc


#     def move(self):
#         if(self.plc.next_authority[self.current_block] == True):
#             self.current_block += 1
#             print("Train", self.id, " has moved to block ", self.current_block)

def print_PLC(plc):

    print("Occupancy: ")
    for i in range(17):
        print(i, ":", plc.occupancy[i], end = " | ")
    print("\n")

    print("Next Authority: ")
    for i in range(17):
        if plc.occupancy[i] == True:
            print(i, ":", plc.next_authority[i], end = " ")
    print("\n")

    
    print("Block Error: ")
    for i in range(17):
        if plc.block_error[i] == True:
            print(i, ":", plc.block_error[i], end = " ")
    print("\n")

    print("Switch 5: ", plc.switch_5)
    print("Signal 6: ", plc.signal_6)
    print("Signal 12: ", plc.signal_12)
    print("Crossing 3: ", plc.crossing_3)
 

def main():
    #Main TestBench Flow
    plc = BluePLC()
    tm_occupancy = [False for i in range(17)]
    trains = []
    print_PLC(plc)
    while True:
        if plc.occupancy[0] == False and plc.occupancy[1] == False and plc.occupancy[2] == False:
            print("Dispatch Train? (y/n)")

            if input() == "y":
                switch = input("Enter switch (False/True): ")
                if switch == "False":
                    plc.dispatch(False)
                elif switch == "True":
                    plc.dispatch(True)
    
                tm_occupancy[0] = True
                plc.update_track(tm_occupancy)
                trains.append(0)
            print_PLC(plc)    
        else:
            print("Cannot dispatch train")
        
        for i in range(len(trains)):
            if plc.next_authority[trains[i]] == True:
                tm_occupancy[trains[i]] = False
                tm_occupancy[trains[i] + 1] = True
                if trains[i] == 5 and plc.switch_5 == False:
                    print("Train at block", trains[i], " has moved to block ", 12)
                    trains[i] = 12
                else:
                    print("Train at block", trains[i], " has moved to block ", trains[i] + 1)
                    trains[i] += 1
                
        
        plc.update_track(tm_occupancy)
        print_PLC(plc)
        print("Continue? (y/n)")
        if input() == "n":
            break


if __name__ == "__main__":
    main()



            