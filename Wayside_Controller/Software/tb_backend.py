#test case 1
#tests: authority, switches, signals and crossings with empty track and edge cases that test switch states
#from SoftwareShell import WaysideShell
from GreenMainPLC import GreenPLC

def main():
    occ=[False for i in range(151)]
    sw77=False
    sw85=False
    sw28=False
    sw13=False
    #ws=WaysideShell()
    plc=GreenPLC()
    #testing individual functions that update authority, switches, signals, crossings:
    '''auth=plc.update_authority(occ)
    for i in range(151):
        print(f"Green Line Authority Block {i}: {auth[i]} ")
    
    switch77,switch85,switch28,switch13=plc.update_switch(occ)
    print(f"Switch 77: {switch77}, \nSwitch 85: {switch85}, \nSwitch 28: {switch28}, \nSwitch 13: {switch13}")

    signal77,signal85,signal28,signal13=plc.update_signal(switch77,switch85,switch28,switch13)
    print(f"Signal 77: {signal77}, \nSignal 85: {signal85}, \nSignal 28: {signal28}, \nSignal 13: {signal13}")

    crossing19,crossing108=plc.update_crossing(occ)
    print(f"Crossing 19: {crossing19}, \nCrossing 108: {crossing108}")'''

    #testing update_values function that should update all authority, switches, signals, crossings:
    auth,switch77,switch85,switch28,switch13,signal77,signal85,signal28,signal13,crossing19,crossing108=plc.update_values(occ)
    for i in range(151):
        print(f"Green Line Authority Block {i}: {auth[i]} ")
    print(f"Switch 77: {switch77}, \nSwitch 85: {switch85}, \nSwitch 28: {switch28}, \nSwitch 13: {switch13}")
    print(f"Signal 77: {signal77}, \nSignal 85: {signal85}, \nSignal 28: {signal28}, \nSignal 13: {signal13}")
    print(f"Crossing 19: {crossing19}, \nCrossing 108: {crossing108}")

if __name__== "__main__":
    main()