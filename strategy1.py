from common import Agent, Cell, Board, display
import random as rnd
import time

'''
Check if any neighboring cells to an inputted cell are mine cells based on the inputted mine's clue.
'''

def identify_mine_neighbors(agent, gboard, coords):
    r,c = coords
    if((gboard.board[r][c] - agent.board[r][c].numMineNeighbors) == agent.board[r][c].numHiddenNeighbors):
        for cn in agent.board[r][c].neighbors:
            if(agent.board[cn[0]][cn[1]].revealed == False):
                agent.identifyMine(cn)
    return

'''
Check if any neighboring cells to an inputted cell are safe cells based on the inputted mine's clue.
'''

def identify_safe_neighbors(agent,gboard,coords):
    r,c = coords
    if((len(agent.board[r][c].neighbors) - gboard.board[r][c] - agent.board[r][c].numSafeNeighbors) == agent.board[r][c].numHiddenNeighbors):
        for cn in agent.board[r][c].neighbors:
            #If an univisted cell is determined to be safe, check if any of that cells neighbors can be determined to be mine cells or safe cells.
            if(agent.board[cn[0]][cn[1]].revealed == False):
                agent.checkCell(cn,gboard)
                identify_mine_neighbors(agent,gboard,(cn[0],cn[1]))
                identify_safe_neighbors(agent,gboard,(cn[0],cn[1]))
    return

'''
Run strategy 1. 
1. Select a random unvisited cell
2. Reveal the cell
3. Check if any of the cell's neighbors can be inferred to be mine cells or safe cells
Repeat until all cells are visited or flagged
'''

def strategy1(gboard,dim,agent):
    #Initially pick a random cell
    while((dim*dim) - len(agent.revealedCoords) - len(agent.identifiedMineCoords) != 0):
        r = rnd.randint(0,dim-1)
        c = rnd.randint(0,dim-1)
        #If the cell has been visited or flagged as a mine cell, pick another cell
        while ((r,c) in agent.revealedCoords or (r,c) in agent.identifiedMineCoords):
            r = rnd.randint(0,dim-1)
            c = rnd.randint(0,dim-1)
        #Check the cell and identify neighbors as mine cells or safe cells if possible.
        agent.checkCell((r,c),gboard)
        identify_mine_neighbors(agent,gboard,(r,c))
        identify_safe_neighbors(agent,gboard,(r,c))