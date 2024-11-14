def offset(angle):
    x=angle
    if(x<0): #min angle check
        x=x+360
    if(x>360): #max angle check
        x=x-360
    if(x>315):
        return 1 - ((x - 315)/45)
    if(x>225):
        return 1
    if(x>180):
        return (x-180)/45
    return 0



for i in range(17):
    print(str(i*22.5) + "\t" + str(offset(i*22.5)) + "\n")