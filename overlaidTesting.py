from common import Agent, Board, display
from strategy4 import strategy4
from strategy3 import strategy3
from strategy2 import strategy2
from strategy1 import strategy1
import numpy as np
import matplotlib.pyplot as plt

def testStrategy():
    dim = 10 # start value for dim, up to 50 hopefully
    mineDensity = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] # start value for mineDensity, up to 0.7
    #plotDict = {}

    #biglist = []
    dim = 100
    i = 0
    average = []
    for m in mineDensity:
        successRate = []
        while i<10:
            gb = Board(dim)
            gb.set_mines(int(dim**2*m))
            corners = [(0, 0), (0, dim - 1), (dim - 1, 0), (dim - 1, dim - 1)]
            agent = Agent(dim=dim, preferredCoords=corners)
            strategy4(gb,dim,agent)
            result = display(dim,agent)
            successRate.append(result)

        successRate = np.asarray(successRate)
        average.append(np.average(successRate))
        
    plt.figure(figsize = (10,10))
    plt.ylim(0,1)
    plt.title('Triple Improved Agent for Dimension 100')
    plt.xlabel('Mine Density')
    plt.ylabel('Average Success Rate')
    plt.scatter(mineDensity, average, c='#1f77b4', s=10)
    plt.plot(mineDensity, average)
    plt.savefig('DIMENSION100.png')
    plt.show()

#     while dim <= 50: #change to 50
#         print('dim= ', dim)
#         averages1 = []
#         averages2 = []
#         averages3 = []
#         averages4 = []
#         for m in mineDensity:
#             successRate1 = []
#             successRate2 = []
#             successRate3 = []
#             successRate4 = []
#             for i in range(1): #change to 30
#                 gb1= Board(dim)
#                 gb1.set_mines((dim**2)*m)
#                 corners = [(0, 0), (0, dim - 1), (dim - 1, 0), (dim - 1, dim - 1)]
#                 ag1 = Agent(dim=dim, preferredCoords=corners)
#                 strategy1(gb1, dim, ag1)
#                 result1 = display(dim, ag1)
#                 successRate1.append(result1)

#                 gb2 = Board(dim)
#                 gb2.set_mines((dim**2)*m)
#                 ag2 = Agent(dim=dim, preferredCoords=corners)
#                 strategy2(gb2, dim, ag2)
#                 result2 = display(dim, ag2)
#                 successRate2.append(result2)

#                 gb3 = Board(dim)
#                 gb3.set_mines((dim**2)*m)
#                 ag3 = Agent(dim=dim, preferredCoords=corners)
#                 strategy3(gb3, dim, ag3)
#                 result3 = display(dim, ag3)
#                 successRate3.append(result3)

#                 gb4 = Board(dim)
#                 gb4.set_mines((dim**2)*m)
#                 ag4 = Agent(dim=dim, preferredCoords=corners)
#                 strategy4(gb4, dim, ag4)
#                 result4 = display(dim, ag4)
#                 successRate4.append(result4)

#             successRate1 = np.asarray(successRate1)
#             averages1.append(np.average(successRate1))
#             successRate2 = np.asarray(successRate2)
#             averages2.append(np.average(successRate2))
#             successRate3 = np.asarray(successRate3)
#             averages3.append(np.average(successRate3))
#             successRate4 = np.asarray(successRate4)
#             averages4.append(np.average(successRate4))
#         #print(averages)
#         #biglist.append(averages)
#         plt.figure(figsize=(12,12))
#         plt.plot(mineDensity, averages1, label="Strategy 1")
#         plt.plot(mineDensity, averages2, label="Strategy 2")
#         plt.plot(mineDensity, averages3, label="Strategy 3")
#         plt.plot(mineDensity, averages4, label="Strategy 4")
#         plt.title("Comparison of All Strategies for Dimension {}".format(dim))
#         plt.xlabel('Mine Density')
#         plt.ylabel('Average Final Score')
#         plt.legend(loc='best')
#         plt.savefig('OverlaidStratsDim{}.png'.format(dim))
#         dim += 10

#     # dim = 10 
#     # for i in range(0,5): # change to 5
#     #     plt.figure(figsize=(12,12))
#     #     plt.ylim(0,1)
#     #     plt.scatter(mineDensity,biglist[i],c='#1f77b4', s=10)
#     #     for j in range(len(mineDensity)):
#     #         plt.text(mineDensity[j], biglist[i][j], '('+'%.1f' % mineDensity[j]+', '+'%.3f'%biglist[i][j]+')', size='x-small', in_layout=True, snap=True)
#     #         #plt.annotate(text='('+'%.1f' % mineDensity[j]+', '+'%.3f'%biglist[i][j]+')', xy=(mineDensity[j], biglist[i][j]))
#     #     plt.plot(mineDensity, biglist[i])
#     #     plt.title('Strategy 3 with Board of Dimension {}'.format(dim))
#     #     plt.xlabel('Mine Density')
#     #     plt.ylabel('Average Final Score')
#     #     plt.savefig('Strat3_Dimension {}.png'.format(dim))
#     #     dim += 10

#     # plt.figure(figsize=(10,10))
#     # plt.ylim(0,1)
#     # plt.plot(mineDensity, biglist[0], label='Dimension 10')
#     # plt.plot(mineDensity, biglist[1], label='Dimension 20')
#     # plt.plot(mineDensity, biglist[2], label='Dimension 30')
#     # plt.plot(mineDensity, biglist[3], label='Dimension 40')
#     # plt.plot(mineDensity, biglist[4], label='Dimension 50')
#     # plt.legend(loc='best')
#     # plt.savefig('Strat3_Overlaid Graphs.png')

#     # f, ax = plt.subplots(5,1, figsize=(15,15))
#     # dim = 10
#     # for i in range(0, 5):
#     #     ax[i].plot(mineDensity, biglist[i])
#     #     ax[i].set_title('Board with Dimension {}'.format(dim))
#     #     ax[i].set_xlabel('Mine Density')
#     #     ax[i].set_ylabel('Average Final Score')
#     #     dim += 10
#     # f.savefig('test.png', bbox_inches="tight")
#     # f.show()
#     # print(biglist)
testStrategy()
    
