from Agent import Agent,Cell 
from Board import Board, findNeighboringCoords
from queue import Queue
import random as rnd
import numpy as np

def strategy2(gboard, dim, agent):
    coeffs = []
    constants = []
    cellTypes = []
    inferredSafeQueue = Queue(maxsize = dim*dim)
    
    r = rnd.randint(0,dim-1)
    c = rnd.randint(0,dim-1)
    while((dim*dim) - len(agent.revealedCoords) - len(agent.identifiedMineCoords) != 0): #run until all cells are explored
        while ((r,c) in agent.revealedCoords or (r,c) in agent.identifiedMineCoords): #pick coordinates again if cell has already been explored
            r = rnd.randint(0,dim-1)
            c = rnd.randint(0,dim-1)
        currentCell = agent.checkCell((r,c),gboard) #check the cell at (r, c)
        if (currentCell.type == -1):
            newEq = np.zeros([dim**2], dtype=int)
            newEq[tupleToIndex(r, c, dim)] = 1
            coeffs.append(newEq) #add the new equation to the KB matrix
            constants.extend([1]) #add 1 to the constants vector
            cellTypes = np.linalg.solve(coeffs, constants) #attempt to solve the new system
            #check to see if new cells are inferred safe now
            #add those inferred safe cells to inferredSafeQeue and choose next cell from there
            #if the inferredSafeQueue is empty generate a random cell to inspect
        else:
            newEq = np.zeros([dim**2], dtype=int)
            neighbors = findNeighboringCoords((r, c), dim)
            for n in neighbors:
                newEq[tupleToIndex(n[0], n[1], dim)] = 1
            coeffs.append(newEq) #add the new equation to the KB matrix
            constants.extend(currentCell.type) #add the clue value to the constants vector
            cellTypes = np.linalg.solve(coeffs, constants) #attempt to solve the new system
            #check to see if new cells are inferred safe now
            #add those inferred safe cells to inferredSafeQeue and choose next cell from there
            #if the inferredSafeQueue is empty generate a random cell to inspect


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