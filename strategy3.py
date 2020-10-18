import random as rnd
from collections import deque
from queue import Queue

import numpy as np

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
    minesToIdentify = deque()
    safeToReveal = deque()

    # pick a corner at random to start the game
    corners = [(0, 0), (0, gboard.dim-1), (gboard.dim-1, 0),
               (gboard.dim-1, gboard.dim-1)]
    coord = corners[rnd.randint(0, 3)]
    firstCell = agent.checkCell(coord, gboard)
    clue = firstCell.type

    # based on revelation from first pick, update KB accordingly
    if not(clue == Cell.MINE):
        neighbors = firstCell.neighbors
        if clue == 3:
            for n in neighbors:
                agent.identifyMine(n)
        elif clue == 0:
            for n in neighbors:
                agent.revealedCoords.append(n)
        else:
            for n in neighbors:
                agent.board[n].probability = clue / 3

    # the actual game loop (until all Cells on Agent Board have been explored)
    while not(agent.isFinished()):

        identify_Mines_Safes(agent, minesToIdentify, safeToReveal)
        if minesToIdentify:
            cell = minesToIdentify.popleft()
            agent.identifyMine(cell.coords)
            continue
        elif safeToReveal:
            cell = safeToReveal.popleft()
            agent.checkCell(cell.coords, gboard)
            continue
        else:
            minCellCoords = findMinCell(agent)
            agent.checkCell(minCellCoords, gboard)

        calculateProbability(agent)

    return


def calculateProbability(self, agent):  # bulk of strategy 3
    return

# identify which Cells are safe and/or mines


def identify_Mines_Safes(self, agent, minesToIdentify, safeToReveal):
    #count = 0
    for row in agent.board:
        for c in row:
            if c.probability == 1:
                minesToIdentify.append(c)
                # agent.board.identifyMine(c.coords)
                #count += 1
            elif c.probability == 0:
                safeToReveal.append(c)
                # agent.revealedCoords.append(c.coords)
                #count += 1
            # might need to put calculateProbability again here because we want to calculate at each time the agent makes a move
            # calculateProbability(agent)
    # return count == 0

# find the coordinates of Cell on the board with the minimum probability of being mine


def findMinCell(self, agent):
    min_prob = 2
    final_coords = None
    for row in agent.board:
        for c in row:
            if c.probability < min_prob and c.probability > 0:
                min_prob = c.probability
                final_coords = c.coords
    return final_coords
