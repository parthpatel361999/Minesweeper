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

def diffBoard(rnd_starts,dim):
    mdensity = int( 0.4*dim**2 )
    startBoard = Board(dim)
    startBoard.set_mines(mdensity)
    baseRate = simulate(startBoard,dim)
    print("baseRate: " + str(baseRate))
    for coord in startBoard.minelist:
        baseRate = mutate(coord,startBoard.minelist,baseRate,dim)
    difficult = Board(dim)
    difficult.set_specific_mines(startBoard.minelist)
    print(difficult.board)
    print("Forced Rate:" + str(baseRate))
        


def simulate(startBoard, dim): #returns float
    i = 0
    detectionRate = 0
    num_trials = 30
    while (i < num_trials):
        agent = Agent(dim)
        strategy2(startBoard, dim, agent)
        detectionRate += len(agent.identifiedMineCoords) / (len(agent.identifiedMineCoords) + len(agent.trippedMineCoords))
        i += 1
    return float(detectionRate) / num_trials
    
def mutate(coord, minelist,baserate,dim):
    i = 1
    r,c = coord 
    newrate = baserate
    changedCoord = [coord]
    while i <= dim:
        newc = c - i
        if(newc < 0):
            newc = dim + newc 
        if((r,newc) in minelist):
            i += 1
            continue
        minelist[minelist.index((r,c))] = (r,newc)
        mutatedBoard = Board(dim)
        mutatedBoard.set_specific_mines(minelist)
        mutatedRate = simulate(mutatedBoard,dim) #print(mutatedRate)
        if (mutatedRate <= newrate):
            newrate = mutatedRate
            changedCoord.clear()
            changedCoord.append((r,newc))
        c = newc
        i += 1
    #print(minelist) #print(changedCoord)
    minelist[minelist.index((r,c))] = changedCoord[0]
    return newrate

startTime = time.time()
diffBoard(0,10) 
print(time.time() - startTime)