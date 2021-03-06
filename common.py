import random as rnd

import numpy as np

'''
Define a Board class. This class keeps track of a "board" as a 2-dimensional array of integers representing the status of each location in this maze
'''

class Board:
    def __init__(self, dim):
        self.board = np.zeros([dim, dim], dtype=int)
        self.dim = dim
        self.num_mines = 0
        self.minelist = []

    #randomly place num_mines mines in the board
    def set_mines(self, num_mines):
        count = 0
        self.num_mines = num_mines
        while count < num_mines:
            pos = rnd.randint(0, self.dim*self.dim-1)
            row = pos // self.dim
            col = pos % self.dim
            if self.board[row][col] != Cell.MINE:
                self.board[row][col] = Cell.MINE
                self.minelist.append((row, col))
                #for each mine placed, increment the neighbors clue value by 1.
                neighbors = findNeighboringCoords((row, col), self.dim)
                for n in neighbors:
                    nrow, ncol = n
                    if self.board[nrow][ncol] != Cell.MINE:
                        self.board[nrow, ncol] += 1
                count += 1
    
    def set_specific_mines(self, locations):
        count = 0
        self.num_mines = len(locations)
        for (row, col) in locations:
            if self.board[row][col] != Cell.MINE:
                self.board[row][col] = Cell.MINE
                self.minelist.append((row, col))
                # update neighbors here
                neighbors = findNeighboringCoords((row, col), self.dim)
                for n in neighbors:
                    nrow, ncol = n
                    if self.board[nrow][ncol] != Cell.MINE:
                        self.board[nrow, ncol] += 1
                count += 1

    def isSolved(self, num_discovered):
        return num_discovered == self.num_mines

'''
Define an Agent class. This class keeps track of the agents moves using a 2-dimensional array of integers.
'''

class Agent:
    def __init__(self, dim, preferredCoords=[]):
        self.dim = dim
        self.revealedCoords = []
        self.trippedMineCoords = []
        self.identifiedMineCoords = []
        self.preferredCoords = preferredCoords
        self.board = []
        for r in range(dim):
            col = []
            for c in range(dim):
                col.append(Cell((r, c), dim))
            self.board.append(col)

    #update the agent with the information associated with a newly revealed cell. 
    def checkCell(self, coords, masterBoard):
        row, col = coords
        self.revealedCoords.append(coords)
        cell = self.board[row][col]
        cell.revealed = True
        cell.type = masterBoard.board[row, col]
        if cell.type == Cell.MINE:
            self.trippedMineCoords.append(coords)
        for neighbor in cell.neighbors:
            nRow, nCol = neighbor
            neighborCell = self.board[nRow][nCol]
            neighborCell.numHiddenNeighbors -= 1
            if cell.type == Cell.MINE:
                neighborCell.numMineNeighbors += 1
            else:
                neighborCell.numSafeNeighbors += 1
        return cell

    # Does not check for false positives --> must be 100% certain that given coords are a mine
    def identifyMine(self, coords):
        row, col = coords
        cell = self.board[row][col]
        cell.type = Cell.MINE
        self.identifiedMineCoords.append(coords)
        for neighbor in cell.neighbors:
            nRow, nCol = neighbor
            neighborCell = self.board[nRow][nCol]
            neighborCell.numMineNeighbors += 1
        return cell

    #check if a cell has been visited
    def hasExplored(self, coords):
        return coords in self.revealedCoords or coords in self.identifiedMineCoords

    #check if all cells have been visited
    def isFinished(self):
        return len(self.revealedCoords) + len(self.identifiedMineCoords) >= self.dim**2

    #choose from preferred coords if not visited, otherwise generate a random unvisited cell
    def choosePreferredOrRandomCoords(self):
        r = c = -1
        for preferredCoords in self.preferredCoords:
            if not self.hasExplored(preferredCoords):
                r, c = preferredCoords
                break
        if r == -1 and c == -1:
            r, c = self.chooseRandomCoords()
        return r, c

    #choose a random unexplored cell
    def chooseRandomCoords(self):
        r = rnd.randint(0, self.dim - 1)
        c = rnd.randint(0, self.dim - 1)
        while self.hasExplored((r, c)):
            r = rnd.randint(0, self.dim - 1)
            c = rnd.randint(0, self.dim - 1)
        return r, c


class Cell:
    UNCHECKED = -2
    MINE = -1

    def __init__(self, coords, dim):
        self.coords = coords
        self.type = self.UNCHECKED
        self.revealed = False
        self.neighbors = findNeighboringCoords(coords, dim)
        self.numHiddenNeighbors = len(self.neighbors)
        self.numSafeNeighbors = 0
        self.numMineNeighbors = 0
        self.probabilityIsMine = 0

    def isIdentifiedMine(self):
        return not self.revealed and self.type == self.MINE


def findNeighboringCoords(coords, dim):
    cellRow, cellCol = coords
    potentialNeighbors = [(cellRow-1, cellCol-1),
                          (cellRow-1, cellCol),
                          (cellRow-1, cellCol+1),
                          (cellRow, cellCol-1),
                          (cellRow, cellCol+1),
                          (cellRow+1, cellCol-1),
                          (cellRow+1, cellCol),
                          (cellRow+1, cellCol+1),
                          ]
    neighbors = []
    for pn in potentialNeighbors:
        r, c = pn
        if (r >= dim or r < 0 or c >= dim or c < 0):
            continue
        neighbors.append(pn)
    return neighbors


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
    # print(display.board)
    # print("Tripped Mines: " + str(len(agent.trippedMineCoords)))
    # print("Identified Mines: " + str(len(agent.identifiedMineCoords)))
    # print("Revealed Cells: " + str(len(agent.revealedCoords)))
    # print("Identified Mines/Total Mines: " + str(len(agent.identifiedMineCoords) / (len(agent.trippedMineCoords) + len(agent.identifiedMineCoords))))
    return float(len(agent.identifiedMineCoords)) / float(len(agent.trippedMineCoords) + len(agent.identifiedMineCoords))