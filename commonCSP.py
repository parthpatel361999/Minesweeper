def addEq(KB, equation):  # add an equation to the KB
    # reduce the new equation by every equation in the KB
    equation = reduceEq(KB, equation)
    if(len(equation) == 1):  # if the equation is already contained in the KB, skip
        return KB
    # reduce every equation in the KB by reduced new equation
    KB = reduceKB(KB, equation)
    KB.append(equation)  # insert the new equation into the KB
    return KB


def reduceKB(KB, newEq):
    KB2 = []
    for eq in KB:
        if (eq == newEq):  # if the equation is already in the KB, skip
            continue
        # if newEq is a subset of an equation in KB
        elif (set(newEq[0: len(newEq) - 1]).issubset(set(eq[0: len(eq) - 1]))):
            # store the difference of the constraint values
            constraintDifference = eq[len(eq) - 1] - newEq[len(newEq) - 1]
            # find the set difference
            e = list(set(eq[0: len(eq) - 1]) - set(newEq[0: len(newEq) - 1]))
            # append the constaint difference to the end of the equation
            e.append(constraintDifference)
            KB2.append(e)
        else:
            KB2.append(eq)
    return KB2


def reduceEq(KB, newEq):
    for eq in KB:  # for every equation eq in the KB, reduce the new equation by eq
        # if eq is a subset of the new equation
        if (set(eq[0: len(eq) - 1]).issubset(set(newEq[0: len(newEq) - 1]))):
            # store the difference of the constraint values
            constraintDifference = newEq[len(newEq) - 1] - eq[len(eq) - 1]
            # find the set difference
            newEq = list(set(newEq[0: len(newEq) - 1]) -
                         set(eq[0: len(eq) - 1]))
            # append the constaint difference to the end of the equation
            newEq.append(constraintDifference)
    return newEq


def tupleToIndex(r, c, dim):
    return dim * r + c  # converts cell tuples to unique integers


def indexToTuple(i, dim):
    # converts the unique integers back into their respective tuples
    return (int(i / dim), i % dim)
