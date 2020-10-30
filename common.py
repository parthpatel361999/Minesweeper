import random as rnd

import numpy as np


class Board:
    def __init__(self, dim):
        self.board = np.zeros([dim, dim], dtype=int)
        self.dim = dim
        self.num_mines = 0
        self.minelist = []
    def set_mines(self, num_mines):
        count = 0
        self.num_mines = num_mines
        while count < num_mines:
            pos = rnd.randint(0, self.dim*self.dim-1)
            row = pos // self.dim
            col = pos % self.dim
            if self.board[row][col] != Cell.MINE:
                self.board[row][col] = Cell.MINE
                self.minelist.append((row,col))
                # update neighbors here
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
                # update neighbors here
                neighbors = findNeighboringCoords((row, col), self.dim)
                for n in neighbors:
                    nrow, ncol = n
                    if self.board[nrow][ncol] != Cell.MINE:
                        self.board[nrow, ncol] += 1
                count += 1

    def isSolved(self, num_discovered):
        return num_discovered == self.num_mines


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

    def reset(self):
        self.revealedCoords = []
        self.trippedMineCoords = []
        self.identifiedMineCoords = []
        #self.preferredCoords = preferredCoords
        self.board = []
        for r in range(self.dim):
            col = []
            for c in range(self.dim):
                col.append(Cell((r, c), self.dim))
            self.board.append(col)
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

    def hasExplored(self, coords):
        return coords in self.revealedCoords or coords in self.identifiedMineCoords

    def isFinished(self):
        return len(self.revealedCoords) + len(self.identifiedMineCoords) >= self.dim**2

    def choosePreferredOrRandomCoords(self):
        r = c = -1
        for preferredCoords in self.preferredCoords:
            if not self.hasExplored(preferredCoords):
                r, c = preferredCoords
                break
        if r == -1 and c == -1:
            r, c = self.chooseRandomCoords()
        return r, c

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
    potentialNeighbors = [(cellRow, cellCol+1),
                          (cellRow, cellCol-1),
                          (cellRow+1, cellCol),
                          (cellRow-1, cellCol),
                          (cellRow+1, cellCol+1),
                          (cellRow-1, cellCol-1),
                          (cellRow+1, cellCol-1),
                          (cellRow-1, cellCol+1)
                          ]
    neighbors = []
    for pn in potentialNeighbors:
        r, c = pn
        if (r >= dim or r < 0 or c >= dim or c < 0):
            continue
        neighbors.append(pn)
    return neighbors


def display(dim, agent):
    numTripped = 0
    numIdentifiedMines = 0
    numRevealed = 0
    display = Board(dim)
    for i in range(0, dim):
        for j in range(0, dim):
            if((i, j) in agent.trippedMineCoords):
                display.board[i][j] = '2'
                numTripped += 1
            elif((i, j) in agent.identifiedMineCoords):
                display.board[i][j] = '1'
                numIdentifiedMines += 1
            elif((i, j) in agent.revealedCoords):
                display.board[i][j] = '9'
                numRevealed += 1
            else:
                continue

    return float(numIdentifiedMines) / float(numTripped + numIdentifiedMines)
    # print(display.board)
    # print("Tripped Mines: " + str(numTripped))
    # print("Identified Mines: " + str(numIdentifiedMines))
    # print("Revealed Cells: " + str(numRevealed))
    # print("Identified Mines/Total Mines: " +
    #       str(numIdentifiedMines / (numTripped + numIdentifiedMines)))
