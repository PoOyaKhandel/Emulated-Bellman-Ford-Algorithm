"""
Emulated Bellman-Ford Algorithm
PoOya Khandel, Mohammad Hossein Tavakoli Bina
"""
from BellmanFord import BFA
import msvcrt
import re

whichPort = {}
adrToName = {}
routerCount = 0
hit = None
routerName = input("Welcome to Emulated Bellman-Ford Algorithm\n"
                   "Which router am I?")

with open("which_port.txt") as whichRouter:
    for lines in whichRouter:
        whichPort[lines[0]] = int(lines[2:6])
        adrToName[int(lines[2:6])] = int(lines[0])
        routerCount += 1

myLine = open("adj_mat.txt").readlines()[int(routerName) - 1]
myLine = myLine.rstrip('\n')
firstCost = re.split(" ", myLine)
print(firstCost)

myBf = BFA(routerCount, firstCost, routerName, whichPort, adrToName)
myBf.who_to_send()
s = input("To start BellmanFort Algorithm, Press 's'\n")
while not(s == 's'):
    s = input("you should enter 's'\n")
while True:
    hit = msvcrt.kbhit()
    myBf.send()
    myBf.receive()
    if hit:
        key = ord(msvcrt.getch())
        if key == ord('u'):
            myLine = open("adj_mat.txt").readlines()[int(routerName) - 1]
            newCost = [myLine[2 * m] for m in range(routerCount)]
            myBf.check_cost(newCost)
