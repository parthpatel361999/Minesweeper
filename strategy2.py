from common import Agent, Cell, Board, findNeighboringCoords, display
from commonCSP import addEq, reduceKB, reduceEq, tupleToIndex, indexToTuple
import random as rnd
import numpy as np
import time

'''
Run strategy 2. 
1. Select a random unvisited cell
2. Reveal the cell
3. If the cell is a mine cell, add the equation [var, 1] to the Knowledge Base
   If the cell is a safe cell, add the equations [var, 0] and [(neighbors of var), var's clue] to the Knowledge Base
4. Check if any inferences can be made from the Knowledge Base
5. If a cell has been inferred to be safe, reveal it in the next iteration
   Else, pick a random unvisited cell for the next iteration
'''

def strategy2(gboard, dim, agent):
    KB = []
    inferredSafeSet = set()
    r = rnd.randint(0,dim-1)
    c = rnd.randint(0,dim-1)

    while((dim*dim) - len(agent.revealedCoords) - len(agent.identifiedMineCoords) != 0):
        #Pick an unvisited cell
        while ((r,c) in agent.revealedCoords or (r,c) in agent.identifiedMineCoords): 
            r = rnd.randint(0,dim-1)
            c = rnd.randint(0,dim-1)
        
        #Check the cell at (r, c)
        currentCell = agent.checkCell((r,c),gboard) 

        #if the cell is a mine
        if (currentCell.type == -1):
            newEq = [tupleToIndex(r, c, dim), 1]
            #insert the equation [(r, c) = 1] into the KB
            addEq(KB, newEq) 
        #if the revealed cell is safe
        else: 
            newEq1 = [tupleToIndex(r, c, dim), 0]
            #insert the equation [(r, c) = 0] into the KB
            addEq(KB, newEq1) 
            newEq2 = []
            #find all neighbors of (r, c)
            for n in currentCell.neighbors:
                newEq2.append(tupleToIndex(n[0], n[1], dim))
            newEq2.append(currentCell.type)
            #insert the equation [(neighbor1) + (neighbor2) + ... + (neighborN) = hint] into the KB
            addEq(KB, newEq2) 

        madeInference = True
        while(madeInference):
            #check to see if a valid inference can be made
            madeInference = checkForInference(KB, agent, inferredSafeSet) 
        
        #if a cell is inferred to be safe, reveal it next
        if (len(inferredSafeSet) > 0): 
            (r, c) = inferredSafeSet.pop()

'''
Check if any inferences can be made from the Knowledge Base
If the clue value of an equation is equal to the number of variables in that equation
    Infer all of those variables to be mine cells.
    Add the corresponding mine equations to the Knowledge Base
If the clue value of an equation is 0
    Infer all of those variables to be safe cells.
    Add the corresponding safe equations to the Knowledge Base
'''

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