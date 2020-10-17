from Agent import Agent,Cell 
from Board import Board
from queue import Queue
import random as rnd
import numpy as np

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
    corners = [(0,0), (0,gboard.dim-1), (gboard.dim-1,0), (gboard.dim-1, gboard.dim-1)]
    coord = corners[rnd.randint(0,3)]
    firstCell = agent.checkCell(coord, gboard)
    clue = firstCell.type
    
    if not(clue == -1):
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

    while not(agent.isFinished()):

        calculateProbability(agent) # this gonna be the bulk of strat3
        if not(identify_Mines_Safes(agent)):
            cellToIdentify = findMinCell(agent)
            agent.identifyMine(cellToIdentify)
        break        

    return

def calculateProbability(self, agent):
    return

def identify_Mines_Safes(self, agent):
    count = 0
    for row in agent.board:
        for c in row:
            if c.probability == 1:
                agent.board.identifyMine(c.coords)
                count += 1
            elif c.probability == 0:
                agent.revealedCoords.append(c.coords)
                count += 1
            # might need to put calculateProbability again here because we want to calculate at each time the agent makes a move
            # calculateProbability(agent)
    return count == 0

def findMinCell(self, agent):
    min_prob = 2
    final_coords = None
    for row in agent.board:
        for c in row:
            if c.probability < min_prob and c.probability > 0:
                min_prob = c.probability
                final_coords = c.coords
    return final_coords

    

