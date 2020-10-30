from common import Board, Agent, display, findNeighboringCoords
from strategy2 import strategy2

def hardBoard(dim):
    gboard = Board(dim)
    gboard.set_mines(dim**2 * 0.7)
    agent = Agent(dim)
    mineList = gboard.minelist.copy()
    # finalList = mineList.copy()

    strategy2(gboard,dim, agent)
    worstScore = display(dim, agent)
    print('first score:', worstScore)

    length = len(gboard.minelist)
    for mine in gboard.minelist:
        print(mine)
        neighbors = findNeighboringCoords(mine, dim)
        mineList, worstScore = findWorstAmongNeighbors(neighbors, mineList, mine, dim, worstScore)
    print(worstScore)



def findWorstAmongNeighbors(locations, mineList, currentMine, dim, worstScore):
    #referenceList = mineList.copy()
    successTracker = {} # keeps track of average successRate for each neighbor
    listTracker = {} # keeps track of mine lists generated for each neighbor
    agent = Agent(dim) 
    print("worst score:", worstScore)
    for n in locations: # iterate through neighbors
        if n in mineList: # ignore all configs where mine is moved to another mine location
            continue
        referenceList = mineList.copy() # copy the orginal Mine List to run the sims
        referenceList.remove(currentMine) # remove where the mine currently is
        referenceList.append(n) # add where the mine should now be in the sim
        i = 0
        sumSuccessRate = 0
        while (i < 10): # should be 30 for stat significant
            testBoard = Board(dim) 
            testBoard.set_specific_mines(referenceList) # generate a board with the specific mines
            strategy2(testBoard, dim, agent) 
            sumSuccessRate += display(dim, agent)
            agent.reset()
            i += 1
        successTracker[float(sumSuccessRate)/10] = n
        #print("list of successes:", successTracker)
        listTracker[n] = referenceList

    if not successTracker:
        return mineList.copy(), worstScore
    lowest = min(successTracker.keys())
    if lowest <= float(worstScore):
        finder = successTracker[lowest]
        finalList = listTracker[finder]
        return finalList.copy(), lowest

    return mineList.copy(), worstScore # gonna have to change the list


hardBoard(10)