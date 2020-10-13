from Agent import Agent,Cell 
from Board import Board
from queue import Queue
import random as rnd
import numpy as np

def strategy2(gboard, dim, agent):
    coeffs = []
    constants = []
    inferredSafeQueue = Queue(maxsize = dim*dim)
    cellTypes = []
    
    r = rnd.randint(0,dim-1)
    c = rnd.randint(0,dim-1)
    while((dim*dim) - len(agent.revealedCoords) - len(agent.identifiedMineCoords) != 0):
        while ((r,c) in agent.revealedCoords or (r,c) in agent.identifiedMineCoords):
            r = rnd.randint(0,dim-1)
            c = rnd.randint(0,dim-1)
        currentCell = agent.checkCell((r,c),gboard)
        if (currentCell.type == -1):
            newEq = np.zeros([dim**2], dtype=int)
            newEq[tupleToIndex(r, c, dim)] = 1
            coeffs.append(newEq)
            constants.extend([1])
            cellTypes = np.linalg.solve(coeffs, constants)

        else:
            cellTypes[currentCell.coords[0]][currentCell.coords[1]] = 0
            cellClues[currentCell.coords[0]][currentCell.coords[1]] = currentCell.type


        print((r,c))
        display(dim,agent)

def tupleToIndex(r, c, dim):
    return dim * r + c #converts cell tuples to unique integers
def indexToTuple(i, dim):
    return (int(i / dim), i % dim) #converts the unique integers back into their respective tuples

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


# dim = 5
# gb = Board(dim)
# gb.set_mines(dim)

# print(gb.board)

# ag = Agent(dim)
# strategy2(gb,dim,ag)

# display(dim,ag)

a = [[1, 1],[-1, 1]]
b = [2, 0]
print(np.linalg.solve(a,b))