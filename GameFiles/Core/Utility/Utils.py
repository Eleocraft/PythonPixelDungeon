import math
import random as prng

def distance(pos1, pos2):
    return math.sqrt((pos2.x - pos1.x) ** 2 + (pos2.y - pos1.y) ** 2)

def RandomFromList(list):
    totalAmount = sum(list)
    randomNumber = prng.randrange(0, totalAmount)
    currentAmount = 0
    for i in range(len(list)):
        if list[i] + currentAmount > randomNumber:
            return i
        else:
            currentAmount += list[i]
    return len(list) - 1
