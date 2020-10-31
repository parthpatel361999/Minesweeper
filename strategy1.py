from common import Agent, Cell, Board, display
import random as rnd
import time

def identify_mine_neighbors(agent, gboard, coords):
    r,c = coords
    if((gboard.board[r][c] - agent.board[r][c].numMineNeighbors) == agent.board[r][c].numHiddenNeighbors):
        for cn in agent.board[r][c].neighbors:
            if(agent.board[cn[0]][cn[1]].revealed == False):
                agent.identifyMine(cn)
    return

def identify_safe_neighbors(agent,gboard,coords):
    r,c = coords
    if((len(agent.board[r][c].neighbors) - gboard.board[r][c] - agent.board[r][c].numSafeNeighbors) == agent.board[r][c].numHiddenNeighbors):
        for cn in agent.board[r][c].neighbors:
            if(agent.board[cn[0]][cn[1]].revealed == False):
                agent.checkCell(cn,gboard)
                identify_mine_neighbors(agent,gboard,(cn[0],cn[1]))
                identify_safe_neighbors(agent,gboard,(cn[0],cn[1]))
    return

def strategy1(gboard,dim,agent):
    while((dim*dim) - len(agent.revealedCoords) - len(agent.identifiedMineCoords) != 0):
        r = rnd.randint(0,dim-1)
        c = rnd.randint(0,dim-1)
        while ((r,c) in agent.revealedCoords or (r,c) in agent.identifiedMineCoords):
            r = rnd.randint(0,dim-1)
            c = rnd.randint(0,dim-1)
        agent.checkCell((r,c),gboard)
        identify_mine_neighbors(agent,gboard,(r,c))
        identify_safe_neighbors(agent,gboard,(r,c))

'''
dim = 50
gb = Board(dim)
gb.set_mines(int(0.4*dim**2))
print(gb.board)
ag = Agent(dim)
startTime = time.time()
strategy1(gb,dim,ag)
display(dim,ag)
endTime = time.time()
print("Time:", endTime - startTime,
        "seconds (" + str((endTime - startTime)/60), "min)")
'''