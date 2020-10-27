from common import Agent, Cell, Board, findNeighboringCoords
from commonCSP import *
import time
import copy
import random as rnd

def strategy2(gboard, dim, agent):
    KB = []
    inferredSafeSet = set()
    r = rnd.randint(0,dim-1)
    c = rnd.randint(0,dim-1)

    while((dim*dim) - len(agent.revealedCoords) - len(agent.identifiedMineCoords) != 0): #run until all cells are explored
        while ((r,c) in agent.revealedCoords or (r,c) in agent.identifiedMineCoords): #pick coordinates again if cell has already been explored
            r = rnd.randint(0,dim-1)
            c = rnd.randint(0,dim-1)
        
        currentCell = agent.checkCell((r,c),gboard) #check the cell at (r, c)

        if (currentCell.type == -1): #the revealed cell is a mine
            newEq = [tupleToIndex(r, c, dim), 1]
            addEq(KB, newEq) #insert the equation [(r, c) = 1] into the KB
        else: #the revealed cell is safe
            newEq1 = [tupleToIndex(r, c, dim), 0]
            addEq(KB, newEq1) #insert the equation [(r, c) = 0] into the KB
            newEq2 = []
            for n in currentCell.neighbors: #find all neighbors of (r, c)
                newEq2.append(tupleToIndex(n[0], n[1], dim))
            newEq2.append(currentCell.type)
            addEq(KB, newEq2) #insert the equation [(neighbor1) + (neighbor2) + ... + (neighborN) = hint] into the KB

        madeInference = True
        while(madeInference):
            madeInference = checkForInference(KB, agent, inferredSafeSet) #check to see if a valid inference can be made
        
        if (len(inferredSafeSet) > 0): #if a cell is inferred to be safe, reveal it next
            (r, c) = inferredSafeSet.pop()

def display(dim,agent):
    numTripped = 0
    numIdentifiedMines = 0
    numRevealed = 0
    display = Board(dim)
    for i in range(0,dim):
        for j in range(0,dim):
            if( (i,j) in agent.trippedMineCoords):
                display.board[i][j] = '2'
                numTripped += 1
            elif((i,j) in agent.identifiedMineCoords):
                display.board[i][j] = '1'
                numIdentifiedMines += 1
            elif((i,j) in agent.revealedCoords):
                display.board[i][j] = '9'
                numRevealed += 1
            else:
                continue
    print(display.board)
    print("Tripped Mines: " + str(numTripped))
    print("Identified Mines: " + str(numIdentifiedMines))
    print("Revealed Cells: " + str(numRevealed))
    print("Identified Mines/Total Mines: " + str(numIdentifiedMines / (numTripped + numIdentifiedMines)))

# dim = 10
# gb = Board(dim)
# gb.set_mines(dim**2 * 0.4)
# print(gb.board)
# ag = Agent(dim)
# startTime = time.time()
# strategy2(gb,dim,ag)
# endTime = time.time()
# display(dim,ag)

dim = 4
numBoards = 100
numTrials = 100
worstBoard = []
worstRate = 1
for _ in range(numBoards):
    godBoard = Board(dim)
    godBoard.set_mines(dim**2 * 0.4)
    avgDetectionRate = 0

    for _ in range(numTrials):
        agent = Agent(dim)
        strategy2(godBoard, dim, agent)
        avgDetectionRate = avgDetectionRate + len(agent.identifiedMineCoords) / (len(agent.identifiedMineCoords) + len(agent.trippedMineCoords))
    avgDetectionRate = avgDetectionRate / numTrials
    if(avgDetectionRate < worstRate):
        worstBoard = copy.deepcopy(godBoard.board) #check if neccessary to deepcopy here
        worstRate = avgDetectionRate

print(worstBoard)
print(worstRate)