from common import Agent, Board, display
from strategy2 import strategy2
import numpy as np
import matplotlib.pyplot as plt

def testStrategy():
    dim = 10 # start value for dim, up to 50 hopefully
    mineDensity = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] # start value for mineDensity, up to 0.7
    plotDict = {}

    biglist = []
    while dim <= 50:
        print('dim= ', dim)
        averages = []
        for m in mineDensity:
            successRate = []
            for i in range(1):
                gb = Board(dim)
                gb.set_mines((dim**2)*m)
                corners = [(0, 0), (0, dim - 1), (dim - 1, 0), (dim - 1, dim - 1)]
                ag = Agent(dim=dim, preferredCoords=corners)
                strategy2(gb, dim, ag)
                result = display(dim, ag)
                #print('result:', result)
                successRate.append(result)
            successRate = np.asarray(successRate)
            averages.append(np.average(successRate))
        print(averages)
        biglist.append(averages)
        dim += 10

    f, ax = plt.subplots(2,1)
    dim = 10
    for i in range(0, 5):
        ax[i].plot(mineDensity, biglist[i])
        ax[i].set_title('Board with Dimension {}'.format(dim))
        ax[i].xlabel('Mine Density')
        ax[i].ylabel('Average Final Score')
        dim += 10
    f.show()
    print(biglist)
testStrategy()
    