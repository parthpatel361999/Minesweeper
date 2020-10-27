from common import Cell


def addEq(KB, equation):  # add an equation to the KB
    # reduce the new equation by every equation in the KB
    reduceEq(KB, equation)
    if(len(equation) < 2):  # if the equation is already contained in the KB or gets reduced to nothing, skip
        return KB
    # reduce every equation in the KB by reduced new equation
    reduceKB(KB, equation)
    KB.append(equation)  # insert the new equation into the KB


def reduceKB(KB, newEq):
    modified = []
    for i in range(len(KB)):
        # if newEq is a subset of an equation in KB
        if (KB[i] != newEq and set(newEq[0: len(newEq) - 1]).issubset(set(KB[i][0: len(KB[i]) - 1]))):
            # store the difference of the constraint values
            constraintDifference = KB[i][len(
                KB[i]) - 1] - newEq[len(newEq) - 1]
            # find the set difference
            e = list(set(KB[i][0: len(KB[i]) - 1]) -
                     set(newEq[0: len(newEq) - 1]))
            # append the constaint difference to the end of the equation
            e.append(constraintDifference)
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
    for eq in KB:  # for every equation eq in the KB, reduce the new equation by eq
        # if eq is a subset of the new equation
        if (set(eq[0: len(eq) - 1]).issubset(set(newEq[0: len(newEq) - 1]))):
            newEqLength = len(newEq)
            # store the difference of the constraint values
            constraintDifference = newEq[len(newEq) - 1] - eq[len(eq) - 1]
            # find the set difference
            newEq.extend(
                list(set(newEq[0: len(newEq) - 1]) - set(eq[0: len(eq) - 1])))
            # append the constaint difference to the end of the equation
            newEq.append(constraintDifference)
            for _ in range(newEqLength):
                newEq.remove(newEq[0])


def tupleToIndex(r, c, dim):
    return dim * r + c  # converts cell tuples to unique integers


def indexToTuple(i, dim):
    # converts the unique integers back into their respective tuples
    return (int(i / dim), i % dim)
