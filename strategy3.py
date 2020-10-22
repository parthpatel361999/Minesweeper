import copy
import random as rnd

from Agent import Agent, Cell
from Board import Board
from strategy2 import addEq

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
    addEq(safeKB, safeEq)
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
    addEq(bombKB, bombEq)
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

    # pick a corner at random to start the game
    corners = [(0, 0), (0, dim - 1), (dim - 1, 0),
               (dim - 1, dim - 1)]
    coords = corners[rnd.randint(0, len(corners))]
    firstCell = agent.checkCell(coords, gboard)
    clue = firstCell.type
    corners.remove(coords)

    while clue == Cell.MINE:
        if len(corners) == 0:
            coords = (rnd.randint(0, dim), rnd.randint(0, dim))
        else:
            coords = corners[rnd.randint(0, len(corners))]
            corners.remove(coords)
        firstCell = agent.checkCell(coords, gboard)
        clue = firstCell.type

    # based on revelation from first pick, update KB accordingly
    neighbors = firstCell.neighbors
    if clue == len(firstCell.neighbors):
        for n in neighbors:
            agent.identifyMine(n)
    elif clue == 0:
        for n in neighbors:
            agent.checkCell(n)
    else:
        for n in neighbors:
            agent.board[n].probability = clue / len(firstCell.neighbors)

    # the actual game loop (until all Cells on Agent Board have been explored)

    while not agent.isFinished():
        cell, status = calculateProbability(agent)
        if status == Cell.MINE:
            agent.identifyMine(cell.coords)
        else:
            agent.checkCell(cell.coords)

    return


def calculateProbability(agent):  # bulk of strategy 3
    minProbability = 1
    minProbabilityCell = None
    # probability logic
    currCellProbability = -1  # prob will end up starting with another val
    currCell = None
    # loop for probabilty
    while True:
        # logic logic logic
        if currCellProbability == 1:
            return (currCell, Cell.MINE)
        elif currCellProbability == 0:
            return (currCell, Cell.SAFE)

        if currCellProbability < minProbability:
            minProbability = currCellProbability
            minProbabilityCell = currCell

    return (minProbabilityCell, Cell.UNCHECKED)
