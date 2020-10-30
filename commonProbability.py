from commonCSP import addEq, indexToTuple, tupleToIndex


def thinKB(KB, variables, agent):
    thinnedKB = []
    for eq in KB:
        if len(eq) == 2:
            r, c = indexToTuple(eq[0], agent.dim)
            neighbors = agent.board[r][c].neighbors
            infoExhausted = True
            for neighbor in neighbors:
                nr, nc = neighbor
                if tupleToIndex(nr, nc, agent.dim) in variables or not agent.hasExplored(neighbor):
                    infoExhausted = False
                    break
            if not infoExhausted:
                thinnedKB.append(eq)
        else:
            thinnedKB.append(eq)
    return thinnedKB


def addSafeEq(KB, cell, dim, agent, variables):
    """
    Add an equation identifying the cell's coordinates as safe to the knowledge base. Then, create a clue 
    equation for all of the cell's neighbors, and add those neighbors to the unknown variables list if
    they haven't been explored by the agent already.
    """
    r, c = cell.coords
    safeEq = [tupleToIndex(r, c, dim), 0]
    addEq(KB, safeEq)
    clueEq = []
    for neighbor in cell.neighbors:
        nRow, nCol = neighbor
        neighborIndex = tupleToIndex(nRow, nCol, dim)
        clueEq.append(neighborIndex)
        if not agent.hasExplored(neighbor) and neighborIndex not in variables:
            variables.append(neighborIndex)
    clueEq.append(cell.type)
    addEq(KB, clueEq)


def addMineEq(KB, cell, dim):
    """
    Add an equation identifying the cell's coordinates as a mine to the knowledge base. 
    """
    r, c = cell.coords
    mineEq = [tupleToIndex(r, c, dim), 1]
    addEq(KB, mineEq)


def createVariableGraph(KB, variables):
    variableGraph = []
    relevantKBs = []
    while len(variables) > 0:
        node = variables[0]
        visited = set()
        queue = [node]
        connectedComponent = []
        relevantKB = []
        while len(queue) > 0:
            checkNode = queue.pop(0)
            visited.add(checkNode)
            connectedComponent.append(checkNode)
            variables.remove(checkNode)
            neighbors = []
            for eq in KB:
                if eq not in relevantKB and checkNode in eq[0:len(eq) - 1]:
                    for var in eq[0:len(eq) - 1]:
                        if var != checkNode:
                            neighbors.append(var)
                    relevantKB.append(eq)
            for neighbor in neighbors:
                if neighbor not in visited and neighbor in variables:
                    queue.append(neighbor)
                    visited.add(neighbor)
        variableGraph.append(connectedComponent)
        relevantKBs.append(relevantKB)
    return variableGraph, relevantKBs


def copyKB(KB):
    newKB = []
    for eq in KB:
        newKB.append(eq.copy())
    return newKB


def findValidConfigs(KB, variables, simulatedMineVariables, mineCounts):
    if len(variables) < 1:
        return 0

    validConfigs = 0

    madeInference = checkForInferencesTrackingMines(
        KB, variables, simulatedMineVariables)
    while madeInference:
        madeInference = checkForInferencesTrackingMines(
            KB, variables, simulatedMineVariables)

    if len(variables) == 0:
        validConfigs += 1
        for mineVar in simulatedMineVariables:
            mineCounts[mineVar] += 1
    else:
        variable = variables[0]
        safeEq = [variable, 0]
        safeKB = copyKB(KB)
        addEq(safeKB, safeEq)
        safeConfigIsValid = configIsValid(safeKB)
        if len(variables) == 1 and safeConfigIsValid:
            validConfigs += 1
            for mineVar in simulatedMineVariables:
                mineCounts[mineVar] += 1
        elif safeConfigIsValid:
            validConfigs += findValidConfigs(
                safeKB, variables[1:], simulatedMineVariables.copy(), mineCounts)
        mineEq = [variable, 1]
        mineKB = copyKB(KB)
        addEq(mineKB, mineEq)
        simulatedMineVariables.add(variable)
        mineConfigIsValid = configIsValid(mineKB)
        if len(variables) == 1 and mineConfigIsValid:
            validConfigs += 1
            for mineVar in simulatedMineVariables:
                mineCounts[mineVar] += 1
        elif mineConfigIsValid:
            validConfigs += findValidConfigs(
                mineKB, variables[1:], simulatedMineVariables.copy(), mineCounts)

    return validConfigs


def checkForInferencesTrackingMines(KB, variables, mineVariables):
    madeInference = False
    eqsToAdd = []
    for eq in KB:
        if len(eq) - 1 == eq[-1]:
            for var in eq[0:len(eq) - 1]:
                if var in variables:
                    variables.remove(var)
                    mineVariables.add(var)
                    mineEq = [var, 1]
                    eqsToAdd.append(mineEq)
                    madeInference = True
        elif eq[-1] == 0:
            for var in eq[0:len(eq) - 1]:
                if var in variables:
                    variables.remove(var)
                    safeEq = [var, 0]
                    eqsToAdd.append(safeEq)
                    madeInference = True
    for eq in eqsToAdd:
        addEq(KB,  eq)
    return madeInference


def configIsValid(KB):
    for eq in KB:
        if len(eq) - 1 < eq[-1] or eq[-1] < 0:
            return False
    return True