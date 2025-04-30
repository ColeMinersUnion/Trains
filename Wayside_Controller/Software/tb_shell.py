#this is the testbench for the software implementation of the wayside shell and plc
from testShell import WaysideShell
#from GreenMainPLC import GreenPLC 

def main():
    # unit test for wayside software module
    # testing the intake of a list of block occupancies from the track model 
    # and producing correct values for updated authority, switch states, signals, and crossings 
    # for the green line

    occ=[False for i in range(151)]
    occ2=[False,False,True,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,True,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,True,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,False]
    
    occ3=[False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,True,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,True,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,True,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,False]
    
    occ4=[False,True,False,False,False,
          False,False,False,False,False,
          False,False,True,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,
          False,False,False,False,False,False]
    sh=WaysideShell()
    #sh=shell()
    new_occ,auth,switch77,switch85,switch28,switch13,signal77,signal85,signal28,signal13,crossing19,crossing108=sh.update_occupancy(occ4)

    '''for i in range(151):
        print(f"Green Line Authority Block {i}: {auth[i]} ")
    
    print(f"Switches: {switch77}, {switch85}, {switch28}, {switch13}")
    print(f"Signals: {signal77}, {signal85}, {signal28}, {signal13}")
    print(f"Crossings: {crossing19}, {crossing108}")'''
    for i in range(41):
        print(f"Occupancy Block {i}: {new_occ[i]} ")
    for i in range(69,151):
        print(f"Occupancy Block {i}: {new_occ[i]} ")
    for i in range(151):
        print(f"Green Line Authority Block {i}: {auth[i]} ")
    print(f"Switch 77: {switch77}, \nSwitch 85: {switch85}, \nSwitch 28: {switch28}, \nSwitch 13: {switch13}")
    print(f"Signal 77: {signal77}, \nSignal 85: {signal85}, \nSignal 28: {signal28}, \nSignal 13: {signal13}")
    print(f"Crossing 19: {crossing19}, \nCrossing 108: {crossing108}")

if __name__== "__main__":
    main()