from Board import findNeighboringCoords


class Agent:
    def __init__(self, dim):
        self.dim = dim
        self.revealedCoords = []
        self.trippedMineCoords = []
        self.identifiedMineCoords = []
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
