import random as rnd
import time

from common import Agent, Board, Cell, findNeighboringCoords
from commonCSP import indexToTuple, tupleToIndex
from commonProbability import (addMineEq, addSafeEq, createVariableGraph,
                               findValidConfigs, thinKB)


# double improved agent
def strategy4(gboard, dim, agent):
    """
    Declare a list for the knowledge base, which will be filled with equations (represented as lists 
    themselves). Also declare a set for the unknown variables in the knowledge base.
    """
    KB = []
    variables = []

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
            addMineEq(KB, currentCell, dim)
        else:
            addSafeEq(KB, currentCell, dim, agent, variables)

        safeVarsToAdd, mineVarsToAdd = checkForInferences(KB, variables)
        while len(safeVarsToAdd) > 0 or len(mineVarsToAdd) > 0:
            addInferredSafeAndMineVariables(
                safeVarsToAdd, mineVarsToAdd, gboard, KB, agent, variables)
            safeVarsToAdd, mineVarsToAdd = checkForInferences(KB, variables)

        KB = thinKB(KB, set(variables), agent)
        # print("variables:", str(len(variables)))

        """
        If there are no unknown variables in the knowledge base, choose one of the preferred coordinates.
        If all preferred coordinates have been explored, choose random coordinates.

        There is no point in calculating probabilities if there are no variables for which to calculate
        probabilities, so choose the preferred coordinates instead.
        """
        if agent.isFinished() and len(variables) == 0:
            break
        elif len(variables) == 0:
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
            safeVariables, mineVariables = calculateVariableProbabilities(
                KB, variables, dim)
            while len(safeVariables) > 0 or len(mineVariables) > 0:

                for variable in mineVariables:
                    if variable in variables:
                        variables.remove(variable)
                    coords = indexToTuple(variable, agent.dim)
                    mineCell = agent.identifyMine(coords)
                    addMineEq(KB, mineCell, agent.dim)

                for variable in safeVariables:
                    if variable in variables:
                        variables.remove(variable)
                    coords = indexToTuple(variable, agent.dim)
                    cell = agent.checkCell(coords, gboard)
                    if cell.type == Cell.MINE:
                        addMineEq(KB, cell, dim)
                    else:
                        addSafeEq(KB, cell, dim, agent, variables)

                safeVarsToAdd, mineVarsToAdd = checkForInferences(
                    KB, variables)

                while len(safeVarsToAdd) > 0 or len(mineVarsToAdd) > 0:
                    addInferredSafeAndMineVariables(
                        safeVarsToAdd, mineVarsToAdd, gboard, KB, agent, variables)
                    safeVarsToAdd, mineVarsToAdd = checkForInferences(
                        KB, variables)

                KB = thinKB(KB, set(variables), agent)
                if len(variables) > 0:
                    safeVariables, mineVariables = calculateVariableProbabilities(
                        KB, variables, dim)
                # print("inner variables:", str(len(variables)))

            if len(variables) > 0:
                r, c = indexToTuple(variables[0], dim)
                variables.remove(variables[0])
            elif not agent.isFinished():
                r, c = agent.choosePreferredOrRandomCoords()


def checkForInferences(KB, variables):
    mineVarsToAdd = set()
    safeVarsToAdd = set()
    for eq in KB:
        if len(eq) - 1 == eq[-1]:
            for var in eq[0:len(eq) - 1]:
                if var in variables:
                    variables.remove(var)
                    mineVarsToAdd.add(var)

        elif eq[-1] == 0:
            for var in eq[0:len(eq) - 1]:
                if var in variables:
                    variables.remove(var)
                    safeVarsToAdd.add(var)

    return safeVarsToAdd, mineVarsToAdd


def addInferredSafeAndMineVariables(safeVarsToAdd, mineVarsToAdd, gboard, KB, agent, variables):
    for variable in safeVarsToAdd:
        if variable in variables:
            variables.remove(variable)
        coords = indexToTuple(variable, agent.dim)
        safeCell = agent.checkCell(coords, gboard)
        addSafeEq(KB, safeCell, agent.dim, agent, variables)
    for variable in mineVarsToAdd:
        if variable in variables:
            variables.remove(variable)
        coords = indexToTuple(variable, agent.dim)
        mineCell = agent.identifyMine(coords)
        addMineEq(KB, mineCell, agent.dim)


def calculateVariableProbabilities(KB, variables, dim):
    # print("KB size:", str(len(KB)))
    mineCounts = {}
    for variable in variables:
        mineCounts[variable] = 0
    variableGraph, relevantKBs = createVariableGraph(
        KB, variables.copy())
    # print("components:", len(variableGraph))
    maxSize = 0
    for component in variableGraph:
        if len(component) > maxSize:
            maxSize = len(component)
    # print("component max size:", maxSize)
    safeVariables = []
    mineVariables = []
    variableProbabilities = []
    for i in range(0, len(variableGraph)):
        relevantKB = relevantKBs[i]
        connectedVariables = variableGraph[i]
        validConfigurations = findValidConfigs(
            relevantKB, connectedVariables.copy(), set(), mineCounts)
        for variable in connectedVariables:
            if mineCounts[variable] == validConfigurations:
                mineVariables.append(variable)
            else:
                mineProb = float(mineCounts[variable]) / \
                    float(validConfigurations)
                if mineProb < 1.0/8.0:
                    safeVariables.append(variable)
                else:
                    variableProbabilities.append((mineProb, variable))
    variables.clear()
    variableProbabilities.sort()
    for probVar in variableProbabilities:
        probability, variable = probVar
        variables.append(variable)
    return safeVariables, mineVariables


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
    print("total explored:", str(numTripped + numIdentifiedMines + numRevealed))
    for coords in agent.identifiedMineCoords:
        r, c = coords
        if gb.board[r][c] != Cell.MINE:
            print(r, c, "reported as mine incorrectly")


i = 0

dim = 50

while i < 20:

    gb = Board(dim)
    gb.set_mines(int(dim**2 * 0.4))

    print("Strat 3")
    print(gb.board)
    corners = [(0, 0), (0, dim - 1), (dim - 1, 0), (dim - 1, dim - 1)]
    ag = Agent(dim=dim, preferredCoords=corners)
    startTime = time.time()
    strategy4(gb, dim, ag)

    print("Display")
    print(gb.board)
    display(dim, ag)
    endTime = time.time()
    print("Time:", endTime - startTime,
          "seconds (" + str((endTime - startTime)/60), "min)")

    i += 1