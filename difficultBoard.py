from common import Agent, Cell, Board, findNeighboringCoords
from commonCSP import *
import random as rnd
import operator as op
from functools import reduce
import time
import copy

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
'''
def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom

def totalEuclid(board):
    mines = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == -1:
                mines.append((i, j))
    total = 0
    for i in range(len(mines)):
        for j in range(i + 1, len(mines)):
            (r1, c1) = mines[i]
            (r2, c2) = mines[j]
            total = total + ((r1-r2)**2 + (c1-c2)**2)**0.5
    return total

def localSearch(dim, numMines, numRestarts):
    worstDetectionRate = 1
    worstBoard = []
    numTrials = 20
    for _ in range(numRestarts):
        godBoard = Board(dim)
        godBoard.set_mines(dim**2 * 0.4) #check for unique config
        for _ in range(numTrials):
            agent = Agent(dim)
            strategy2(godBoard, dim, agent)
            avgDetectionRate = avgDetectionRate + len(agent.identifiedMineCoords) / (len(agent.identifiedMineCoords) + len(agent.trippedMineCoords))
        avgDetectionRate = avgDetectionRate / numTrials
        if(avgDetectionRate < worstDetectionRate):
            worstBoard = copy.deepcopy(godBoard.board) #check if neccessary to deepcopy here
            worstDetectionRate = avgDetectionRate
'''
#created set_specific_mines()
#created totalEuclid()

"""Brute Force checker
dim = 3
numBoards = 100
numTrials = 30
worstBoard = []
worstRate = 1
boardSet = []
for i in range(numBoards):
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
"""
def diffBoard(rnd_starts,dim):
    mdensity = int( 0.4*dim**2 )
    agent = Agent(dim)
    startBoard = Board(dim)
    startBoard.set_mines(mdensity)
    baseRate = simulate(startBoard)
    triedconfigs = set() #holds new row,cols
    i = 0 
    for row,col in startBoard.minelist:
        print(row,col)
        r = c = 0
        mutate((row,col),startBoard.minelist)
        i = i + 1


    # first generate random board
    # in a do while type of loop (runs for rnd_start iterations)
        # run strategy 2 30 times (simulate function ret type: float)
        #calculate the average detection rate
        # mutate the board:
            # keep moving mine with wraparounds (left)
            # if there is a mine hop over the mine


    strategy2(startBoard, dim, agent)

def simulate(startBoard, dim): #returns float
    i = 0
    detectionRate = 0
    while (i < 30):
        agent = Agent(dim)
        strategy2(startBoard, dim, agent)
        detectionRate += len(agent.identifiedMineCoords) / (len(agent.identifiedMineCoords) + len(agent.trippedMineCoords))
        i += 1
    return float(detectionRate) / 30
    
def mutate((r,c), minelist,baserate,triedconfigs,dim, index_minelist)): 
    #TODO fix this

    #will return the mutated board. 1 cell has changed location.
    #move r,c left (c-1)
    #generate a new board, set all the mines except for r,c where set r,c-1 
    #check if there is a mine there, if yes, then set at r, c-2
    #if r,c at this point is at 
    i = 1 
    br = baserate
    ml2 = minelist.copy()
    while (i < dim):
        newc = c - i
        if (newc < 0):
            newc = dim + newc
        
        if ((r,newc) in minelist):
            continue
        
        else:
            minelist.remove((r,c))
            minelist.add((r,newc))
            newboard = Board(dim)
            newboard.set_specific_mines(minelist)
            newrate = simulate(newboard)
            if(newrate <= br):
                br = newrate
                ml2 = minelist
            c = newc
        i = i + 1

    
    return newrate 

    


print(totalEuclid(worstBoard))