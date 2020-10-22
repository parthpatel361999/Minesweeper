import copy
import random as rnd
from collections import deque

from Agent import Agent, Cell
from Board import Board
from strategy2 import addEq, indexToTuple, tupleToIndex

"""
    KB = []
    varList = []
    simulatedBombVars = []
    bombCounts = {}
    -----------
    validConfigs = 0
    -----------
    1. add first var in varList to KB as safe (var = 0)
    2. if leaf node:
        a. if valid config:
            i. validConfigs += 1
            ii. for var in simulatedBombVars: bombCounts[var] += 1
    3. else:
        a. if valid config:
            validConfigts += function(KB, varList[1, end], simulatedBombVars, bombVars)
    4. add first var in varList to KB as bomb (var = 1)
    5. add var to simulatedBombVars
    6. if leaf node:
        a. if valid config:
            i. validConfigs += 1
            ii. for var in simulatedBombVars: bombCounts[var] += 1
    7. else:
        a. if valid config:
            validConfigs += function(KB, varList[1, end], simulatedBombVars, bombVars)
    8. return validConfigs        

"""


def configIsValid(KB):
    for eq in KB:
        if len(eq) - 1 > eq[-1] or eq[-1] < 0:
            return False
    return True


def findValidConfigs(KB, variables, simulatedBombVariables, bombCounts):
    validConfigs = 0
    variable = variables[0]

    safeEq = [variable, 0]
    safeKB = copy.deepcopy(KB)
    safeKB = addEq(safeKB, safeEq)
    safeConfigIsValid = configIsValid(safeKB)
    if len(variables) == 1 and safeConfigIsValid:
        validConfigs += 1
        for bombVar in simulatedBombVariables:
            bombCounts[bombVar] += 1
    elif safeConfigIsValid:
        validConfigs += findValidConfigs(
            safeKB, variables[1:], simulatedBombVariables.copy(), bombCounts)

    bombEq = [variable, 1]
    bombKB = copy.deepcopy(KB)
    bombKB = addEq(bombKB, bombEq)
    simulatedBombVariables.append(variable)
    bombConfigIsValid = configIsValid(bombKB)
    if len(variables) == 1 and bombConfigIsValid:
        validConfigs += 1
        for bombVar in simulatedBombVariables:
            bombCounts[bombVar] += 1
    elif bombConfigIsValid:
        validConfigs += findValidConfigs(
            bombKB, variables[1:], simulatedBombVariables.copy(), bombCounts)

    return validConfigs


# double improved agent
def strategy3(gboard, dim, agent):
    """
    Basic Outline for Algo:
        1. Pick one of the corner cells
        2. Compute probability that a cell contains a mine, for all cells
        3. For cell in board, if P(cell = mine) = 1, mark cell as mine
        4. For cell in board, if P(cell = mine) = 0, reveal and add to knowledge base
        5. If no cell was safe, pick minimum probability in the board
    """

    KB = []
    variables = []
    inferredSafeCoords = deque()
    inferredMineCoords = deque()

    corners = [(0, 0), (0, dim - 1), (dim - 1, 0),
               (dim - 1, dim - 1)]
    cornerIndex = 0
    r, c = corners[cornerIndex]

    while not agent.isFinished():
        currentCell = agent.checkCell((r, c), gboard)
        if (currentCell.type == Cell.MINE):
            bombEq = [tupleToIndex(r, c, dim), 1]
            KB = addEq(KB, bombEq)
        else:
            safeEq = [tupleToIndex(r, c, dim), 0]
            KB = addEq(KB, safeEq)
            clueEq = []
            # find all neighbors of (r, c)
            for neighbor in currentCell.neighbors:
                nrow, ncol = neighbor
                neighborIndex = tupleToIndex(nrow, ncol, dim)
                clueEq.append(neighborIndex)
                variables.append(neighborIndex)
            clueEq.append(currentCell.type)
            KB = addEq(KB, clueEq)
        if len(variables) == 0:
            cornerIndex += 1
            if cornerIndex < len(corners):
                r, c = corners[cornerIndex]
            else:
                r = rnd.randint(0, dim - 1)
                c = rnd.randint(0, dim - 1)
                while agent.hasExplored((r, c)):
                    r = rnd.randint(0, dim - 1)
                    c = rnd.randint(0, dim - 1)
        else:
            safeCoords, mineCoords, safestCoords = calculateCellProbabilities(
                KB, variables)

    return


def calculateCellProbabilities(KB, variables):
    return set(), set(), (0, 0)
