import copy
import itertools
import random as rnd
from collections import deque

from common import Agent, Board, Cell
from commonCSP import addEq, indexToTuple, tupleToIndex


# double improved agent
def strategy3(gboard, dim, agent):
    """
    Declare a list for the knowledge base, which will be filled with equations (represented as lists 
    themselves). Also declare a set for the unknown variables in the knowledge base.
    """
    KB = []
    variables = set()

    """
    If there are preferred coordinates for the agent to choose from, choose the first of those. Else,
    choose a random pair of coordinates for the first move.
    """
    r, c = agent.choosePreferredOrRandomCoords()

    while not agent.isFinished():
        """
        Check the current cell. Based on the type of the mine, add the respective equations and variables.
        """

        # print(r, c, "or", tupleToIndex(r, c, dim))
        currentCell = agent.checkCell((r, c), gboard)
        if currentCell.type == Cell.MINE:
            KB = addMineEq(KB, currentCell, dim)
        else:
            KB = addSafeEq(KB, currentCell, dim, agent, variables)
        print("variables:", str(len(variables)))

        """
        If there are no unknown variables in the knowledge base, choose one of the preferred coordinates.
        If all preferred coordinates have been explored, choose random coordinates.

        There is no point in calculating probabilities if there are no variables for which to calculate
        probabilities, so choose the preferred coordinates instead.
        """
        if agent.isFinished() and len(variables) == 0:
            break
        elif len(variables) == 0:
            # print("random choice")
            r, c = agent.choosePreferredOrRandomCoords()
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
            while len(safeVariables) > 0 or len(mineVariables) > 0:
                for variable in safeVariables:
                    variables.remove(variable)
                    coords = indexToTuple(variable, dim)
                    safeCell = agent.checkCell(coords, gboard)
                    KB = addSafeEq(KB, safeCell, dim, agent, variables)
                for variable in mineVariables:
                    variables.remove(variable)
                    coords = indexToTuple(variable, dim)
                    mineCell = agent.identifyMine(coords)
                    KB = addMineEq(KB, mineCell, dim)
                safeVariables, mineVariables, safestVariable = calculateVariableProbabilities(
                    KB, list(variables))

            if safestVariable is not None:
                r, c = indexToTuple(safestVariable, dim)
                variables.remove(safestVariable)
            elif not agent.isFinished():
                r, c = agent.choosePreferredOrRandomCoords()


def addSafeEq(KB, cell, dim, agent, variables=None):
    """
    Add an equation identifying the cell's coordinates as safe to the knowledge base. Then, create a clue 
    equation for all of the cell's neighbors, and add those neighbors to the unknown variables list if
    they haven't been explored by the agent already.
    """
    if variables is None:
        variables = set()
    r, c = cell.coords
    safeEq = [tupleToIndex(r, c, dim), 0]
    KB = addEq(KB, safeEq)
    clueEq = []
    for neighbor in cell.neighbors:
        nRow, nCol = neighbor
        neighborIndex = tupleToIndex(nRow, nCol, dim)
        clueEq.append(neighborIndex)
        if not agent.hasExplored(neighbor):
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
    validConfigurations = findValidConfigs(KB, variables, [],  mineCounts)
    safeVariables = []
    mineVariables = []
    minMineProb = 1.0
    safestVariable = None
    for variable in mineCounts:
        if mineCounts[variable] == 0:
            safeVariables.append(variable)
        elif mineCounts[variable] == validConfigurations:
            mineVariables.append(variable)
        else:
            mineProb = mineCounts[variable] / validConfigurations
            if mineProb < minMineProb:
                safestVariable = variable
                minMineProb = mineProb
    return safeVariables, mineVariables, safestVariable


def findValidConfigs(KB, variables, simulatedMineVariables, mineCounts):
    validConfigs = 0

    if len(variables) < 1:
        return validConfigs

    variable = variables[0]
    existingAssignment = findExistingAssignment(KB, variable)

    if existingAssignment is not None:
        if existingAssignment == 0:
            if len(variables) == 1:
                validConfigs += 1
                for mineVar in simulatedMineVariables:
                    mineCounts[mineVar] += 1
            else:
                validConfigs += findValidConfigs(
                    KB, variables[1:], simulatedMineVariables.copy(), mineCounts)
        elif existingAssignment == 1:
            simulatedMineVariables.append(variable)
            if len(variables) == 1:
                validConfigs += 1
                for mineVar in simulatedMineVariables:
                    mineCounts[mineVar] += 1
            else:
                validConfigs += findValidConfigs(
                    KB, variables[1:], simulatedMineVariables.copy(), mineCounts)
    else:
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


def findExistingAssignment(KB, variable):
    for eq in KB:
        if len(eq) == 2 and eq[0] == variable:
            return eq[1]
    return None


def configIsValid(KB):
    for eq in KB:
        if len(eq) - 1 < eq[-1] or eq[-1] < 0:
            return False
    return True


def display(dim, agent):
    numTripped = 0
    numIdentifiedMines = 0
    numRevealed = 0
    display = Board(dim)
    for i in range(0, dim):
        for j in range(0, dim):
            if((i, j) in agent.trippedMineCoords):
                display.board[i][j] = '2'
                numTripped += 1
            elif((i, j) in agent.identifiedMineCoords):
                display.board[i][j] = '1'
                numIdentifiedMines += 1
            elif((i, j) in agent.revealedCoords):
                display.board[i][j] = '9'
                numRevealed += 1
            else:
                continue
    print(display.board)
    print("Tripped Mines: " + str(numTripped))
    print("Identified Mines: " + str(numIdentifiedMines))
    print("Revealed Cells: " + str(numRevealed))
    print("Identified Mines/Total Mines: " +
          str(numIdentifiedMines / int(agent.dim**2 * 0.4)))
    print("total mines:", str(numTripped + numIdentifiedMines + numRevealed))


dim = 10

gb = Board(dim)
gb.set_mines(int(dim**2 * 0.4))

print("Strat 3")
print(gb.board)
corners = [(0, 0), (0, dim - 1), (dim - 1, 0), (dim - 1, dim - 1)]
ag = Agent(dim=dim, preferredCoords=corners)
strategy3(gb, dim, ag)

print("Display")
print(ag.revealedCoords)
print(ag.identifiedMineCoords)
print(gb.board)
display(dim, ag)
