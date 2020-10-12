from Agent import Agent,Cell 
from Board import Board
import random as rnd

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
        print((r,c))
        display(dim,agent)


def display(dim,agent):
    display = Board(dim)
    for i in range(0,dim):
        for j in range(0,dim):
            if( (i,j) in agent.trippedMineCoords):
                display.board[i][j] = '2'
            elif((i,j) in agent.identifiedMineCoords):
                display.board[i][j] = '1'
            elif((i,j) in agent.revealedCoords):
                display.board[i][j] = '9'
            else:
                continue
    print(display.board)


dim = 5
gb = Board(dim)
gb.set_mines(dim)

print(gb.board)

ag = Agent(dim)
strategy1(gb,dim,ag)

display(dim,ag)