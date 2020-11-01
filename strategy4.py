import random as rnd
import time

from common import Agent, Board, Cell, display, findNeighboringCoords
from commonCSP import indexToTuple, tupleToIndex
from commonProbability import (addMineEq, addSafeEq, createVariableGraph,
                               findValidConfigs, thinKB)


# Triple improved
def strategy4(gboard, dim, agent):
    """
    Declare a list for the knowledge base, which will be filled with equations (represented as lists 
    themselves). Also declare a list for the unknown variables in the knowledge base.
    """
    KB = []
    variables = []

    """
    Initialize the first row and column to be chosen with the agent's preferred coordinates or random
    coordinates if there are no preferred coordinates.
    """
    r, c = agent.choosePreferredOrRandomCoords()

    while not agent.isFinished():
        """
        Check the current cell. Based on the type of the cell, add the respective equations and variables.
        """
        currentCell = agent.checkCell((r, c), gboard)
        if currentCell.type == Cell.MINE:
            addMineEq(KB, currentCell, dim)
        else:
            addSafeEq(KB, currentCell, dim, agent, variables)

        """
        Check the knowledge base for any possible inferences to make. Check and identify all cells inferred
        to be safe and mines. While an inference has been made, check for inferences until an inference has
        not been made.
        """
        safeVarsToAdd, mineVarsToAdd = checkForInferences(KB, variables)
        while len(safeVarsToAdd) > 0 or len(mineVarsToAdd) > 0:
            addInferredSafeAndMineVariables(
                safeVarsToAdd, mineVarsToAdd, gboard, KB, agent, variables)
            safeVarsToAdd, mineVarsToAdd = checkForInferences(KB, variables)

        KB = thinKB(KB, set(variables), agent)
        # print("variables:", str(len(variables)))

        """
        If the agent has finished exploring the entire minefield, finish the algorithm.

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

            Then, check for any inferences that can be made using the updated knowledge base, and do this
            repeatedly while an inference has been made. Then, calculate probabilities for all variables
            again.

            Once there are no additional cells guaranteed to be mines or safe from the probability
            calculations, pick the next row and column. If there is a cell that is least likely to be a
            mine, set its coordinates as the next to be explored; else, choose from the preferred
            coordinates (or random coordinates, if necessary).
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
        """
        If the number of variables in an equation matches the clue, all variables in
        that equation are mines
        """

        if len(eq) - 1 == eq[-1]:
            for var in eq[0:len(eq) - 1]:
                if var in variables:
                    variables.remove(var)
                    mineVarsToAdd.add(var)

        elif eq[-1] == 0:
            """
            If the clue in an equation is 0, all variables in that equation are safe.
            """
            for var in eq[0:len(eq) - 1]:
                if var in variables:
                    variables.remove(var)
                    safeVarsToAdd.add(var)

    return safeVarsToAdd, mineVarsToAdd


def addInferredSafeAndMineVariables(safeVarsToAdd, mineVarsToAdd, gboard, KB, agent, variables):
    """
    Add safe equations (variable = 0) for all safe variables and mine equations
    (variable = 1) for all mine variables to the knowledge base. Remove the corresponding
    variables from the given variables list.
    """
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
            else:
                """
                Generate the probability of this variable being a mine. If the probability is less
                than 1/8, infer the variable to be safe. Otherwise, append it to a list to be sorted
                by mine probability later.
                """
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
