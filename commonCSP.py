from common import Cell

def addEq(KB, equation): #add an equation to the KB
    reduceEq(KB, equation) #reduce the new equation by every equation in the KB
    if(len(equation) < 2): #if the equation is already contained in the KB or gets reduced to nothing, skip
        return KB
    reduceKB(KB, equation) #reduce every equation in the KB by reduced new equation
    KB.append(equation) #insert the new equation into the KB

def checkForInference(KB, agent, safeSet):
    madeInference = False
    for eq in KB:
        if (len(eq) - 1 == eq[-1]): #All cells in this eq must be mines
            for var in eq[0 : len(eq) - 1]: #iterate over the variables in eq
                (r, c) = indexToTuple(var, agent.dim)
                if (agent.board[r][c].type != Cell.MINE): #if the cell is not a tripped or inferred mine
                    agent.identifyMine((r, c)) #identify the cell as an inferred mine
                    addEq(KB, [var, 1]) #add the equation [(r, c) = 1] into the KB
                    madeInference = True #flag to indicate an inference has been made
        elif (eq[-1] == 0): #All variables in this eq must be safe
            for var in eq[0 : len(eq) - 1]:
                (r, c) = indexToTuple(var, agent.dim)
                if(agent.board[r][c].revealed == True or (r, c) in safeSet):
                    continue
                addEq(KB, [var, 0])
                safeSet.add((r, c))
                madeInference = True #flag to indicate an inference has been made
    return madeInference

def reduceKB(KB, newEq):
    modified = []
    for i in range(len(KB)):
        newEqLen = len(newEq)
        KBEqLen = len(KB[i])
        if (newEqLen <= KBEqLen and KB[i] != newEq and set(newEq[0 : newEqLen - 1]).issubset(set(KB[i][0 : KBEqLen - 1]))): #if newEq is a subset of an equation in KB
            constraintDifference = KB[i][KBEqLen - 1] - newEq[newEqLen - 1] #store the difference of the constraint values
            e = list(set(KB[i][0 : KBEqLen - 1]) - set(newEq[0 : newEqLen - 1])) #find the set difference
            e.append(constraintDifference) #append the constaint difference to the end of the equation
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
    for eq in KB: #for every equation eq in the KB, reduce the new equation by eq
        eqLen = len(eq)
        newEqLen = len(newEq)
        if (eqLen <= newEqLen and set(eq[0 : eqLen - 1]).issubset(set(newEq[0 : newEqLen - 1]))): #if eq is a subset of the new equation
            #newEqLength = len(newEq)
            constraintDifference = newEq[newEqLen - 1] - eq[eqLen - 1] #store the difference of the constraint values
            newEq.extend(list(set(newEq[0 : newEqLen - 1]) - set(eq[0 : eqLen - 1]))) #find the set difference
            newEq.append(constraintDifference) #append the constaint difference to the end of the equation
            for _ in range(newEqLen):
                newEq.remove(newEq[0])


def tupleToIndex(r, c, dim):
    return dim * r + c #converts cell tuples to unique integers

def indexToTuple(i, dim):
    return (int(i / dim), i % dim) #converts the unique integers back into their respective tuples