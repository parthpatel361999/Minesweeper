import random as rnd

from Agent import Agent, Cell
from Board import Board


# double improved agent
def strategy3(gboard, dim, agent):
    """
    Basic Outline for Algo:
        1. Pick one of the corner cells
        2. Compute probability that a cell contains a mine, for all cells
        3. For cell in board, if P(cell = mine) = 1, mark cell as mine
        4. For cell in board, if P(cell = mine) = 0, reveal and add to knowledge base
        5. If no cell was safe, pick minimum probability in the board
    """

    # pick a corner at random to start the game
    corners = [(0, 0), (0, dim - 1), (dim - 1, 0),
               (dim - 1, dim - 1)]
    coords = corners[rnd.randint(0, len(corners))]
    firstCell = agent.checkCell(coords, gboard)
    clue = firstCell.type
    corners.remove(coords)

    while clue == Cell.MINE:
        if len(corners) == 0:
            coords = (rnd.randint(0, dim), rnd.randint(0, dim))
        else:
            coords = corners[rnd.randint(0, len(corners))]
            corners.remove(coords)
        firstCell = agent.checkCell(coords, gboard)
        clue = firstCell.type

    # based on revelation from first pick, update KB accordingly
    neighbors = firstCell.neighbors
    if clue == len(firstCell.neighbors):
        for n in neighbors:
            agent.identifyMine(n)
    elif clue == 0:
        for n in neighbors:
            agent.checkCell(n)
    else:
        for n in neighbors:
            agent.board[n].probability = clue / len(firstCell.neighbors)

    # the actual game loop (until all Cells on Agent Board have been explored)

    while not agent.isFinished():
        cell, status = calculateProbability(agent)
        if status == Cell.MINE:
            agent.identifyMine(cell.coords)
        else:
            agent.checkCell(cell.coords)

    return


def calculateProbability(agent):  # bulk of strategy 3
    minProbability = 1
    minProbabilityCell = None
    # probability logic
    currCellProbability = -1  # prob will end up starting with another val
    currCell = None
    # loop for probabilty
    while True:
        # logic logic logic
        if currCellProbability == 1:
            return (currCell, Cell.MINE)
        elif currCellProbability == 0:
            return (currCell, Cell.SAFE)

        if currCellProbability < minProbability:
            minProbability = currCellProbability
            minProbabilityCell = currCell

    return (minProbabilityCell, Cell.UNCHECKED)
