blocks = [False] * 15
num_blocks = len(blocks)
#print(blocks)

#block_to_change = int(input("Input block to change: "))

#blocks[block_to_change - 1] = not(blocks[block_to_change - 1])

#print(blocks)

#simulating a train: 
#first check if speed is safe (max speed of train: 70)
speed = 50
authority = 200
speed_max=70
commanded_speed=0
commanded_authority=0
num_blocks_a=10
#if speed is safe, push it through to track model
if speed <= speed_max:
    commanded_speed=speed
    commanded_authority=authority
else: #if not safe, override it and change to zero
    speed=commanded_speed
    commanded_authority=authority  #either way authority passes through to the track
#for each block (15 in total, 1-10 for wayside a, 1-5 & 11-15 for wayside b)
#we want to check their occupancy so for every 3.6 seconds the train should be moving to the next block
next=0
time=0
while next<num_blocks_a:
    if next == 0:
        print(blocks)
        blocks[next]=not(blocks[next])
        next = next + 1
        time = time + 3.6
    else:
        print(blocks)
        blocks[next]=not(blocks[next])
        blocks[next-1]=not(blocks[next])
        next = next + 1
        time = time + 3.6
print("Time taken to traverse Wayside A: " + str(time) + " seconds")
print("Commanded speed to be sent to track model: " + str(commanded_speed))
print("Commanded authority to be sent to the track model: " + str(commanded_authority))
