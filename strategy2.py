from Agent import Agent,Cell 
from Board import Board, findNeighboringCoords
import random as rnd
import numpy as np

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
            KB = addEq(KB, newEq) #insert the equation [(r, c) = 1] into the KB
        else: #the revealed cell is safe
            newEq1 = [tupleToIndex(r, c, dim), 0]
            KB = addEq(KB, newEq1) #insert the equation [(r, c) = 0] into the KB
            newEq2 = []
            for n in currentCell.neighbors: #find all neighbors of (r, c)
                newEq2.append(tupleToIndex(n[0], n[1], dim))
            newEq2.append(currentCell.type)
            KB = addEq(KB, newEq2) #insert the equation [(neighbor1) + (neighbor2) + ... + (neighborN) = hint] into the KB

        madeInference = True
        while(madeInference):
            (KB, madeInference) = checkForInference(KB, agent, inferredSafeSet) #check to see if a valid inference can be made
        
        if (len(inferredSafeSet) > 0): #if a cell is inferred to be safe, reveal it next
            (r, c) = inferredSafeSet.pop()
        
def addEq(KB, equation): #add an equation to the KB
    equation = reduceEq(KB, equation) #reduce the new equation by every equation in the KB
    if(equation == []): #if the equation is already contained in the KB or gets reduced to nothing, skip
        return KB
    KB = reduceKB(KB, equation) #reduce every equation in the KB by reduced new equation
    KB.append(equation) #insert the new equation into the KB
    return KB

def checkForInference(KB, agent, safeSet):
    madeInference = False
    for eq in KB:
        if (len(eq) - 1 == eq[-1]): #All cells in this eq must be mines
            for var in eq[0 : len(eq) - 1]: #iterate over the variables in eq
                (r, c) = indexToTuple(var, agent.dim)
                if (agent.board[r][c].type != Cell.MINE): #if the cell is not a tripped or inferred mine
                    agent.identifyMine((r, c)) #identify the cell as an inferred mine
                    KB = addEq(KB, [var, 1]) #add the equation [(r, c) = 1] into the KB
                    madeInference = True #flag to indicate an inference has been made
        elif (eq[-1] == 0): #All variables in this eq must be safe
            for var in eq[0 : len(eq) - 1]:
                (r, c) = indexToTuple(var, agent.dim)
                if(agent.board[r][c].revealed == True or (r, c) in safeSet):
                    continue
                KB = addEq(KB, [var, 0])
                safeSet.add((r, c))
                madeInference = True #flag to indicate an inference has been made
    return(KB, madeInference)

#check case when duplicate clues get added
def reduceKB(KB, newEq):
    newKB = []
    modified = []
    for eq in KB:
        if (eq != newEq and set(newEq[0 : len(newEq) - 1]).issubset(set(eq[0 : len(eq) - 1]))): #if newEq is a subset of an equation in KB
            constraintDifference = eq[len(eq) - 1] - newEq[len(newEq) - 1] #store the difference of the constraint values
            e = list(set(eq[0 : len(eq) - 1]) - set(newEq[0 : len(newEq) - 1])) #find the set difference
            e.append(constraintDifference) #append the constaint difference to the end of the equation
            if(e not in newKB):
                newKB.append(e)
                modified.append(e)
        elif(eq not in newKB):
            newKB.append(eq)
    if(modified != []):
        for eq in modified:
            newKB = reduceKB(newKB, eq)
    return newKB

def reduceEq(KB, newEq):
    for eq in KB: #for every equation eq in the KB, reduce the new equation by eq
        if (set(eq[0 : len(eq) - 1]).issubset(set(newEq[0 : len(newEq) - 1]))): #if eq is a subset of the new equation
            constraintDifference = newEq[len(newEq) - 1] - eq[len(eq) - 1] #store the difference of the constraint values
            newEq = list(set(newEq[0 : len(newEq) - 1]) - set(eq[0 : len(eq) - 1])) #find the set difference
            newEq.append(constraintDifference) #append the constaint difference to the end of the equation
    if (len(newEq) < 2):
        return []
    else:
        return newEq

def tupleToIndex(r, c, dim):
    return dim * r + c #converts cell tuples to unique integers

def indexToTuple(i, dim):
    return (int(i / dim), i % dim) #converts the unique integers back into their respective tuples

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

dim = 20
gb = Board(dim)
gb.set_mines(160)

print(gb.board)

ag = Agent(dim)
strategy2(gb,dim,ag)
display(dim,ag)