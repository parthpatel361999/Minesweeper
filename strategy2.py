from common import Agent,Cell 
from common import Board, findNeighboringCoords
import random as rnd
import numpy as np
import time

#TODO resolve KB inefficiency
#Line 80 check order

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
        
def addEq(KB, equation): #add an equation to the KB
    reduceEq(KB, equation) #reduce the new equation by every equation in the KB
    if(len(equation) < 2): #if the equation is already contained in the KB or gets reduced to nothing, skip
        return KB
    reduceKB(KB, equation) #reduce every equation in the KB by reduced new equation
    KB.append(equation) #insert the new equation into the KB

def checkForInference(KB, agent, safeSet):
    madeInference = False
    for eq in KB:
        if (len(eq) - 1 == eq[-1]): #All cells in this eq must be mines
            for var in eq[0 : len(eq) - 1]: #iterate over the variables in eq
                (r, c) = indexToTuple(var, agent.dim)
                if (agent.board[r][c].type != Cell.MINE): #if the cell is not a tripped or inferred mine
                    agent.identifyMine((r, c)) #identify the cell as an inferred mine
                    addEq(KB, [var, 1]) #add the equation [(r, c) = 1] into the KB
                    madeInference = True #flag to indicate an inference has been made
        elif (eq[-1] == 0): #All variables in this eq must be safe
            for var in eq[0 : len(eq) - 1]:
                (r, c) = indexToTuple(var, agent.dim)
                if(agent.board[r][c].revealed == True or (r, c) in safeSet):
                    continue
                addEq(KB, [var, 0])
                safeSet.add((r, c))
                madeInference = True #flag to indicate an inference has been made
    return madeInference

def reduceKB(KB, newEq):
    modified = []
    for i in range(len(KB)):
        newEqLen = len(newEq)
        KBEqLen = len(KB[i])
        if (newEqLen <= KBEqLen and KB[i] != newEq and set(newEq[0 : newEqLen - 1]).issubset(set(KB[i][0 : KBEqLen - 1]))): #if newEq is a subset of an equation in KB
            constraintDifference = KB[i][KBEqLen - 1] - newEq[newEqLen - 1] #store the difference of the constraint values
            e = list(set(KB[i][0 : KBEqLen - 1]) - set(newEq[0 : newEqLen - 1])) #find the set difference
            e.append(constraintDifference) #append the constaint difference to the end of the equation
            if(e not in KB):
                KB[i] = e
                modified.append(e)
            else:
                KB[i] = []
    while([] in KB):
        KB.remove([])
    for E in modified:
        reduceKB(KB, E)

def reduceEq(KB, newEq):
    for eq in KB: #for every equation eq in the KB, reduce the new equation by eq
        eqLen = len(eq)
        newEqLen = len(newEq)
        if (eqLen <= newEqLen and set(eq[0 : eqLen - 1]).issubset(set(newEq[0 : newEqLen - 1]))): #if eq is a subset of the new equation
            #newEqLength = len(newEq)
            constraintDifference = newEq[newEqLen - 1] - eq[eqLen - 1] #store the difference of the constraint values
            newEq.extend(list(set(newEq[0 : newEqLen - 1]) - set(eq[0 : eqLen - 1]))) #find the set difference
            newEq.append(constraintDifference) #append the constaint difference to the end of the equation
            for _ in range(newEqLen):
                newEq.remove(newEq[0])

def tupleToIndex(r, c, dim):
    return dim * r + c #converts cell tuples to unique integers

def indexToTuple(i, dim):
    return (int(i / dim), i % dim) #converts the unique integers back into their respective tuples

# def display(dim,agent):
#     numTripped = 0
#     numIdentifiedMines = 0
#     numRevealed = 0
#     display = Board(dim)
#     for i in range(0,dim):
#         for j in range(0,dim):
#             if( (i,j) in agent.trippedMineCoords):
#                 display.board[i][j] = '2'
#                 numTripped += 1
#             elif((i,j) in agent.identifiedMineCoords):
#                 display.board[i][j] = '1'
#                 numIdentifiedMines += 1
#             elif((i,j) in agent.revealedCoords):
#                 display.board[i][j] = '9'
#                 numRevealed += 1
#             else:
#                 continue
#     print(display.board)
#     print("Tripped Mines: " + str(numTripped))
#     print("Identified Mines: " + str(numIdentifiedMines))
#     print("Revealed Cells: " + str(numRevealed))
#     print("Identified Mines/Total Mines: " + str(numIdentifiedMines / (numTripped + numIdentifiedMines)))

# dim = 30
# gb = Board(dim)
# #gb.set_mines(40)
# gb.set_mines(dim**2 * 0.4)

# #print(gb.board)

# ag = Agent(dim)
# startTime = time.time()
# strategy2(gb,dim,ag)
# endTime = time.time()
# display(dim,ag)
#print("Time taken: " + str(endTime - startTime))