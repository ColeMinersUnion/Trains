blocks = [False] * 15
print(blocks)

block_to_change = int(input("Input block to change: "))

blocks[block_to_change - 1] = not(blocks[block_to_change - 1])

print(blocks)