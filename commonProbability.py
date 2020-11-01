from commonCSP import addEq, indexToTuple, tupleToIndex


def thinKB(KB, variables, agent):
    """
    If an equation is of length 2, then it is an assignment for a variable. If
    all of the neighbors of the cell corresponding to the variable have been
    explored, then this equation is no longer needed as all information it can
    provide has been exhausted. Therefore, it can be removed from the knowledge
    base.  
    """
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
    """
    Run a basic BFS on the variables and generate all connected components. The only special aspect of
    this BFS is the neighbor calculation.
    """
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
            """
            Calculate the neighbors for this variable. If this variable exists in an equation that
            does not already exist in the relevant knowledge base, add all other variables of that
            equation to the neighbors list.
            """
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
    """
    Create a copy of the knowledge base.
    """
    newKB = []
    for eq in KB:
        newKB.append(eq.copy())
    return newKB


def findValidConfigs(KB, variables, simulatedMineVariables, mineCounts):
    if len(variables) < 1:
        return 0

    validConfigs = 0

    """
    Prune the search tree. Check if any inferences can be made in the knowledge base about
    any of the variables still to be explored based on variable assignments that have been
    made so far. If yes, add those inferences to this knowledge base so that fewer
    combinations of the variables' values need to be considered, decreasing the number of
    branches to be explored. 
    """

    madeInference = checkForInferencesTrackingMines(
        KB, variables, simulatedMineVariables)
    while madeInference:
        madeInference = checkForInferencesTrackingMines(
            KB, variables, simulatedMineVariables)

    """
    If a leaf node has been reached, check which variables were simulated to be mines and
    increment their mine counts in the given dictionary.
    """
    if len(variables) == 0:
        validConfigs += 1
        for mineVar in simulatedMineVariables:
            mineCounts[mineVar] += 1
    else:
        """
        Pick the first variable from the variables list. Simulate this variable being a safe
        cell first by adding a "safe equation" for this variable to a copy of the knowledge
        base. If the new configuration is valid and a leaf node has been reached, conduct the
        "leaf node" process as described in the previous comment. Else, recurse with this copied
        knowledge base and the variables list without this variable.

        If this simulated configuration is not valid, we do not explore the branch further, thus
        pruning this branch.
        """
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
        """
        Using the same variable, simulate this variable being a mine by adding a "mine equation"
        for this variable to a copy of the knowledge base. Add this variable to the simulated mine
        list. If the new configuration is valid and a leaf node has been reached, conduct the
        "leaf node" process as described in the second-to-last comment. Else, recurse with this
        copied knowledge base and the variables list without this variable.

        If this simulated configuration is not valid, we do not explore the branch further, thus
        pruning this branch.
        """
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

    """
    Return the number of valid configurations.
    """
    return validConfigs


def checkForInferencesTrackingMines(KB, variables, mineVariables):
    madeInference = False
    eqsToAdd = []
    for eq in KB:
        """
        If a variable is mine the same number of times as the number of valid configurations,
        it must be a mine.
        """
        if len(eq) - 1 == eq[-1]:
            for var in eq[0:len(eq) - 1]:
                if var in variables:
                    variables.remove(var)
                    mineVariables.add(var)
                    mineEq = [var, 1]
                    eqsToAdd.append(mineEq)
                    madeInference = True
        elif eq[-1] == 0:
            """
            Generate the probability of this variable being a mine. If the probability is less
            than 1/8, infer the variable to be safe. Otherwise, append it to a list to be sorted
            by mine probability later.
            """
            for var in eq[0:len(eq) - 1]:
                if var in variables:
                    variables.remove(var)
                    safeEq = [var, 0]
                    eqsToAdd.append(safeEq)
                    madeInference = True
    """
    Add all new equations to the knowledge base.
    """
    for eq in eqsToAdd:
        addEq(KB,  eq)
    return madeInference


def configIsValid(KB):
    """
    The knowledge base is not valid if:
        a. The clue of the equation exceeds the number of variables in the equation.
        b. The clue of the equation is less than 0.
    """
    for eq in KB:
        if len(eq) - 1 < eq[-1] or eq[-1] < 0:
            return False
    return True
