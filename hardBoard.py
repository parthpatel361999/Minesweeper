from common import Board, Agent, display, findNeighboringCoords
from strategy2 import strategy2


def hello(dim):
    gboard = Board(dim)
    gboard.set_mines(dim**2 * 0.4)
    agent = Agent(dim)
    mineList = gboard.minelist.copy()
    finalList = mineList.copy()

    strategy2(gboard,dim, agent)
    worstScore = display(dim, agent)
    
    print(len(gboard.minelist))
    for mine in gboard.minelist:
        #mineList = gboard.minelist.copy()
        # row, col = mine
        print(gboard.minelist.index(mine))
        neighbors = findNeighboringCoords(mine, dim)
        for n in neighbors:
            if n in mineList:
                continue
            totalSuccessRate = 0
            for i in range(10):
                mineList = gboard.minelist.copy()
                simBoard = Board(dim)
                mineList.remove(mine)
                mineList.append((n[0],n[1]))
                simBoard.set_specific_mines(mineList)
                agent.reset()
                strategy2(simBoard, dim, agent)
                currentScore = display(dim, agent) # the last thing to change is right here i gotta do an average of however many
                totalSuccessRate += currentScore
            averageScore = totalSuccessRate/10
            if averageScore <= worstScore: # times instead of just once
                worstScore = averageScore
                finalList = mineList.copy()
    

    return worstScore, finalList

w, f = hello(dim=5)
print(w)
print(f)