import copy
import random as rnd
from collections import deque

from common import Agent, Board, Cell
from commonCSP import addEq, checkForInference, indexToTuple, tupleToIndex

def strat3(gboard, agent, dim):
    KB = []
    unknownVars = set()
    
    r,c = agent.choosePreferredorRandomCoords()

    while not agent.isFinished():
        currentCell = agent.checkCell((r, c), gboard)
        if currentCell.type == Cell.MINE:
            KB = addMineEq(KB, currentCell, dim)
        else:
            KB = addSafeEq(KB, currentCell, dim, agent, variables)


def addSafeEq(KB, cell, dim, agent, variables=None):
    """
    Add an equation identifying the cell's coordinates as safe to the knowledge base. Then, create a clue 
    equation for all of the cell's neighbors, and add those neighbors to the unknown variables list if
    they haven't been explored by the agent already.
    """
    if variables is None:
        variables = set()
    r, c = cell.coords
    safeEq = [tupleToIndex(r, c, dim), 0]
    KB = addEq(KB, safeEq)
    clueEq = []
    for neighbor in cell.neighbors:
        nRow, nCol = neighbor
        neighborIndex = tupleToIndex(nRow, nCol, dim)
        clueEq.append(neighborIndex)
        if not agent.hasExplored(neighbor):
            variables.add(neighborIndex)
    clueEq.append(cell.type)
    KB = addEq(KB, clueEq)
    return KB

    def addMineEq(KB, cell, dim):
        """
        Add an equation identifying the cell's coordinates as a mine to the knowledge base. 
        """
        r, c = cell.coords
        mineEq = [tupleToIndex(r, c, dim), 1]
        KB = addEq(KB, mineEq)
        return KB