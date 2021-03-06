from common import Board, Agent, display, findNeighboringCoords
from strategy2 import strategy2
import numpy as np

def hardBoard(n,dim):
    gboard = Board(dim)
    gboard.set_mines(dim**2 * 0.4)
    agent = Agent(dim)
    mineList = gboard.minelist.copy()
    # finalList = mineList.copy()

    strategy2(gboard,dim, agent)
    worstScore = display(dim, agent)
    firstScore = worstScore
    #print('first score:', firstScore)

    length = len(gboard.minelist)
    #print('length of mineList:', length)
    j = 0
    while j < n:
        for mine in mineList:
            # if mineList.index(mine) % 10 == 0:
            #     print('exploring mine:', mineList.index(mine), '/', length)
            neighbors = findVHNeighbors(mine, dim)
            mineList, worstScore = findWorstAmongNeighbors(neighbors, mineList, mine, dim, worstScore)
        b = Board(dim)
        b.set_specific_mines(mineList)
        #print(b.board)
        #print('final score:', worstScore)
        j += 1
    return firstScore, worstScore

def findVHNeighbors(coords, dim):
    neighbors = []
    row, col = coords
    r1 = row - 1
    r2 = row + 1
    c1 = col - 1
    c2 = col + 1
    while r1 >= 0:
        neighbors.append((r1,col))
        r1 -= 1
    while r2 < dim:
        neighbors.append((r2, col))
        r2 += 1
    while c1 >= 0:
        neighbors.append((row,c1))
        c1 -= 1
    while c2 < dim:
        neighbors.append((row,c2))
        c2 += 1
    return neighbors

def findWorstAmongNeighbors(locations, mineList, currentMine, dim, worstScore):
    #referenceList = mineList.copy()
    successTracker = {} # keeps track of average successRate for each neighbor
    listTracker = {} # keeps track of mine lists generated for each neighbor
    agent = Agent(dim) 
    #print("worst score:", worstScore)
    for n in locations: # iterate through neighbors
        if n in mineList: # ignore all configs where mine is moved to another mine location
            continue
        referenceList = mineList.copy() # copy the orginal Mine List to run the sims
        referenceList.remove(currentMine) # remove where the mine currently is
        referenceList.append(n) # add where the mine should now be in the sim
# ---------------------------------------------------------------------------------------------------      
        tBoard = Board(dim)
        tBoard.set_specific_mines(referenceList)
        strategy2(tBoard, dim,agent)
        successTracker[display(dim,agent)] = n
        listTracker[n] = referenceList
        
# ---------------------------------------------------------------------------------------------------
        
        # i = 0
        # sumSuccessRate = 0
        # while (i < 10): # should be 30 for stat significant
        #     testBoard = Board(dim) 
        #     testBoard.set_specific_mines(referenceList) # generate a board with the specific mines
        #     strategy2(testBoard, dim, agent) 
        #     sumSuccessRate += display(dim, agent)
        #     agent.reset()
        #     i += 1
        # successTracker[float(sumSuccessRate)/10] = n
        # #print("list of successes:", successTracker)
        # listTracker[n] = referenceList
# ---------------------------------------------------------------------------------------------------
    if not successTracker:
        return mineList.copy(), worstScore
    lowest = min(successTracker.keys())
    if lowest <= float(worstScore):
        finder = successTracker[lowest]
        finalList = listTracker[finder]
        return finalList.copy(), lowest

    return mineList.copy(), worstScore # gonna have to change the list