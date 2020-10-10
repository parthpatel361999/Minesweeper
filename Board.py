import random as rnd

import numpy as np


class Board:
    def __init__(self, dim):
        self.board = np.zeros([dim, dim], dtype=int)
        self.dim = dim
        self.num_mines = 0

    def set_mines(self, num_mines):
        count = 0
        self.num_mines = num_mines
        while count < num_mines:
            pos = rnd.randint(0, self.dim*self.dim-1)
            row = pos // self.dim
            col = pos % self.dim
            if self.board[row][col] != -1:
                self.board[row][col] = -1
                # update neighbors here
                neighbors = findNeighboringCoords((row, col), self.dim)
                for n in neighbors:
                    nrow, ncol = n
                    if self.board[nrow][ncol] != -1:
                        self.board[nrow, ncol] += 1
                count += 1


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


b = Board(10)
b.set_mines(8)
print(b.board)
