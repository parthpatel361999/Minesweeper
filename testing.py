from common import Agent, Board, display
from strategy4 import strategy4
from strategy3 import strategy3
from strategy2 import strategy2
from strategy1 import strategy1
import numpy as np
import matplotlib.pyplot as plt
import sys

def testStrategy(strat):
    dim = 10 # start value for dim, up to 50 hopefully
    mineDensity = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] # start value for mineDensity, up to 0.7
    i = 0
    while dim <= 50: #change to 50
        print('dim= ', dim)
        averages = []
        for m in mineDensity:
            successRate = []
            for i in range(30): #change to 30
                gb = Board(dim)
                gb.set_mines((dim**2)*m)
                corners = [(0, 0), (0, dim - 1), (dim - 1, 0), (dim - 1, dim - 1)]
                ag = Agent(dim=dim, preferredCoords=corners)
                if(strat == 1):
                    strategy1(gb, dim, ag)
                elif(strat == 2):
                    strategy2(gb, dim, ag)
                elif(strat == 3):
                    strategy3(gb, dim, ag)
                elif(strat == 4):
                    strategy4(gb, dim, ag)
                result = display(dim, ag)
                #print('result:', result)
                successRate.append(result)
            successRate = np.asarray(successRate)
            averages.append(np.average(successRate))
        print(averages)

        fig = plt.figure(figsize=(12,12))
        plt.ylim(0,1)
        plt.scatter(mineDensity,averages,c='#1f77b4', s=10)
        for j in range(len(mineDensity)):
            plt.text(mineDensity[j], averages[j], '('+'%.1f' % mineDensity[j]+', '+'%.3f'%averages[j]+')', size='x-small', in_layout=True, snap=True)
            #plt.annotate(text='('+'%.1f' % mineDensity[j]+', '+'%.3f'%biglist[i][j]+')', xy=(mineDensity[j], biglist[i][j]))
        plt.plot(mineDensity, averages)
        plt.title('Boards of Dimension {}'.format(dim))
        plt.xlabel('Mine Density')
        plt.ylabel('Average Final Score')
        plt.show()
        plt.close(fig)
        i += 1
        dim += 10

testStrategy(int(sys.argv[1]))