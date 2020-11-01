import matplotlib.pyplot as plt
import numpy as np
from hardBoard import hardBoard
from common import Agent, Board, display

def testing():
    dim = 5
    mineDensities = [0.1 * x for x in range(1,10)]
    while dim <= 25:
        averagesFirst = []
        averagesLast = []
        for m in mineDensities:
            i = 0
            firstSuccess = []
            finalSuccess = []
            while i < 30:
                #print('mineDen: ', m, 'iteration: ', i)
                x,y = hardBoard(1, dim)
                firstSuccess.append(x)
                finalSuccess.append(y)
                i += 1
            averagesFirst.append(np.average(firstSuccess))
            averagesLast.append(np.average(finalSuccess))
        print('For Dimension {}:'.format(dim))
        print('Intial Success Rate: ', np.average(firstSuccess))
        print('Forced Success Rate: ', np.average(finalSuccess))
        plt.figure(figsize=(10,10))
        plt.plot(mineDensities, averagesFirst, label='Initial Success Rate')
        plt.plot(mineDensities, averagesLast, label='Forced Success Rate')
        plt.title('Performance of Standard vs Hard Board for Dimension {}'.format(dim))
        plt.ylim(0,1)
        plt.xlabel('Mine Density')
        plt.ylabel('Average Success Rate')
        plt.legend(loc='best')
        plt.savefig('diffBoardDim{}.png'.format(dim))
        dim += 5

testing()