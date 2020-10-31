import random as rnd

from common import Agent, Board, Cell
from visualization import Visualizer


def identify_mine_neighbors(agent, gboard, coords, visualizer):
    r, c = coords
    if((gboard.board[r][c] - agent.board[r][c].numMineNeighbors) == agent.board[r][c].numHiddenNeighbors):
        for cn in agent.board[r][c].neighbors:
            if(agent.board[cn[0]][cn[1]].revealed == False):
                agent.identifyMine(cn)
                visualizer.createVisualization()
    return


def identify_safe_neighbors(agent, gboard, coords, visualizer):
    r, c = coords
    if((len(agent.board[r][c].neighbors) - gboard.board[r][c] - agent.board[r][c].numSafeNeighbors) == agent.board[r][c].numHiddenNeighbors):
        for cn in agent.board[r][c].neighbors:
            if(agent.board[cn[0]][cn[1]].revealed == False):
                agent.checkCell(cn, gboard)
                visualizer.createVisualization()
                identify_mine_neighbors(
                    agent, gboard, (cn[0], cn[1]), visualizer)
                identify_safe_neighbors(
                    agent, gboard, (cn[0], cn[1]), visualizer)
    return


def strategy1(gboard, dim, agent, visualizer):
    while((dim*dim) - len(agent.revealedCoords) - len(agent.identifiedMineCoords) != 0):
        r = rnd.randint(0, dim-1)
        c = rnd.randint(0, dim-1)
        while ((r, c) in agent.revealedCoords or (r, c) in agent.identifiedMineCoords):
            r = rnd.randint(0, dim-1)
            c = rnd.randint(0, dim-1)
        agent.checkCell((r, c), gboard)
        visualizer.createVisualization()

        identify_mine_neighbors(agent, gboard, (r, c), visualizer)
        identify_safe_neighbors(agent, gboard, (r, c), visualizer)
        # print((r,c))
        # display(dim,agent)


def display(dim, agent):
    display = Board(dim)
    for i in range(0, dim):
        for j in range(0, dim):
            if((i, j) in agent.trippedMineCoords):
                display.board[i][j] = '2'
            elif((i, j) in agent.identifiedMineCoords):
                display.board[i][j] = '1'
            elif((i, j) in agent.revealedCoords):
                display.board[i][j] = '9'
            else:
                continue
    print(display.board)


dim = 10
gb = Board(dim)
gb.set_mines(int(dim**2 * .4))

print(gb.board)

ag = Agent(dim)
vis = Visualizer(ag, 1)
strategy1(gb, dim, ag, vis)

display(dim, ag)
