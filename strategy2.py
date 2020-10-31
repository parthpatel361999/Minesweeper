import random as rnd
import time

import numpy as np

from common import Agent, Board, Cell, findNeighboringCoords
from visualization import Visualizer


def strategy2(gboard, dim, agent, visualization):
    KB = []
    inferredSafeSet = set()
    r = rnd.randint(0, dim-1)
    c = rnd.randint(0, dim-1)

    # run until all cells are explored
    while((dim*dim) - len(agent.revealedCoords) - len(agent.identifiedMineCoords) != 0):
        # pick coordinates again if cell has already been explored
        while ((r, c) in agent.revealedCoords or (r, c) in agent.identifiedMineCoords):
            r = rnd.randint(0, dim-1)
            c = rnd.randint(0, dim-1)

        currentCell = agent.checkCell(
            (r, c), gboard)  # check the cell at (r, c)
        visualization.createVisualization()

        if (currentCell.type == -1):  # the revealed cell is a mine
            newEq = [tupleToIndex(r, c, dim), 1]
            addEq(KB, newEq)  # insert the equation [(r, c) = 1] into the KB
        else:  # the revealed cell is safe
            newEq1 = [tupleToIndex(r, c, dim), 0]
            addEq(KB, newEq1)  # insert the equation [(r, c) = 0] into the KB
            newEq2 = []
            for n in currentCell.neighbors:  # find all neighbors of (r, c)
                newEq2.append(tupleToIndex(n[0], n[1], dim))
            newEq2.append(currentCell.type)
            # insert the equation [(neighbor1) + (neighbor2) + ... + (neighborN) = hint] into the KB
            addEq(KB, newEq2)

        madeInference = True
        while(madeInference):
            # check to see if a valid inference can be made
            madeInference = checkForInference(
                KB, agent, inferredSafeSet, visualization)

        if (len(inferredSafeSet) > 0):  # if a cell is inferred to be safe, reveal it next
            (r, c) = inferredSafeSet.pop()


def addEq(KB, equation):  # add an equation to the KB
    # reduce the new equation by every equation in the KB
    reduceEq(KB, equation)
    if(len(equation) < 2):  # if the equation is already contained in the KB or gets reduced to nothing, skip
        return KB
    # reduce every equation in the KB by reduced new equation
    reduceKB(KB, equation)
    KB.append(equation)  # insert the new equation into the KB


def checkForInference(KB, agent, safeSet, visualization):
    madeInference = False
    for eq in KB:
        if (len(eq) - 1 == eq[-1]):  # All cells in this eq must be mines
            for var in eq[0: len(eq) - 1]:  # iterate over the variables in eq
                (r, c) = indexToTuple(var, agent.dim)
                # if the cell is not a tripped or inferred mine
                if (agent.board[r][c].type != Cell.MINE):
                    # identify the cell as an inferred mine
                    agent.identifyMine((r, c))
                    visualization.createVisualization()
                    # add the equation [(r, c) = 1] into the KB
                    addEq(KB, [var, 1])
                    madeInference = True  # flag to indicate an inference has been made
        elif (eq[-1] == 0):  # All variables in this eq must be safe
            for var in eq[0: len(eq) - 1]:
                (r, c) = indexToTuple(var, agent.dim)
                if(agent.board[r][c].revealed == True or (r, c) in safeSet):
                    continue
                addEq(KB, [var, 0])
                safeSet.add((r, c))
                madeInference = True  # flag to indicate an inference has been made
    return madeInference


def reduceKB(KB, newEq):
    modified = []
    for i in range(len(KB)):
        newEqLen = len(newEq)
        KBEqLen = len(KB[i])
        # if newEq is a subset of an equation in KB
        if (newEqLen <= KBEqLen and KB[i] != newEq and set(newEq[0: newEqLen - 1]).issubset(set(KB[i][0: KBEqLen - 1]))):
            # store the difference of the constraint values
            constraintDifference = KB[i][KBEqLen - 1] - newEq[newEqLen - 1]
            # find the set difference
            e = list(set(KB[i][0: KBEqLen - 1]) - set(newEq[0: newEqLen - 1]))
            # append the constaint difference to the end of the equation
            e.append(constraintDifference)
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
    for eq in KB:  # for every equation eq in the KB, reduce the new equation by eq
        eqLen = len(eq)
        newEqLen = len(newEq)
        # if eq is a subset of the new equation
        if (eqLen <= newEqLen and set(eq[0: eqLen - 1]).issubset(set(newEq[0: newEqLen - 1]))):
            #newEqLength = len(newEq)
            # store the difference of the constraint values
            constraintDifference = newEq[newEqLen - 1] - eq[eqLen - 1]
            # find the set difference
            newEq.extend(
                list(set(newEq[0: newEqLen - 1]) - set(eq[0: eqLen - 1])))
            # append the constaint difference to the end of the equation
            newEq.append(constraintDifference)
            for _ in range(newEqLen):
                newEq.remove(newEq[0])


def tupleToIndex(r, c, dim):
    return dim * r + c  # converts cell tuples to unique integers


def indexToTuple(i, dim):
    # converts the unique integers back into their respective tuples
    return (int(i / dim), i % dim)

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


dim = 10
gb = Board(dim)
# gb.set_mines(40)
gb.set_mines(dim**2 * 0.4)

# print(gb.board)

ag = Agent(dim)
vis = Visualizer(ag, 2)
startTime = time.time()
strategy2(gb, dim, ag, vis)
endTime = time.time()
#print("Time taken: " + str(endTime - startTime))
