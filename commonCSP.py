import sys

from common import Cell

'''
addEq adds an equation to the Knowledge Base. It first reduces the equation by the Knowledge Base.
Then it reduces the Knowledge Base by the equation. 
Then it appends. 

'''
def addEq(KB, equation):  # add an equation to the KB
    # reduce the new equation by every equation in the KB
    reduceEq(KB, equation)
    if(len(equation) < 2):  # if the equation is already contained in the KB or gets reduced to nothing, skip
        return KB
    # reduce every equation in the KB by reduced new equation
    reduceKB(KB, equation)
    KB.append(equation)  # insert the new equation into the KB
'''
ReduceKB handles taking the new equation and figuring out if it is a subset.
Then we construct the set difference and the difference in the constraint values. 

'''
def reduceKB(KB, newEq):
    modified = [newEq]
    while len(modified) > 0:
        newEq = modified[0]
        newEqLen = len(newEq)
        for i in range(len(KB)):
            KBEqLen = len(KB[i])
            # if newEq is a subset of an equation in KB
            if (newEqLen <= KBEqLen and KB[i][KBEqLen - 1] >= newEq[newEqLen - 1] and KB[i] != newEq and set(newEq[0: newEqLen - 1]).issubset(set(KB[i][0: KBEqLen - 1]))):
                # store the difference of the constraint values
                constraintDifference = KB[i][KBEqLen - 1] - newEq[newEqLen - 1]

                # find the set difference
                e = list(set(KB[i][0: KBEqLen - 1]) -
                         set(newEq[0: newEqLen - 1]))
                # append the constaint difference to the end of the equation
                e.append(constraintDifference)
                if(e not in KB):
                    KB[i] = e
                    modified.append(e)
                else:
                    KB[i] = []
        modified.remove(modified[0])
        while([] in KB):
            KB.remove([])

'''
    ReduceEq reduces an Equation by the entire Knowledge Base. A set difference
    and constraint value are constructed if there exists a subset between any equation
    in the knowledge base and the equation we want to add to the Knowledge Base.
    
'''
def reduceEq(KB, newEq):
    for eq in KB:  # for every equation eq in the KB, reduce the new equation by eq
        eqLen = len(eq)
        newEqLen = len(newEq)
        # if eq is a subset of the new equation
        if (eqLen <= newEqLen and set(eq[0: eqLen - 1]).issubset(set(newEq[0: newEqLen - 1]))):
            #newEqLength = len(newEq)
            # store the difference of the constraint values
            constraintDifference = newEq[newEqLen - 1] - eq[eqLen - 1]
            # find the set difference
            newEq.extend(
                list(set(newEq[0: newEqLen - 1]) - set(eq[0: eqLen - 1])))
            # append the constaint difference to the end of the equation
            newEq.append(constraintDifference)
            for _ in range(newEqLen):
                newEq.remove(newEq[0])

def tupleToIndex(r, c, dim):
    return dim * r + c  # converts cell tuples to unique integers


def indexToTuple(i, dim):
    # converts the unique integers back into their respective tuples
    return (int(i / dim), i % dim)
