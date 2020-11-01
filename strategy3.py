import random as rnd
import time

from common import Agent, Board, Cell, display, findNeighboringCoords
from commonCSP import addEq, indexToTuple, tupleToIndex
from commonProbability import (addMineEq, addSafeEq, configIsValid, copyKB,
                               createVariableGraph, findValidConfigs, thinKB)


def strategy3(gboard, dim, agent):
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

        currentCell = agent.checkCell((r, c), gboard)
        if currentCell.type == Cell.MINE:
            addMineEq(KB, currentCell, dim)
        else:
            addSafeEq(KB, currentCell, dim, agent, variables)

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
            equations and variables. 

            After adding all the equations and checking/identifying the coordinates corresponding to each 
            inferred variable, recalculate the probabilities for all remaining variables. Repeat until there
            are no inferences to be drawn.

            Then, if there is a cell that is least likely to be a mine, set its
            coordinates as the next to be explored; else, choose from the preferred coordinates (or
            random coordinates, if necessary).
            """
            KB = thinKB(KB, set(variables), agent)
            safeVariables, mineVariables = calculateVariableProbabilities(
                KB, variables, dim)
            while len(safeVariables) > 0 or len(mineVariables) > 0:
                for variable in safeVariables:
                    if variable in variables:
                        variables.remove(variable)
                    coords = indexToTuple(variable, dim)
                    safeCell = agent.checkCell(coords, gboard)
                    addSafeEq(KB, safeCell, dim, agent, variables)
                for variable in mineVariables:
                    if variable in variables:
                        variables.remove(variable)
                    coords = indexToTuple(variable, dim)
                    mineCell = agent.identifyMine(coords)
                    addMineEq(KB, mineCell, dim)
                KB = thinKB(KB, set(variables), agent)
                safeVariables, mineVariables = calculateVariableProbabilities(
                    KB, variables, dim)
                # print("inner variables:", str(len(variables)))

            if len(variables) > 0:
                r, c = indexToTuple(variables[0], dim)
                variables.remove(variables[0])
            elif not agent.isFinished():
                r, c = agent.choosePreferredOrRandomCoords()


def calculateVariableProbabilities(KB, variables, dim):
    """
    Initialize a dictionary to track in how many valid configurations a cell is represented
    as a mine.
    """
    mineCounts = {}
    for variable in variables:
        mineCounts[variable] = 0

    """  
    Create a list for the connected components of the variables and another list for each
    of their relevant KBs.
    """
    variableGraph, relevantKBs = createVariableGraph(
        KB, variables.copy())

    """
    For each connected component, generate the valid configurations of the board and increment
    a specific variable's mine count value whenever it shows up in a valid configuration
    as a mine.
    """
    safeVariables = []
    mineVariables = []
    variableProbabilities = []
    for i in range(0, len(variableGraph)):
        relevantKB = relevantKBs[i]
        connectedVariables = variableGraph[i]
        validConfigurations = findValidConfigs(
            relevantKB, connectedVariables.copy(), set(), mineCounts)
        for variable in connectedVariables:
            """
            If a variable is mine the same number of times as the number of valid configurations,
            it must be a mine.
            """
            if mineCounts[variable] == validConfigurations:
                mineVariables.append(variable)
            elif mineCounts[variable] == 0:
                """
                If a variable is never a mine in any of the valid configurations, it must be safe.                
                """
                safeVariables.append(variable)
            else:
                """
                Calculate the probability for this variable, and append it to a list to be sorted
                by mine probability later.
                """
                mineProb = float(mineCounts[variable]) / \
                    float(validConfigurations)
                variableProbabilities.append((mineProb, variable))
    variables.clear()
    variableProbabilities.sort()
    for probVar in variableProbabilities:
        probability, variable = probVar
        variables.append(variable)
    return safeVariables, mineVariables
