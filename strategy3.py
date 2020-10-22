import copy
import random as rnd
from collections import deque

from Agent import Agent, Cell
from Board import Board
from strategy2 import addEq, indexToTuple, tupleToIndex


# double improved agent
def strategy3(gboard, dim, agent):
    """
    Declare a list for the knowledge base, which will be filled with equations (represented as lists 
    themselves). Also declare a set for the unknown variables in the knowledge base.
    """
    KB = []
    variables = set()

    """
    Create a list of the preferred coordinates for the agent to choose from when no better option is
    available. In thise case, the preferred coordinates are the corners of the minefield. For the
    first choice of where the agent should explore, choose the first (top-left) corner.
    """
    corners = [(0, 0), (0, dim - 1), (dim - 1, 0),
               (dim - 1, dim - 1)]
    cornerIndex = 0
    r, c = corners[cornerIndex]

    while not agent.isFinished():
        """
        Check the current cell. Based on the type of the mine, add the respective equations and variables.
        """
        currentCell = agent.checkCell((r, c), gboard)
        if (currentCell.type == Cell.MINE):
            KB = addMineEq(KB, currentCell, dim)
        else:
            KB = addSafeEq(KB, currentCell, dim, agent, variables)

        """
        If there are no unknown variables in the knowledge base, choose one of the preferred coordinates.
        If all preferred coordinates have been explored, choose random coordinates.

        There is no point in calculating probabilities if there are no variables for which to calculate
        probabilities, so choose the preferred coordinates instead.
        """
        if len(variables) == 0:
            cornerIndex += 1
            if cornerIndex < len(corners):
                r, c = corners[cornerIndex]
            else:
                r, c = agent.chooseRandomCoords()

        else:
            """
            Calculate the probabilities for all variables, and find the variables that are guaranteed to
            be safe and those that are guaranteed to be mines. For such variables, remove them from the
            unknown variables set and check or identify the corresponding coordinates. Add the respective
            equations and variables. Then, if there is a cell that is least likely to be a mine, set its
            coordinates as the next to be explored; else, choose from the preferred coordinates (or
            random coordinates, if necessary).
            """
            safeVariables, mineVariables, safestVariable = calculateVariableProbabilities(
                KB, list(variables))
            for variable in safeVariables:
                variables.remove(variable)
                safeCell = agent.checkCell(indexToTuple(variable, dim), gboard)
                KB = addSafeEq(KB, safeCell, dim, variables)
            for variable in mineVariables:
                variables.remove(variable)
                mineCell = agent.identifyMine(indexToTuple(variable, dim))
                KB = addMineEq(KB, mineCell, dim)
            if not safestVariable is None:
                r, c = indexToTuple(safestVariable, dim)
            else:
                cornerIndex += 1
                if cornerIndex < len(corners):
                    r, c = corners[cornerIndex]
                else:
                    r, c = agent.chooseRandomCoords()


def addSafeEq(KB, cell, dim, agent, variables=set()):
    """
    Add an equation identifying the cell's coordinates as safe to the knowledge base. Then, create a clue 
    equation for all of the cell's neighbors, and add those neighbors to the unknown variables list if
    they haven't been explored by the agent already.
    """
    r, c = cell.coords
    safeEq = [tupleToIndex(r, c, dim), 0]
    KB = addEq(KB, safeEq)
    clueEq = []
    for neighbor in cell.neighbors:
        nRow, nCol = neighbor
        neighborIndex = tupleToIndex(nRow, nCol, dim)
        clueEq.append(neighborIndex)
        if not agent.hasExplored((nRow, nCol)):
            variables.add(neighborIndex)
    clueEq.append(cell.type)
    KB = addEq(KB, clueEq)
    return KB


def addMineEq(KB, cell, dim):
    """
    Add an equation identifying the cell's coordinates as a mine to the knowledge base. 
    """
    r, c = cell.coords
    mineEq = [tupleToIndex(r, c, dim), 1]
    KB = addEq(KB, mineEq)
    return KB


def calculateVariableProbabilities(KB, variables):
    mineCounts = {}
    for variable in variables:
        mineCounts[variable] = 0
    validConfigurations = findValidConfigs(KB, variables, [], mineCounts)
    safeVariables = []
    mineVariables = []
    minMineProb = 1
    safestVariable = None
    for variable in mineCounts:
        if mineCounts[variable] == 0:
            safeVariables.append(variable)
        elif mineCounts[variable] == validConfigurations:
            mineVariables.append(variable)
        else:
            mineProb = mineCounts[variable] / validConfigurations
            if mineProb < minMineProb:
                minMineProb = mineProb
                safestVariable = variable
    return safeVariables, mineVariables, safestVariable


def findValidConfigs(KB, variables, simulatedMineVariables, mineCounts):
    validConfigs = 0
    variable = variables[0]

    safeEq = [variable, 0]
    safeKB = copy.deepcopy(KB)
    safeKB = addEq(safeKB, safeEq)
    safeConfigIsValid = configIsValid(safeKB)
    if len(variables) == 1 and safeConfigIsValid:
        validConfigs += 1
        for mineVar in simulatedMineVariables:
            mineCounts[mineVar] += 1
    elif safeConfigIsValid:
        validConfigs += findValidConfigs(
            safeKB, variables[1:], simulatedMineVariables.copy(), mineCounts)

    mineEq = [variable, 1]
    mineKB = copy.deepcopy(KB)
    mineKB = addEq(mineKB, mineEq)
    simulatedMineVariables.append(variable)
    mineConfigIsValid = configIsValid(mineKB)
    if len(variables) == 1 and mineConfigIsValid:
        validConfigs += 1
        for mineVar in simulatedMineVariables:
            mineCounts[mineVar] += 1
    elif mineConfigIsValid:
        validConfigs += findValidConfigs(
            mineKB, variables[1:], simulatedMineVariables.copy(), mineCounts)

    return validConfigs


def configIsValid(KB):
    for eq in KB:
        if len(eq) - 1 > eq[-1] or eq[-1] < 0:
            return False
    return True
