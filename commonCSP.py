from common import Cell


def checkForInference(KB, agent, safeSet):
    madeInference = False
    for eq in KB:
        if (len(eq) - 1 == eq[-1]):  # All cells in this eq must be mines
            for var in eq[0: len(eq) - 1]:  # iterate over the variables in eq
                (r, c) = indexToTuple(var, agent.dim)
                # if the cell is not a tripped or inferred mine
                if (agent.board[r][c].type != Cell.MINE):
                    # identify the cell as an inferred mine
                    agent.identifyMine((r, c))
                    # add the equation [(r, c) = 1] into the KB
                    KB = addEq(KB, [var, 1])
                    madeInference = True  # flag to indicate an inference has been made
        elif (eq[-1] == 0):  # All variables in this eq must be safe
            for var in eq[0: len(eq) - 1]:
                (r, c) = indexToTuple(var, agent.dim)
                if(agent.board[r][c].revealed == True or (r, c) in safeSet):
                    continue
                KB = addEq(KB, [var, 0])
                safeSet.add((r, c))
                madeInference = True  # flag to indicate an inference has been made
    return(KB, madeInference)


def addEq(KB, equation):  # add an equation to the KB
    # reduce the new equation by every equation in the KB
    equation = reduceEq(KB, equation)
    if(equation == []):  # if the equation is already contained in the KB or gets reduced to nothing, skip
        return KB
    # reduce every equation in the KB by reduced new equation
    KB = reduceKB(KB, equation)
    KB.append(equation)  # insert the new equation into the KB
    return KB


def reduceKB(KB, newEq):
    newKB = []
    for eq in KB:
        # this check is covered by reduceEq
        # tempEq = eq[0:len(eq) - 1]
        # tempEq.sort()
        # tempNewEq = newEq[0:len(newEq) - 1]
        # tempNewEq.sort()
        # if (tempEq == tempNewEq and eq[len(eq) - 1] == newEq[len(newEq) - 1]): #if the equation is already in the KB, skip
        #     continue
        # if newEq is a subset of an equation in KB
        if (set(newEq[0: len(newEq) - 1]).issubset(set(eq[0: len(eq) - 1]))):
            # store the difference of the constraint values
            constraintDifference = eq[len(eq) - 1] - newEq[len(newEq) - 1]
            # find the set difference
            e = list(set(eq[0: len(eq) - 1]) - set(newEq[0: len(newEq) - 1]))
            # append the constaint difference to the end of the equation
            e.append(constraintDifference)
            if(e not in newKB):
                newKB.append(e)
        elif(eq not in newKB):
            newKB.append(eq)
    return newKB


def reduceEq(KB, newEq):
    for eq in KB:  # for every equation eq in the KB, reduce the new equation by eq
        # if eq is a subset of the new equation
        print("New", newEq)
        print("eq", eq)

        if (set(eq[0: len(eq) - 1]).issubset(set(newEq[0: len(newEq) - 1]))):
            # store the difference of the constraint values
            constraintDifference = newEq[len(newEq) - 1] - eq[len(eq) - 1]
            # find the set difference
            newEq = list(set(newEq[0: len(newEq) - 1]) -
                         set(eq[0: len(eq) - 1]))
            # append the constaint difference to the end of the equation
            newEq.append(constraintDifference)
    if (len(newEq) < 2):
        return []
    else:
        return newEq


def tupleToIndex(r, c, dim):
    return dim * r + c  # converts cell tuples to unique integers


def indexToTuple(i, dim):
    # converts the unique integers back into their respective tuples
    return (int(i / dim), i % dim)
